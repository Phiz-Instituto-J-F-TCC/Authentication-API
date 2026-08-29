import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import Mock, patch

from app.services import auth_service


class FakeConnection:
    def __init__(self):
        self.cursor_value = object()
        self.commit = Mock()
        self.rollback = Mock()
        self.close = Mock()

    def cursor(self):
        return self.cursor_value


class AuthenticationServiceTests(unittest.TestCase):
    def test_should_confirm_active_email_without_starting_authentication(self):
        connection = FakeConnection()

        with patch.object(auth_service, "get_db", return_value=connection), patch.object(
            auth_service, "find_aluno_by_email", return_value=(1,)
        ), patch.object(auth_service, "send_auth_email") as send_auth_email:
            result = auth_service.validate_authentication_email("student@example.com")

        self.assertEqual(result, {"eligible": True})
        send_auth_email.assert_not_called()

    def test_should_reject_missing_or_inactive_email(self):
        connection = FakeConnection()

        with patch.object(auth_service, "get_db", return_value=connection), patch.object(
            auth_service, "find_aluno_by_email", return_value=None
        ):
            with self.assertRaises(auth_service.AuthError) as error:
                auth_service.validate_authentication_email("student@example.com")

        self.assertEqual(error.exception.status_code, 404)
        self.assertEqual(error.exception.detail, "E-mail não encontrado ou está inativo.")

    def test_should_start_authentication_with_the_phiz_id_from_the_miniapp(self):
        connection = FakeConnection()

        with patch.object(auth_service, "get_db", return_value=connection), patch.object(
            auth_service, "find_aluno_by_email", return_value=(1,)
        ), patch.object(auth_service, "insert_token") as insert_token, patch.object(
            auth_service, "send_auth_email"
        ) as send_auth_email:
            result = auth_service.create_authentication("Student@Example.com", "phiz-user-id")

        self.assertIn("polling_token", result)
        self.assertTrue(result["polling_token"])
        insert_token.assert_called_once()
        self.assertEqual(insert_token.call_args.args[4], "phiz-user-id")
        send_auth_email.assert_called_once()
        connection.commit.assert_called_once()

    def test_should_report_the_email_stage_when_email_delivery_fails(self):
        connection = FakeConnection()

        with patch.object(
            auth_service, "validate_authentication_email", return_value={"eligible": True}
        ), patch.object(auth_service, "get_db", return_value=connection), patch.object(
            auth_service, "find_aluno_by_email", return_value=(1,)
        ), patch.object(auth_service, "insert_token"), patch.object(
            auth_service, "send_auth_email", side_effect=TimeoutError
        ):
            with self.assertLogs(auth_service.logger, level="ERROR") as logs, self.assertRaises(
                auth_service.AuthError
            ) as error:
                auth_service.create_authentication("student@example.com", "phiz-user-id")

        self.assertEqual(error.exception.status_code, 500)
        self.assertIn(
            "authentication_failed stage=send_email error_type=TimeoutError",
            logs.output[0],
        )
        connection.rollback.assert_called_once()
        connection.close.assert_called_once()

    def test_should_reject_a_missing_phiz_id_before_accessing_the_database(self):
        with patch.object(auth_service, "get_db") as get_db:
            with self.assertRaises(auth_service.AuthError) as error:
                auth_service.create_authentication("student@example.com", "")

        self.assertEqual(error.exception.status_code, 422)
        self.assertEqual(error.exception.detail, "Phiz ID inválido.")
        get_db.assert_not_called()

    def test_should_update_the_student_phiz_id_after_confirmation(self):
        connection = FakeConnection()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=1)

        with patch.object(auth_service, "get_db", return_value=connection), patch.object(
            auth_service,
            "find_token",
            return_value=(7, "student@example.com", "phiz-id-from-server", expires_at, False),
        ), patch.object(auth_service, "update_aluno_phiz_id") as update_aluno_phiz_id, patch.object(
            auth_service, "mark_token_as_used"
        ) as mark_token_as_used:
            result = auth_service.validate_and_finish("confirmation-token")

        self.assertTrue(result["success"])
        update_aluno_phiz_id.assert_called_once_with(
            connection.cursor_value,
            "student@example.com",
            "phiz-id-from-server",
        )
        mark_token_as_used.assert_called_once_with(connection.cursor_value, 7)
        connection.commit.assert_called_once()

    def test_should_not_confirm_a_legacy_phone_request_as_a_phiz_id(self):
        connection = FakeConnection()
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=1)

        with patch.object(auth_service, "get_db", return_value=connection), patch.object(
            auth_service,
            "find_token",
            return_value=(7, "student@example.com", None, expires_at, False),
        ), patch.object(auth_service, "update_aluno_phiz_id") as update_aluno_phiz_id:
            result = auth_service.validate_and_finish("legacy-confirmation-token")

        self.assertFalse(result["success"])
        update_aluno_phiz_id.assert_not_called()
        connection.commit.assert_not_called()

    def test_should_reject_expired_polling_token(self):
        connection = FakeConnection()
        expired_at = datetime.now(timezone.utc) - timedelta(seconds=1)

        with patch.object(auth_service, "get_db", return_value=connection), patch.object(
            auth_service, "find_authentication_status", return_value=(False, expired_at)
        ):
            with self.assertRaises(auth_service.AuthError) as error:
                auth_service.get_authentication_status("polling-token")

        self.assertEqual(error.exception.status_code, 410)

    def test_should_reject_resend_during_server_cooldown(self):
        connection = FakeConnection()
        created_at = datetime.now(timezone.utc)

        with patch.object(auth_service, "get_db", return_value=connection), patch.object(
            auth_service,
            "find_authentication_for_resend",
            return_value=(42, "student@example.com", False, created_at),
        ), patch.object(auth_service, "send_auth_email") as send_auth_email:
            with self.assertRaises(auth_service.AuthError) as error:
                auth_service.resend_authentication("polling-token")

        self.assertEqual(error.exception.status_code, 429)
        send_auth_email.assert_not_called()

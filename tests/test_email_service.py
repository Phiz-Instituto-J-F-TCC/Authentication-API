import unittest
from unittest.mock import call, patch

from app.services import email_service


class EmailServiceTests(unittest.TestCase):
    def test_should_send_using_tls_and_a_bounded_smtp_connection(self):
        with patch.object(email_service, "FROM_EMAIL", "sender@example.com"), patch.object(
            email_service, "FROM_PASSWORD", "not-a-real-password"
        ), patch("app.services.email_service.smtplib.SMTP") as smtp:
            server = smtp.return_value.__enter__.return_value

            email_service.send_auth_email(
                "student@example.com",
                "https://example.com/finish_authentication?token=test-token",
            )

        smtp.assert_called_once_with(
            email_service.SMTP_HOST,
            email_service.SMTP_PORT,
            timeout=email_service.SMTP_TIMEOUT_SECONDS,
        )
        self.assertEqual(server.ehlo.call_args_list, [call(), call()])
        server.starttls.assert_called_once()
        server.login.assert_called_once_with("sender@example.com", "not-a-real-password")
        server.send_message.assert_called_once()

    def test_should_fail_before_connecting_when_smtp_configuration_is_missing(self):
        with patch.object(email_service, "FROM_EMAIL", None), patch.object(
            email_service, "FROM_PASSWORD", None
        ), patch("app.services.email_service.smtplib.SMTP") as smtp:
            with self.assertRaisesRegex(RuntimeError, "SMTP configuration is missing"):
                email_service.send_auth_email(
                    "student@example.com",
                    "https://example.com/finish_authentication?token=test-token",
                )

        smtp.assert_not_called()

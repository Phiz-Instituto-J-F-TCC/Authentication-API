import unittest
from urllib.error import HTTPError
from unittest.mock import MagicMock, patch

from app.services import email_service


class EmailServiceTests(unittest.TestCase):
    def test_should_send_email_using_resend_https_api(self):
        response = MagicMock()
        response.status = 201

        with patch.object(email_service, "RESEND_API_KEY", "not-a-real-key"), patch.object(
            email_service, "RESEND_FROM_EMAIL", "Phiz <onboarding@resend.dev>"
        ), patch("app.services.email_service.urlopen") as urlopen:
            urlopen.return_value.__enter__.return_value = response

            email_service.send_auth_email(
                "student@example.com",
                "https://example.com/finish_authentication?token=test-token",
            )

        request = urlopen.call_args.args[0]
        self.assertEqual(request.full_url, email_service.RESEND_EMAILS_URL)
        self.assertEqual(request.get_method(), "POST")
        self.assertEqual(request.get_header("Authorization"), "Bearer not-a-real-key")
        self.assertEqual(urlopen.call_args.kwargs["timeout"], email_service.RESEND_TIMEOUT_SECONDS)

    def test_should_fail_without_resend_configuration(self):
        with patch.object(email_service, "RESEND_API_KEY", None), patch.object(
            email_service, "RESEND_FROM_EMAIL", None
        ), patch("app.services.email_service.urlopen") as urlopen:
            with self.assertRaisesRegex(RuntimeError, "Resend configuration is missing"):
                email_service.send_auth_email(
                    "student@example.com",
                    "https://example.com/finish_authentication?token=test-token",
                )

        urlopen.assert_not_called()

    def test_should_keep_resend_http_status_without_logging_response_content(self):
        error = HTTPError(email_service.RESEND_EMAILS_URL, 422, "Unprocessable", {}, None)

        with patch.object(email_service, "RESEND_API_KEY", "not-a-real-key"), patch.object(
            email_service, "RESEND_FROM_EMAIL", "Phiz <onboarding@resend.dev>"
        ), patch("app.services.email_service.urlopen", side_effect=error):
            with self.assertRaises(email_service.ResendEmailError) as raised_error:
                email_service.send_auth_email(
                    "student@example.com",
                    "https://example.com/finish_authentication?token=test-token",
                )
import unittest

from app.services.phiz_identity_service import (
    PhizIdentityResolutionError,
    resolve_phiz_id,
)


class ResolvePhizIdTests(unittest.TestCase):
    def test_should_reject_a_missing_login_code(self):
        with self.assertRaises(PhizIdentityResolutionError) as error:
            resolve_phiz_id("")

        self.assertEqual(error.exception.status_code, 422)

    def test_should_require_the_official_server_integration(self):
        with self.assertRaises(PhizIdentityResolutionError) as error:
            resolve_phiz_id("temporary-login-code")

        self.assertEqual(error.exception.status_code, 501)

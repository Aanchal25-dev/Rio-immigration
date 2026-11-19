from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from .views import add_applicant


class ApplicantBirthDateTests(SimpleTestCase):
    def test_invalid_birth_dates_are_rejected_before_creating_applicant(self):
        for dob in ["199754-04-18", "12345-01-01", "2024-02-30", "0000-01-01"]:
            with self.subTest(dob=dob):
                request = RequestFactory().post("/add_applicant/", {"dob": dob})
                request.user = SimpleNamespace(is_authenticated=True)
                with patch("rio.views.messages.error") as error:
                    response = add_applicant(request)
                self.assertEqual(response.status_code, 302)
                error.assert_called_once_with(
                    request, "Enter a valid date of birth with a four-digit year."
                )

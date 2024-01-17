from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import BasePermission

from website.TextChoices import LicenseStatus
from website.models import License, Config


class CheckLicenseStatus(BasePermission):
    # todo check license status

    def has_permission(self, request, view):
        return self.check_license(request)

    def check_license(self, request):
        license_key = Config.objects.get(key="license_key", is_active=True).value
        lic = License.objects.filter(license_key=license_key).first()
        if lic is None:
            raise self.raise_validation_error("License does not exists for your system")
        if lic.status == LicenseStatus.INACTIVE:
            raise self.raise_validation_error("Please activate your license first")
        if lic.status == LicenseStatus.REVOKED:
            raise self.raise_validation_error(
                "Your license has been revoked please contact the provider"
            )
        if lic.end_date < timezone.datetime.now().date():
            raise self.raise_validation_error(
                "Your subscription has expired please renew it"
            )
        return True

    def raise_validation_error(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        raise ValidationError({"message": [message]})

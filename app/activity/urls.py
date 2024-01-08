from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from activity.apis import AttendanceAPI, AttendanceRequestAPI, LeaveRequestAPI

router = routers.DefaultRouter()

router.register(r"web/calendar", AttendanceAPI, basename="calender")
router.register(
    r"web/attendance-request", AttendanceRequestAPI, basename="attendance-request"
)
router.register(r"web/leave-request", LeaveRequestAPI, basename="leave-request")
urlpatterns = []

urlpatterns += router.urls + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

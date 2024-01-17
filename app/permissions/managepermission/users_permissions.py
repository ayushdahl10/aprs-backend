STAFF_API = [
    ("staffs-list", "get"),
    ("staffs-list", "post"),
    ("staffs-detail", "patch"),
    ("staffs-detail", "get"),
    ("staffs-update-user-detail", "patch"),
]

DEPARTMENT_API = [
    ("departments-list", "get"),
    ("departments-list", "post"),
    ("departments-detail", "get"),
    ("departments-detail", "patch"),
]

ATTENDANCE_API = [
    ("calender-list", "get"),
    ("calender-detail", "get"),
]

COMPANY_API = [
    ("companies-list", "get"),
    ("companies-list", "post"),
    ("companies-detail", "patch"),
    ("companies-detail", "get"),
]

ATTEN_REQUEST_API = [
    ("attendance-request-list", "post"),
    ("attendance-request-list", "get"),
    ("attendance-request-detail", "get"),
    ("attendance-request-detail", "patch"),
    ("attendance-request-detail", "delete"),
]

ATTENDANCE_REQUEST_STATUS_API = [
    ("attendance-request-update-attendance-request", "patch"),
]

ATTENDANCE_REQUEST_GET_STAFF_API = [
    ("attendance-request-get-staff-pending-request", "get"),
]

LEAVE_REQUEST_API = [
    ("leave-request-list", "post"),
    ("leave-request-list", "get"),
    ("leave-request-detail", "get"),
    ("leave-request-detail", "patch"),
    ("leave-request-detail", "delete"),
    ("leave-request-check-request", "get"),
]

UPDATE_LEAVE_REQUEST = [
    ("leave-request-update-leave-request", "patch"),
    ("leave-request-check-staff-request", "get"),
]

from django.db.models import TextChoices


class LayoutTypes(TextChoices):
    DEFAULT_LAYOUT = "default_layout", ("Default Layout")
    ADMIN_LAYOUT = "default_admin_layout", ("Admin Layout")


class SectionTypes(TextChoices):
    HEADER = "header", ("Header")
    BODY = "body", ("Body")
    FOOTER = "footer", ("Footer")

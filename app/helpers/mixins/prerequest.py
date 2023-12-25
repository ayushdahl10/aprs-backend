class RequestHandler:
    @property
    def is_paginated(self):
        if self.request.GET.get("paginate") is None:
            return True
        return eval(self.request.GET.get("paginate", "false").capitalize())

    @property
    def get_client_ip_address(self):
        user_ip = (
            self.request.META.get("HTTP_X_FORWARDED_FOR")
            or self.request.META.get("HTTP_X_REAL_IP")
            or self.request.META.get("REMOTE_ADDR")
        )
        return user_ip

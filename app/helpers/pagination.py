from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 200
    def get_max_page_size(self):
        return 100

    def paginate_queryset(self, queryset, request, view=None):
        self.max_page_size = self.get_max_page_size()
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        page_data = {
                "total_pages": self.page.paginator.num_pages,
                "total_records": self.page.paginator.count,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "record_range": self.get_record_range(),
                "current_page": self.page.number,
            }
        data=data
        page_data=page_data
        return Response(page_data).data,Response(data).data

    def get_record_range(self):
        """
        Range of contents in current page.
        """

        paginator = self.page.paginator
        current_page = self.page.number
        content_per_page = paginator.per_page

        if paginator.count == 0:
            range_start = 0
            range_end = 0
        else:
            range_start = content_per_page * (current_page - 1) + 1
            range_end = content_per_page * current_page

        if range_end > paginator.count:
            range_end = paginator.count

        return [range_start, range_end]


class CustomPage(CustomPagination):
    page_size = 1000
    max_page_size = 1000

    def get_max_page_size(self):
        return self.max_page_size
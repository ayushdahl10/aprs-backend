from django.http import HttpResponse
from django.db.models import Q
from django.template import loader
from manager.models import Page
from abc import ABC
from django.db.models import Count
from manager.models import ComponentSection


class BaseView(ABC):
    data: dict = {}

    def __init__(self, request, data, *args, **kwargs) -> None:
        self.data = data
        super().__init__()

    def fill_templates(self):
        pass

    @staticmethod
    def index(request):
        route = request.path
        section: dict = {}
        component_loader: str = ""
        querysets: list = []
        page_section_list = []
        page = Page.objects.filter(page_route=route).first()
        if page is None:
            return HttpResponse("Page not found")
        section.update({"page_title": page.name})
        layout_type = page.layout_type
        template = loader.get_template(f"layout/{layout_type}.html")
        groupped_section = list(
            page.component_section.values("section").annotate(count=Count("section"))
        )
        page_section_list = list(
            page.component_section.all().values_list("id", flat=True)
        )
        for component_section in groupped_section:
            compsection = ComponentSection.objects.filter(
                Q(section=component_section.get("section"))
                & Q(is_active=True)
                & Q(id__in=page_section_list)
            ).order_by("order")
            querysets.append(compsection)
        for queryset in querysets:
            component_loader = ""
            for qt in queryset:
                print(qt.component.path)
                path: str = qt.component.path
                section_name: str = qt.section.name
                print(path)
                component_loader += loader.render_to_string(f"template_types/{path}")
                section.update({section_name: component_loader})
        return HttpResponse(template.render(section, request))

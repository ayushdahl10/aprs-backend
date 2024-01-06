from django.db.models import ObjectDoesNotExist
from rest_framework import serializers


class DetailRelatedField(serializers.RelatedField):
    """
    Read/write serializer field for relational field.
    Syntax:
            DetailRelatedField(Model, [lookup], representation)

            Model: model to which the serializer field is related to
            lookup: field for getting a model instance, if not supplied it defaults to idx
            representation: a model instance method name for getting serialized data
    """

    def __init__(self, model, **kwargs):
        if not kwargs.get("read_only"):
            kwargs["queryset"] = model.objects.all()

        self.lookup = kwargs.pop("lookup", None) or "idx"

        try:
            self.representation = kwargs.pop("representation")
        except KeyError:
            raise Exception("Please supply representation.")

        super(DetailRelatedField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.queryset.get(**{self.lookup: data})
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Object does not exist.")

    def to_representation(self, obj):
        return getattr(obj, self.representation)()

    def get_choices(self, cutoff=None):
        queryset = self.get_queryset()
        if queryset is None:
            return {}

        if cutoff is not None:
            queryset = queryset[:cutoff]

        # cast representation of item to str because
        # to representation could return a dict
        # and dicts can't be used as key on dicts because dicts are not hashable
        return {
            str(self.to_representation(item)): self.display_value(item)
            for item in queryset
        }

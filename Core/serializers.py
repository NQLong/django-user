from django.core import serializers
import json

class BaseSerializer:
    class Meta:
        ...

    def __init__(self, instance=None, *, data=None):
        ...
        if type(instance) != self.Meta.model:
            raise Exception("invalid serializer model")
        self.instance = instance
        self.data = data
        self.handle()

    def to_representation(self, instance: object):
        data= {}
        serializer = json.loads( serializers.serialize("json",[instance]))[0]
        print(serializer)
        for _field in self.Meta.fields:
            if _field == "id":
                data[_field] = serializer.get("pk")
            data[_field] = serializer["fields"].get(_field)
        return data

    def handle(self):
        if self.instance:
            self.data = self.to_representation(self.instance)

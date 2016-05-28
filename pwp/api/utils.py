# coding: utf-8

import json
from django.db.models.fields.related import ManyToManyField

def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, ManyToManyField):
            if instance.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(instance).values_list('pk', flat=True))
        else:
            data[f.name] = f.value_from_object(instance)
    return data

def parseJSON(body):
    return json.loads(body.decode("utf-8"))

def serialize_json(data, model, pk=None):
    serialized_json = dict()
    serialized_json['fields'] = data
    if pk:
        serialized_json['pk'] = pk
    serialized_json['model'] = model
    return json.dumps([serialized_json])

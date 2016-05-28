# coding: utf-8

import json
def parseJSON(body):
    return json.loads(body.decode("utf-8"))

def serialize_json(data, model, pk=None):
    serialized_json = dict()
    serialized_json['fields'] = data
    if pk:
        serialized_json['pk'] = pk
    serialized_json['model'] = model
    return json.dumps([serialized_json])

# coding: utf-8

import json

def parseJSON(body):
    return json.loads(body.decode("utf-8"))

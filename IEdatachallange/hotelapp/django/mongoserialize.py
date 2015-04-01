# -*- coding: utf-8 -*-
"""
Created on Sat Feb 14 07:19:22 2015

@author: root
"""

from django.core.serializers.json import DjangoJSONEncoder
from bson import objectid
class MongoAwareEncoder(DjangoJSONEncoder):
    """JSON encoder class that adds support for Mongo objectids."""
    def default(self, o):
        if isinstance(o, objectid.ObjectId):
            return str(o)
        else:
            return super(MongoAwareEncoder, self).default(o)
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import flash, render_template, jsonify, request, redirect, url_for
from flask import current_app as app
from models.models import db


# Enable instance of SQLAlchemy
db.init_app(app)


# Create a JSON Response
def createJsonResponse(status = 'error', cmd = None, action = None):
    jsonData = {
        'status': status,
        'cmd': cmd,
        'action': action
    }
    return jsonify(jsonData)


# Remove Item from List
def removeItemFromList(lst, k, v):
    for listItem in lst:
        if listItem.get(k) == v:
            lst.remove(listItem)


# Update Item from List
def updateItemFromList(lst, k, v, obj, updK, updV, updObj):
    for listItem in lst:
        if obj is None:
            if listItem.get(k) == v:
                if updObj is not None:
                    listItem.get(updObj, {})[updK] = updV
                else:
                    listItem[updK] = updV
        else:
            if listItem.get(obj, {}).get(k) == v:
                if updObj is not None:
                    listItem.get(updObj, {})[updK] = updV
                else:
                    listItem[updK] = updV


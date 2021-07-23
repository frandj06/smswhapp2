import firebase_admin

from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from firebase_admin import auth, credentials
from flask import flash, render_template, jsonify, request, redirect, url_for
from flask import current_app as app
from models.models import db


# Enable instance of SQLAlchemy
db.init_app(app)


# Enable Firebase Admin
cred = credentials.Certificate(app.config.get('GOOGLE_APPLICATION_CREDENTIALS'))
fba = firebase_admin.initialize_app(cred)


# Create a JSON Response
def createJsonResponse(status = 'error', cmd = None, action = None):
    jsonData = {
        'status': status,
        'cmd': cmd,
        'action': action
    }
    return jsonify(jsonData)


# Creates a Firebase Cookie Session instance
def createCookieSession(idToken, cmd = None, action = None):
    try:
        # Set session expiration to 14 days.
        expires_in = td(days = 14)

        # Set cookie policy for session cookie.
        expires = dt.now(tz.utc) + expires_in

        # Create the session cookie. This will also verify the ID token in the process.
        # The session cookie will have the same claims as the ID token.
        session_cookie = auth.create_session_cookie(idToken, expires_in = expires_in)

        # Create an HTTP Response with a JSON Success Status and attach the cookie to it.
        response = createJsonResponse('success', cmd, action)

        if app.config['ENV'] == 'development':
            # Cookies for Development
            response.set_cookie(app.config['FIREBASE_COOKIE_NAME'], session_cookie, expires = expires, httponly = False, samesite = 'Lax', secure = False)
        else:
            # Cookies for Production
            response.set_cookie(app.config['FIREBASE_COOKIE_NAME'], session_cookie, expires = expires, httponly = True, samesite = 'Lax', secure = True)

        return response
    except Exception as e:
        app.logger.error('** SWING_CMS ** - CreateCookieSession Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


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


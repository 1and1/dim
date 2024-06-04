# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from hashlib import md5
from flask import Flask, request, redirect, current_app
from time import gmtime
from xmltodict import parse

import requests
import urllib.parse

app = Flask(__name__)
app.config.from_pyfile('config.py', silent=True)
app.config.from_pyfile('/etc/dim/cas.cfg', silent=True)


@app.after_request
def after_request(response):
    if app.config.get('FRONTEND_SERVICE', ''):
        header = response.headers
        header['Access-Control-Allow-Origin'] = app.config['FRONTEND_SERVICE']
    return response


@app.route("/")
def login():
    if (not app.config.get('CURRENT_SERVICE', '') or
        not app.config.get('CAS_LOGIN_URL', '') or
            not app.config.get('CAS_VALIDATE_URL', '')):
        return "CAS config incomplete", 500

    if (not app.config.get('FRONTEND_SERVICE', '') or
        not app.config.get('TOOL_NAME', '') or
            not app.config.get('SECRET_KEY', '')):
        return "DIM frontend config incomplete", 500

    if 'ticket' not in request.args:
        return redirect(app.config['CAS_LOGIN_URL'].format(
          app.config['CURRENT_SERVICE']))

    ticket = request.args['ticket']
    cas_response = requests.get(app.config['CAS_VALIDATE_URL'].format(
        app.config['CURRENT_SERVICE'], ticket))

    tree = parse(cas_response.content)
    if not tree.get('cas:serviceResponse', False):
        return "CAS response invalid", 500

    service_response = tree.get('cas:serviceResponse')
    if (not service_response.get('cas:authenticationSuccess', False) and
            not service_response.get('cas:authenticationFailure', False)):
        return "CAS response invalid", 400

    if service_response.get('cas:authenticationFailure', False):
        return service_response.get('cas:authenticationFailure').get('#text'), 400

    success = service_response.get('cas:authenticationSuccess', False)
    if not success.get('cas:user', False):
        return "CAS response does not contain user", 400

    username = success.get('cas:user')
    attributes = success.get('cas:attributes')

    last_name = ''
    if 'cas:lastName' in attributes:
        last_name = attributes['cas:lastName'].encode('latin-1')
    first_name = ''
    if 'cas:firstName' in attributes:
        first_name = attributes['cas:firstName'].encode('latin-1')
    full_name = first_name + b" " + last_name
    salt = str(gmtime())

    response = current_app.make_response(redirect(app.config['FRONTEND_SERVICE']))
    response.set_cookie(
      key='LOGIN_ARGS',
      value=urllib.parse.urlencode({
        'username': username,
        'tool': app.config['TOOL_NAME'],
        'salt': salt,
        'sign': md5((username + salt + app.config['SECRET_KEY']).encode()).hexdigest()
      }),
      expires=datetime.now() + timedelta(seconds=24 * 3600)
    )
    response.set_cookie(
      key='FULL_NAME',
      value=full_name,
      expires=datetime.now() + timedelta(seconds=24 * 3600)
    )
    return response


@app.route("/logout")
def logout():
    if not app.config.get('CAS_LOGOUT_URL', ''):
        return "CAS config incomplete", 500
    return redirect(app.config['CAS_LOGOUT_URL'])


if __name__ == "__main__":
    app.run(ssl_context='adhoc', port=443, host='0.0.0.0')

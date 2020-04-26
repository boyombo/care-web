import base64

import binascii
from django.contrib.auth import authenticate
from django.http import HttpResponse


def basic_error_response(message="Restricted Area"):
    response = HttpResponse("401-{}".format(message))
    response.status_code = 401
    response["WWW-Authenticate"] = 'Basic realm="restricted area"'
    return response


def basic_auth(request):
    if "HTTP_AUTHORIZATION" in request.META:
        auth = request.META["HTTP_AUTHORIZATION"].split()
        if len(auth) == 2:
            if auth[0].lower() == "basic":
                try:
                    b_username, b_pwd = base64.b64decode(auth[1]).split(b":", 1)
                    username = b_username.decode("utf-8")
                    password = b_pwd.decode("utf-8")
                    usr = authenticate(username=username, password=password)
                    return usr, ""
                except Exception as e:
                    print(e)
                    return None, "Malformed authorization header"
            return None, "Invalid authorization header"
        return None, "Invalid authorization header"
    return None, "Invalid request header"

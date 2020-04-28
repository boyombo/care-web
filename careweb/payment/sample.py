import base64


def check(param):
    auth = param.split()
    if len(auth) == 2:
        if auth[0].lower() == "basic":
            try:
                b_username, b_pwd = base64.b64decode(auth[1]).split(b":", 1)
                username = b_username.decode("utf-8")
                password = b_pwd.decode("utf-8")
                print(username, password)
            except Exception as e:
                print(e, "Somethign went wrong")


# encoded = base64.b64encode('admin:FutureCare')
# authorization_header = "Basic " + encoded
check("basic admin")
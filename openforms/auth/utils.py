import datetime
from functools import wraps
import jwt
from flask import request, abort, current_app as app


def get_jwt(user_id, expire_in=120):
    """
    param:
        user_id -> string
        expire_in -> time in minutes, default=120
    return:
        token -> string
    """
    try:
        payload = {
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=expire_in),
            "iat": datetime.datetime.utcnow(),
            "sub": user_id,
        }
        return jwt.encode(payload, app.config.get("SECRET_KEY"), algorithm="HS256")
    except Exception as e:
        return str(e)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not "Authorization" in request.headers:
            pass

        print(request.headers["Authorization"])
        data = request.headers["Authorization"]
        token = str.replace(str(data), 'Bearer ', '')

        user_id = None
        try:
            if token == "":
                raise Exception("JWT token not found!")

            user_id = jwt.decode(token, app.config.get("SECRET_KEY"), algorithms=["HS256"])["sub"]

        except jwt.ExpiredSignatureError:
            return {"status": "error", "data": "Please login again, session expired"}

        except Exception as e:
            raise e

        kwargs["user"] = user_id
        return f(*args, **kwargs)

    return decorated_function

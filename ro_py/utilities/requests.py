from ro_py.utilities.errors import ApiError
from json.decoder import JSONDecodeError
import requests


class Requests:
    def __init__(self):
        self.headers = {}
        self.session = requests.Session()

    def get(self, *args, **kwargs):
        kwargs["headers"] = self.headers

        get_request = self.session.get(*args, **kwargs)

        try:
            get_request_json = get_request.json()
        except JSONDecodeError:
            return get_request

        if isinstance(get_request_json, dict):
            try:
                get_request_error = get_request_json["errors"]
            except KeyError:
                return get_request
        else:
            return get_request

        raise ApiError(f"[{str(get_request.status_code)}] {get_request_error[0]['message']}")

    def post(self, *args, **kwargs):
        kwargs["headers"] = self.headers

        post_request = self.session.post(*args, **kwargs)

        if post_request.status_code == 403:
            if "X-CSRF-TOKEN" in post_request.headers:
                self.headers['X-CSRF-TOKEN'] = post_request.headers["X-CSRF-TOKEN"]
                post_request = self.session.post(*args, **kwargs)

        try:
            post_request_json = post_request.json()
        except JSONDecodeError:
            return post_request

        if isinstance(post_request_json, dict):
            try:
                post_request_json["errors"]
            except KeyError:
                return post_request
        else:
            return post_request

    def patch(self, *args, **kwargs):
        kwargs["headers"] = self.headers

        patch_request = self.session.patch(*args, **kwargs)

        if patch_request.status_code == 403:
            if "X-CSRF-TOKEN" in patch_request.headers:
                self.headers['X-CSRF-TOKEN'] = patch_request.headers["X-CSRF-TOKEN"]
                patch_request = self.session.patch(*args, **kwargs)

        patch_request_json = patch_request.json()

        if isinstance(patch_request_json, dict):
            try:
                patch_request_error = patch_request_json["errors"]
            except KeyError:
                return patch_request
        else:
            return patch_request

        raise ApiError(f"[{str(patch_request.status_code)}] {patch_request_error[0]['message']}")

    def update_xsrf(self, url="https://www.roblox.com/favorite/toggle"):
        xsrf_req = self.session.post(url)
        self.headers['X-CSRF-TOKEN'] = xsrf_req.headers["X-CSRF-TOKEN"]

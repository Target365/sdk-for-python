class HttpErrorHandler:
    def throw_if_not_success(self, response):
        if (response.status_code < 200) or (response.status_code >= 300):
            self.throw_error(response)

    # noinspection PyMethodMayBeStatic
    def throw_error(self, response):
        message = ""
        try:
            message = response.json()
        except Exception:
            message = response.status_code
        raise HttpError(message)


class HttpError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

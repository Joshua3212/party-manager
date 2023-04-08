from django.shortcuts import redirect

from app.config import config


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not config:
            raise Exception(
                "Huddu Store config has to be defined; Check README.md for more info "
            )

        for i in config["teams"]:

            if (
                request.COOKIES.get("x-password") == i["password"]
                and request.COOKIES.get("x-name") == i["name"]
            ):
                return self.get_response(request)

        if not request.path == "/" or not request.GET.get("login"):
            return redirect("/?login=1")
        return self.get_response(request)

from django.shortcuts import redirect

from app import config


class AuthMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not config.config:
            raise Exception("Huddu Store config has to be defined; Check README.md for more info ")

        if not request.COOKIES.get("x-password") == password or not request.COOKIES.get("x-username") == username:
            return redirect("/?login=1")

        if request.GET.get("login") and request.COOKIES.get("x-password") == password and request.COOKIES.get(
                "x-username") == username:
            return redirect("/")

        return self.get_response(request)

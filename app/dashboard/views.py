import secrets

from django.shortcuts import render

from app.config import store


# Create your views here.

def register_customer(request):
    if request.method == "GET":
        return render(request, "register_customer.html", {})
    if request.method == "POST":
        token = secrets.token_hex(16)
        customer = {
            "_id": token,
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
            "birthdate": request.POST["birthdate"]
        }

        store.put(
            token, customer
        )

        return render(request, "register_customer.html", {"success": True})


def verify_customer(request):
    if request.method == "GET":
        return render(request, "verify_customer.html", {})
    if request.method == "POST":
        token = secrets.token_hex(16)
        customer = {
            "_id": token,
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
            "birthdate": request.POST["birthdate"]
        }

        store.put(
            token, customer
        )

        return render(request, "verify_customer.html", {"success": True})


def customers(request):
    if request.method == "GET":
        return render(request, "customers.html", {
            "customers": store.list(request.GET.get("limit", 25), request.GET.get("skip", 0))
        })


def index(request):
    if request.method == "GET":
        return render(request, "index.html", {
        })

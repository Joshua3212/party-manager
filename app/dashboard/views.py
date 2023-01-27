import secrets

from django.shortcuts import render, redirect

from app.config import store


# Create your views here.

def register_customer(request):
    if request.method == "GET":
        return render(request, "register_customer.html", {})
    if request.method == "POST":
        token = secrets.token_hex(16)
        customer = {
            "first_name": request.POST["first_name"],
            "last_name": request.POST["last_name"],
            "birthdate": request.POST["birthdate"]
        }

        store.put(
            token, customer

        )

        return redirect("/register")

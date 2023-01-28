import json
import secrets

import cv2
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
            "birthdate": request.POST["birthdate"],
        }

        store.put(token, customer)

        return render(request, "register_customer.html", {"success": True})


def verify_customer(request):
    if request.method == "GET":
        return render(request, "verify_customer.html", {})
    if request.method == "POST":
        error = False
        token = None
        booking = None

        # file
        print(request.FILES)
        if request.FILES.get("qr"):
            file = request.FILES.get("qr")

            with open("tmp.image", "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                    destination.close()

            try:
                img = cv2.imread("tmp.image")
                detect = cv2.QRCodeDetector()
                token, points, straight_qrcode = detect.detectAndDecode(img)
            except:
                error = {"error": "Kein QR code erkannt."}

        # override token if manually provided
        if request.GET.get("token"):
            token = request.GET.get("token")
        if token:
            booking = store.get(token)
            if not booking:
                error = {"error": f"Keine Buchung für {token} gefunden"}
        else:
            error = {"error": "Weder token noch QR code gegeben."}

        return render(
            request,
            "verify_customer.html",
            {
                "success": json.dumps(booking, indent=3) if booking else None,
                "error": json.dumps(error, indent=3) if error else None,
            },
        )


def customers(request):
    if request.method == "GET":
        return render(
            request,
            "customers.html",
            {
                "customers": store.list(
                    request.GET.get("limit", 25), request.GET.get("skip", 0)
                )
            },
        )


def index(request):
    if request.method == "GET":
        return render(request, "index.html", {})

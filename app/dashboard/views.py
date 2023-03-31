import json
import time

import cv2
from django.shortcuts import render

from app.config import store


# Create your views here.


def register_customer(request):
    if request.method == "GET":
        return render(request, "register_customer.html", {})
    if request.method == "POST":
        customer = {
            "_id": request.POST.get("identifier"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "birthdate": request.POST.get("birthdate"),
            "is_teacher": bool(int(request.POST.get("is_teacher"))),
            "created": int(time.time()),
        }

        store.put(request.POST.get("identifier"), customer)

        return render(request, "register_customer.html", {"success": True})


def verify_customer(request):
    if request.method == "GET":
        return render(request, "verify_customer.html", {})
    if request.method == "POST":
        error = False
        identifier = None
        booking = None

        # file
        if request.FILES.get("qr"):
            file = request.FILES.get("qr")

            with open("tmp.image", "wb+") as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
                    destination.close()

            try:
                img = cv2.imread("tmp.image")
                detect = cv2.QRCodeDetector()
                identifier, points, straight_qrcode = detect.detectAndDecode(img)
            except:
                error = {"error": "Kein QR code erkannt."}

        # override token if manually provided
        if request.POST.get("identifier"):
            identifier = request.POST.get("identifier")
        if identifier:
            booking = store.get(identifier)
            if not booking:
                error = {"error": f"Keine Buchung für {identifier} gefunden"}
        else:
            error = {"error": "Weder token noch QR code gegeben."}

        return render(
            request,
            "verify_customer.html",
            {
                "success": booking,
                "error": json.dumps(error, indent=3) if error else None,
            },
        )


def customers(request):
    if request.method == "GET":
        print(store.list())
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

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
            "id": request.POST.get("identifier"),
            "first_name": request.POST.get("first_name"),
            "last_name": request.POST.get("last_name"),
            "birthdate": request.POST.get("birthdate"),
            "is_teacher": bool(int(request.POST.get("is_teacher", 0))),
            "created_by": request.COOKIES.get("x-name"),
            "created": int(time.time()),
        }

        try:
            store.put(request.POST.get("identifier"), customer)
            store.put(
                request.POST.get("first_name") + " " + request.POST.get("last_name"),
                request.POST.get("identifier"),
            )
            store.put(
                request.POST.get("last_name") + " " + request.POST.get("first_name"),
                request.POST.get("identifier"),
            )
        except Exception:
            return render(
                request,
                "register_customer.html",
                {
                    "error": "Kartennummern wurde schon vergeben. Kartennummern können nur einmal vergeben werden"
                },
            )

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
        data = store.list(
            request.GET.get("limit", 25),
            request.GET.get("skip", 0),
            prefix=request.GET.get("search", None),
        )

        res = []
        for i in data:
            if type(i["value"]) == int and request.GET.get("search"):
                i = store.get(i["value"])
                res.append(i)
            else:
                res.append(i["value"])

        return render(
            request,
            "customers.html",
            {
                "customers": [json.loads(i) for i in set([json.dumps(i) for i in res])],  # super hacky but it works!
                "search": request.GET.get("search", ""),
                "limit": request.GET.get("limit", 25),
                "has_skip": bool(request.GET.get("skip", 0)),
                "skip": request.GET.get("skip", 0),
            },
        )


def index(request):
    if request.method == "GET":
        return render(request, "index.html", {})

import json
import time

import cv2
from django.shortcuts import render

from app.config import mongo_collection


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
            mongo_collection.insert_one(customer)
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
            booking = mongo_collection.find_one({"id": identifier})
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
        if request.GET.get("search", None):
            data = mongo_collection.find(
                {
                    "$or": [
                        {
                            "id": {
                                "$regex": str(request.GET.get("search", "")),
                            }
                        },
                        {
                            "first_name": {
                                "$regex": request.GET.get("search", ""),
                            }
                        },
                        {
                            "last_name": {
                                "$regex": request.GET.get("search", ""),
                            }
                        },
                    ]
                },
                limit=request.GET.get("limit", 25),
                skip=request.GET.get("skip", 0),
            )
        else:
            data = mongo_collection.find(
                {},
                limit=request.GET.get("limit", 25),
                skip=request.GET.get("skip", 0),
            )
        res = []

        for i in data:
            del i["_id"]
            res.append(i)
        return render(
            request,
            "customers.html",
            {
                "customers": [
                    json.loads(i) for i in set([json.dumps(i) for i in res])
                ],  # super hacky but it works!
                "search": request.GET.get("search", ""),
                "limit": request.GET.get("limit", 25),
                "has_skip": bool(request.GET.get("skip", 0)),
                "skip": request.GET.get("skip", 0),
            },
        )


def index(request):
    if request.method == "GET":
        return render(request, "index.html", {})

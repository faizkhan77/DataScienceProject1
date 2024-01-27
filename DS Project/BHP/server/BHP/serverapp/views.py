from django.shortcuts import render, HttpResponse
import requests
import json
import pickle
from django.http import JsonResponse
import numpy as np

# Create your views here.

__locations = None
__data_columns = None
__model = None


def home(request):
    return HttpResponse("Hello")


def load_saved_artifacts():
    print("loading saved artifacts...start")
    global __data_columns
    global __locations

    with open("./artifacts/columns.json", "r") as f:
        __data_columns = json.load(f)["data_columns"]
        print(__data_columns)
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    global __model
    if __model is None:
        with open("./artifacts/banglore_home_prices_model.pickle", "rb") as f:
            __model = pickle.load(f)
    print("loading saved artifacts...done")


def get_locations():
    # load_saved_artifacts()
    global __locations
    return __locations


def load_artifacts(request):
    load_saved_artifacts()
    locations = get_locations()
    print("Locations:", locations)
    return HttpResponse("Artifacts loaded successfully")


def get_data_columns():
    return __data_columns


def get_estimated_price(location, sqft, bhk, bath):
    load_saved_artifacts()
    get_locations()
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)


def get_price(request):
    esm1 = get_estimated_price("1st Phase JP Nagar", 4000, 3, 3)
    esm2 = get_estimated_price("1st Phase JP Nagar", 1000, 2, 2)
    esm3 = get_estimated_price("Ejipura", 1000, 2, 2)
    esm4 = get_estimated_price("Kalhalli", 1000, 2, 2)

    return HttpResponse(f"Estimated Price: {esm1}, {esm2}, {esm3}, {esm4}")


def main(request):
    load_artifacts(request)
    return HttpResponse(get_price(request))


def get_location_names(request):
    if request.method == "GET":
        load_saved_artifacts()

        locations = get_locations()

        response_data = {"locations": locations}
        response = JsonResponse(response_data)
        response["Access-Control-Allow-Origin"] = "*"

        return response

    return JsonResponse({"error": "Invalid request method"})


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def predict_home_price(request):
    if request.method == "POST":
        # Handle POST request
        total_sqft = float(request.POST.get("total_sqft"))
        location = request.POST.get("location")
        bhk = int(request.POST.get("bhk"))
        bath = int(request.POST.get("bath"))

        # load_artifacts(request)
        estimated_price = get_estimated_price(location, total_sqft, bhk, bath)

        response_data = {"estimated_price": estimated_price}
        return JsonResponse(response_data)

    return JsonResponse({"error": "Invalid request method"})

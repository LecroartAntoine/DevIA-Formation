from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpResponse
import random, io, urllib.request, json, os
from PIL import Image



def random_gen(request):

    values = request.GET 

    if 'nb' in values.keys(): 
        if values['nb'].isnumeric():
            nb = int (values['nb']) 
            data = {'result' : random.sample(range(-1000,1001), nb)}
            return JsonResponse(data)
        else:
            return HttpResponse("Mauvaise requête")
    
    else:
        return HttpResponse(random.randint(0, 101))
    


def somme(request):

    values = request.GET

    if 'n1' in values.keys() and 'n2' in values.keys():

        if values['n1'].isnumeric() and values['n2'].isnumeric():
            n1 = int (values['n1'])
            n2 = int (values['n2'])
            return HttpResponse(n1+n2)
        
        else:
            return HttpResponse("Mauvaise Requête")
        
    else:
        return HttpResponse("Mauvaise Requête")
    


def produit(request):

    values = request.GET

    if 'n1' in values.keys() and 'n2' in values.keys():
        if values['n1'].isnumeric() and values['n2'].isnumeric():
            n1 = int (values['n1'])
            n2 = int (values['n2'])
            return HttpResponse(f"{n1} x {n2} = {n1*n2}")
        
        else:
            return HttpResponse("Mauvaise Requête")
        
    else:
        return HttpResponse("Mauvaise Requête")
    



def show_img(request):

    values = request.GET

    if 'num' in values.keys():
        if values['num'].isnumeric() and 1 <= int(values['num']) <= 9:

            url = f"https://www.juleshaag.fr/devIA/devAPI/{values['num']}"

            with urllib.request.urlopen(url) as u:
                img_data = u.read()

            img = Image.open(io.BytesIO(img_data))

            response = HttpResponse(content_type="image/png")

            img.save(response, "PNG")

            return response
        
        else:
            return HttpResponse("Mauvaise Requête")
        
    else:
        return HttpResponse("Mauvaise Requête")
    


def info_station(request):

    url = 'https://www.juleshaag.fr/devIA/devAPI/station_information.json'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    values = request.GET

    if 'id' in values.keys():
        if values['id'].isnumeric():

            for station in data['data']['stations']:
                if station['station_id'] == values['id']:

                    if 'addr' in values.keys() and 'cap' in values.keys():
                        return HttpResponse(f"Adresse : {station['address']}</br>Capacité : {station['capacity']}")

                    elif 'addr' in values.keys():
                        return HttpResponse(station['address'])
                    
                    elif 'cap' in values.keys():
                        return HttpResponse(station['capacity'])
                    
                    else:
                        return JsonResponse(station)
            
            return HttpResponse("Station non-existante")
        
        elif values['id'] == 'toutes' and 'cap' in values.keys():

            capacity = 0

            for station in data['data']['stations']:
                capacity += station['capacity']
            
            return HttpResponse(capacity)

        else:
            return HttpResponse("Mauvaise Requête")
        
    else:
        return HttpResponse("Mauvaise Requête")
    


def info_station_option(request, id, option):

    url = 'https://www.juleshaag.fr/devIA/devAPI/station_information.json'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    for station in data['data']['stations']:
        if station['station_id'] == str(id):

            if option == "addr":
                return HttpResponse(station['address'])
            
            elif option == "cap":
                return HttpResponse(station['capacity'])
            
            else:
                return HttpResponse('Mauvaise Requête')
            
    return HttpResponse("Station non-existante")



def info_station_somme(request):
    url = 'https://www.juleshaag.fr/devIA/devAPI/station_information.json'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    capacity_all = 0
    result = {}

    for station in data['data']['stations']:
        result[station['station_id']] = {"Capacité" : station['capacity']}
        capacity_all += station['capacity']

    result["Capacité totale"] = capacity_all
    
    return JsonResponse(result)



def index(request):
    with open (os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index.html'), encoding = 'utf-8') as file:
        page = file.read()
    return HttpResponse(page)
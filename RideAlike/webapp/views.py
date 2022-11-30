from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import register,uploadCar,uploadVIN
from exif import Image
import geopy.distance
import torch
import easyocr
import requests,json
from . import use_model
import os


# Create your views here.
def vin_decoder(vin_number): # VIN Decoder
    url = 'https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVINValuesBatch/'
    post_fields = {'format': 'json', 'data':vin_number}; # available return format: xml, csv, json
    r = requests.post(url, data=post_fields)
    rlt = json.loads(r.text)
    return rlt


def precheck(img):
    model = torch.hub.load('ultralytics/yolov5', 'yolov5m')
    #model = torch.load('yolov5\yolov5m.pt')
    # Inference
    results = model(f"media/{img}")
    return results


def extract_vin(img):
    reader = easyocr.Reader(['en'])
    output = reader.readtext(f"media/{img}")
    text = ''
    for i in range(len(output)):
        text = text + output[i][1]
    return(text)

def ocr_space_file(filename, overlay=False, api_key='K88251780688957', language='eng'):
    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               }

    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()


def decimal_degrees(coordinate, ref): # To convert the coordinate to decimal degree
            """
                :param coordinate(list): coordinate[0] degrees, coordinate[1] minutes, coordinate[2] seconds
                :param ref(string): direction
                :returns decimal_degrees(float): decimal degrees
            """
            decimal_degrees = coordinate[0] + coordinate[1]/60 + coordinate[2]/3600
            # Latitude (Equator), Longtitude (Prime Meridian)
            if ref == "S" or ref == "W":
                decimal_degrees = -decimal_degrees
            return decimal_degrees

def vin_extract(img):
    headers = {"X-Api-Key": 'hzotFcvpxYYFl2LG1Z5sqw==xCzcuEHFZ0PblDMo', 'Access-Control-Allow-Origin': '*'}
    api_url = 'https://api.api-ninjas.com/v1/imagetotext'

    image_file_descriptor = open(f"media/{img}", 'rb')
    files = {'image': image_file_descriptor}
    r = requests.post(api_url, files=files, headers=headers)
    vin = r.json()
    return vin
    
def find_classes(dir):
        classes = os.listdir(dir)
        classes.sort()
        class_to_idx = {classes[i]: i for i in range(len(classes))}
        return classes, class_to_idx

def homepage(request):
    return render(request,'website/index.html',{})

def Register(request):
    if request.method == 'POST':
        uname = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        re_password = request.POST.get('re_pass')
        phone = request.POST.get('phone')
        now = datetime.now()
        is_created_date = now.strftime("%d/%m/%Y")
        is_created_time = now.strftime("%H:%M:%S")
        if password==re_password:
            if User.objects.filter(username = email).exists():
                messages.info(request,"User Exits")
                return redirect('signup')
            else:
                add_user = User.objects.create_user(username=email,first_name= uname,password=password)
                add_user.email = email
                # add_user.is_created_date = is_created_date
                # add_user.is_created_time = is_created_time
                # add_user.phone = phone
                add_user.save()
                user = register(uname=uname, email=email,phone=phone,is_created_date=is_created_date,is_created_time=is_created_time)
                user.save()
                print('user created')
        else:
            messages.info(request,"password dose not match")
            return redirect('signup')
        return redirect('/signin/')
    else:
        return render(request,'website/register.html')
    #return render(request,'website/register.html',{})

def ulogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        cuser= authenticate(username=email,password=password)
        if cuser is not None:
            login(request,cuser)
            return redirect('/')
        else:
            messages.info(request,"Error..! User not registered")
            return redirect('signin')
    else:
        return render(request,'website/signin.html',{})

def ulogout(request):
    logout(request)
    return redirect('/')

@login_required(redirect_field_name='/signin/')
def upload(request):
    if request.method == 'POST':
        carPhoto = request.FILES['carPhoto']
        vinPhoto = request.FILES['vinPhoto']
        car = uploadCar(carImage=carPhoto)
        vin = uploadVIN(vinImage=vinPhoto)
        car.uname = request.user
        vin.uname = request.user
        car.save()
        vin.save()
        #TODO implement precheck
        pathlist_car = uploadCar.objects.values('carImage')
        element_car = len(pathlist_car)
        path_car = (list(pathlist_car[element_car-1].values())[0])
        # car_precheck = precheck(f"{path_car}")
        # car_precheck = car_precheck.tolist()
        # if 'car' in str(car_precheck[0]):
        #     print(car_precheck)
        # else:
        #     print("error")
        #     print(car_precheck)
        #     context = {"error": "Please upload Picture of Car"}
            #return render(request,'website/upload.html',context)

        #TODO uncomment for geolocation and timestamp
        try:
            car_image = Image(carPhoto)
            vin_image = Image(vinPhoto)
        except:
            print("Please upload photos again")
            return render(request,'website/upload.html',{})
        if car_image.has_exif:
            car_image_latitude = decimal_degrees(car_image.gps_latitude,  car_image.gps_latitude_ref)
            car_image_longtitutude = decimal_degrees(car_image.gps_longitude, car_image.gps_longitude_ref)
            car_image_datetime =  car_image.datetime_original
            # print(car_image_datetime,car_image_latitude,car_image_longtitutude)
        else:
            print("Car image has no exif")
            return render(request,'website/upload.html',{})
            

        if vin_image.has_exif:
            vin_image_latitude = decimal_degrees(vin_image.gps_latitude,  vin_image.gps_latitude_ref)
            vin_image_longtitutude = decimal_degrees(vin_image.gps_longitude, vin_image.gps_longitude_ref)
            vin_image_datetime =  vin_image.datetime_original
            # print(vin_image_datetime,vin_image_latitude,vin_image_longtitutude)
        else:
            messages.info(request,"Error..! Please Use Geo-location enabled Camera.")
            return redirect('/upload/')
            #print("VIN image no exif")
            #return render(request,'website/upload.html',{})
        
        car_cordinate = (car_image_latitude,car_image_longtitutude)
        vin_cordinate = (vin_image_latitude,vin_image_longtitutude)
        dist = geopy.distance.geodesic(car_cordinate, vin_cordinate).meters
        if dist <=100 :
            pass
        else:
            print(dist)
            messages.info(request,"Error..! Please Capture image from same location.")
            return redirect('/upload/')
            # print("Error while checking the dist")
            # return render(request,'website/upload.html',{})

        pathlist_vin = uploadVIN.objects.values('vinImage')
        element_vin = len(pathlist_vin)
        path_vin = (list(pathlist_vin[element_vin-1].values())[0])
        
        try:
            test_file = ocr_space_file(filename=f'media/{path_vin}', language='eng')
            result = json.loads(test_file)['ParsedResults']
            vin_number = result[0]["ParsedText"].strip()
            print(vin_number)
            vin_details = vin_decoder(vin_number)
            #vin_details = vin_decoder('2HGFB2F54CH020773')
            vinmake = vin_details['Results'][0]['Make']
            vinmodel = vin_details['Results'][0]['Model']
            vinyear = vin_details['Results'][0]['ModelYear'] 
        except:
            messages.info(request,"Error..! Please upload VIN Image again.")
            return redirect('/upload/')
            #print("error uwhile extracting VIN", vin_number)
        
        
        conf, car_prediction = use_model.getResults(f"media/{path_car}")
        classes, c_to_idx = find_classes("train")
        # if car_prediction:
        final_list = (classes[car_prediction[0]]).split(" ")
        try:
            car_make = final_list[0]
            car_model = " ".join(final_list[1:-1])
            car_year = final_list[-1]
        except:
            messages.info(request,"Error..! Please upload Car Image again.")
            return redirect('/upload/')
        try:
            contex = {"carMake": car_make, "carModel":car_model, "carYear": car_year,
                        "vinMake":vinmake, "vinModel": vinmodel, "vinYear": vinyear }
            if car_make.upper()== vinmake.upper():
                if vinmodel.upper() in car_model.upper():
                    if vinyear == car_year:
                        return render(request,'website/successfulPage.html',contex)
                    else:
                        return render(request,'website/unsuccessfulPage.html',contex)
                else:
                    return render(request,'website/unsuccessfulPage.html',contex)
            else:
                return render(request,'website/unsuccessfulPage.html',contex)

        except:
            return redirect("/upload/")

            

        #return redirect('/')




    #pass
    return render(request,'website/upload.html',{})
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import User, Clothes
import re
from django.contrib import messages
import bcrypt
from django.db.models import Q
from datetime import date

def index(request):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        return render (request, "mycloset/dashboard.html")

def register(request):
	if request.method == "POST":
		User.objects.register(request)
		return redirect("/")
	else:
		return redirect("/")

def login(request):
    try:
        user = User.objects.get ( email=request.POST["email"] )

        isValid = bcrypt.checkpw( request.POST["password"].encode() , user.password.encode() )
        
        if isValid:
            print ("Password match!")
            request.session['name'] = user.name
            request.session['email'] = user.email
            request.session['user_id'] = user.id
            return redirect ("/dashboard")

        else:
            print ("Passwords do NOT match!")
            messages.add_message (request, messages.ERROR, "Invalid Credentials!")
            return redirect("/")
        
    except:
        messages.add_message (request, messages.ERROR, "No user with this email found!")
        return redirect("/")

def dashboard(request):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        currentuserid = request.session['user_id']
        cleanclothes = Clothes.objects.filter(clean=True)
        return render (request, "mycloset/dashboard.html", {
            "cleanclothes": cleanclothes,
        })

def add(request):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        return render (request, "mycloset/add.html")

def createitem(request):
    today = str(date.today())

    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        if request.method == "POST":
            if len(request.POST["weather"]) < 1:
                messages.add_message( request, messages.ERROR, "You must select at least one weather option!" )
                return redirect("/add")
            else:
                item = Clothes.objects.create(
                    mainType = request.POST["type"],
                    subType = request.POST["subtype"],
                    color = request.POST["color"],
                    pattern = request.POST["pattern"],
                    fanciness = request.POST["fanciness"],
                    weather = request.POST["weather"],
                    clean = True,
                    favorite = False,
                    item_creator_id = request.session['user_id'],
                )

                messages.add_message( request, messages.ERROR, "Your item has been added!" )
                return redirect("/dashboard")
        else:
            return redirect("/add")

def showitem(request, id):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        trip = Trip.objects.get(id=id) 
        context= {
            "trip": trip,
            'travelers': User.objects.filter(trip_travelers__id=id),
        }
        return render (request, "mycloset/showtrip.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")
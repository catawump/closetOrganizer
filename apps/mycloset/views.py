from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect, reverse
from .models import User, Clothes, Outfit
import re
from django.contrib import messages
import bcrypt
from django.db.models import Q
from datetime import date

def index(request):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        return redirect("/dashboard")

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
        cleanclothes = Clothes.objects.filter(Q(clean = True) & Q(favorite = False) & Q(item_creator_id = request.session['user_id']))
        favclothes = Clothes.objects.filter(Q(clean = True) & Q(favorite = True) & Q(item_creator_id = request.session['user_id']))
        return render (request, "mycloset/dashboard.html", {
            "cleanclothes": cleanclothes,
            "favclothes": favclothes,
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
            if request.POST["subtype"] == "no":
                messages.add_message( request, messages.ERROR, "You must select an item type and subtype!" )
                return redirect("/add")
            if len(request.POST["description"]) < 1:
                messages.add_message( request, messages.ERROR, "You must describe the item!" )
                return redirect("/add")
            else:
                item = Clothes.objects.create(
                    mainType = request.POST["type"],
                    subType = request.POST["subtype"],
                    color = request.POST["color"],
                    pattern = request.POST["pattern"],
                    fanciness = request.POST["fanciness"],
                    weather = request.POST["weather"],
                    description = request.POST["description"],
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

def wearitem(request, id):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        item = Clothes.objects.get(id=id)
        item.clean = False
        item.save()
        messages.add_message( request, messages.ERROR, "You have worn this item and it is now dirty." )
        return redirect('/dashboard')

def laundry(request):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        currentuserid = request.session['user_id']
        dirtyclothes = Clothes.objects.filter(Q(clean=False) & Q(item_creator_id = currentuserid))
        return render (request, "mycloset/laundry.html", {
            "dirtyclothes": dirtyclothes,
        })

def washitem(request, id):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        item = Clothes.objects.get(id=id)
        item.clean = True
        item.save()
        messages.add_message( request, messages.ERROR, "You have laundered this item and it is now clean." )
        return redirect('/laundry')

def washall(request):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        dirtyclothes = Clothes.objects.filter(Q(clean=False) & Q(item_creator_id = request.session['user_id']))
        for item in dirtyclothes:
            item.clean = True
            item.save()
        messages.add_message( request, messages.ERROR, "You have done all your laundry! Nice!" )
        return redirect('/laundry')

def viewitem(request, id):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        item = Clothes.objects.get(id=id) 
        context= {
            "item": item,
        }
        return render (request, "mycloset/viewitem.html", context)

def manage(request):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        currentuserid = request.session['user_id']
        allclothes = Clothes.objects.filter(item_creator_id = currentuserid)
        return render (request, "mycloset/manage.html", {
            "allclothes": allclothes,
        })

def favitem(request, id):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        item = Clothes.objects.get(id=id)
        if item.favorite == False:
            item.favorite = True
            item.save()
        else:
            item.favorite = False
            item.save()
        return redirect('/manage')

def delete(request, id):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        currentuserid = request.session['user_id']
        item = Clothes.objects.get(id=id)
        print item.color
        print item.outfit_top.name
        #if item.outfit_top.id == id:
            #messages.add_message( request, messages.ERROR, "You cannot delete an item that is part of an outfit!" )
            #return redirect('/manage')
        #Clothes.objects.get(id=id).delete()
        return redirect('/manage')

def deleteoutfit(request, id):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        currentuserid = request.session['user_id']
        Outfit.objects.get(id=id).delete()
        return redirect('/outfits')

def outfits(request):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        currentuserid = request.session['user_id']
        clothes = Clothes.objects.filter(item_creator_id = currentuserid)
        outfits = Outfit.objects.filter(outfit_creator_id = currentuserid)
        return render (request, "mycloset/outfits.html", {
            "clothes": clothes,
            "outfits": outfits,
        })

def addoutfit(request):
    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        currentuserid = request.session['user_id']
        tops = Clothes.objects.filter(Q(mainType = "Top") & Q(item_creator_id = currentuserid))
        bottoms = Clothes.objects.filter(Q(mainType = "Bottom") & Q(item_creator_id = currentuserid))
        fullbodys = Clothes.objects.filter(Q(mainType = "Full-Body") & Q(item_creator_id = currentuserid))
        shoes = Clothes.objects.filter(Q(mainType = "Shoes") & Q(item_creator_id = currentuserid))
        accessories = Clothes.objects.filter(Q(mainType = "Accessory") & Q(item_creator_id = currentuserid))
        return render (request, "mycloset/addoutfit.html", {
            "tops": tops,
            "bottoms": bottoms,
            "fullbodys": fullbodys,
            "shoes": shoes,
            "accessories": accessories,
        })

def createoutfit(request):
    today = str(date.today())

    if 'name' not in request.session:
        return render (request, "mycloset/index.html")
    else:
        if request.method == "POST":
            if request.POST["top"] == "no" or request.POST["bottom"] == "no" or request.POST["shoes"] == "no" or request.POST["accessory"] == "no":
                messages.add_message( request, messages.ERROR, "You must select an item for every field!" )
                return redirect("/addoutfit")
            if len(request.POST["name"]) < 1:
                messages.add_message( request, messages.ERROR, "You must name your outfit!" )
                return redirect("/addoutfit")
            else:
                outfit = Outfit.objects.create(
                    name = request.POST["name"],
                    outfit_creator = User.objects.get(id=request.session['user_id']),
                )

                outfitnew = Outfit.objects.get(id=outfit.id)
                top = Clothes.objects.get(id = request.POST["top"])
                outfitnew.top.add(top)
                outfitnew.save()
                bottom = Clothes.objects.get(id = request.POST["bottom"])
                outfitnew.bottom.add(bottom)
                outfitnew.save()
                shoe = Clothes.objects.get(id = request.POST["shoes"])
                outfitnew.shoes.add(shoe)
                outfitnew.save()
                accessory = Clothes.objects.get(id = request.POST["accessory"])
                outfitnew.accessory.add(accessory)
                outfitnew.save()
              
                messages.add_message( request, messages.ERROR, "Your outfit has been added!" )

                return redirect("/outfits")
        else:
            return redirect("/addoutfit")


def logout(request):
    request.session.clear()
    return redirect("/")
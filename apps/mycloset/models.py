from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
import re
import bcrypt

#Email validation REGEX

emailREGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

#Class that validates user creation and creates a new user, if all validation passes. Also contains login validation, but we did that in the views file instead.

class userManager(models.Manager):
    def register(self,request):

        if len(request.POST["name"]) < 1:
			messages.add_message( request, messages.ERROR, "Name is required!" )
        if len(request.POST["email"]) < 1:
			messages.add_message( request, messages.ERROR, "Email is required!" )
        if len(request.POST["city"]) < 1:
			messages.add_message( request, messages.ERROR, "City is required!" )
        if not emailREGEX.match( request.POST["email"] ):
			messages.add_message( request, messages.ERROR, "Invalid email format! Ex: test@test.com" )
        if len(request.POST["password"]) < 8:
			messages.add_message( request, messages.ERROR, "Password must be between 8-32 characters!" )
        if request.POST["password"] != request.POST["confirm_password"]:
			messages.add_message( request, messages.ERROR, "Password and Password Confirmation must match!" )
        if User.objects.filter(email=request.POST["email"]).count() > 0:
			messages.add_message( request, messages.ERROR, "A user with this email already exists!" )
#If there are error messages at the end, return false.
        if len(get_messages(request)) > 0:
            return False
#Else, create the user and hash the password.
        else:

            User.objects.create(
                name = request.POST["name"],
                email = request.POST["email"],
                city = request.POST["city"],
                password = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
            )
            messages.add_message( request, messages.ERROR, "Your account has been created! Please log in." )
            return True

    def login(self,request):
        pass

#User Model

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    objects = userManager()

#Clothes Model

class Clothes(models.Model):
    mainType = models.CharField(max_length=255)
    subType = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    weather = models.CharField(max_length=255)
    fanciness = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    clean = models.BooleanField()
    favorite = models.BooleanField()
    pattern = models.CharField(max_length=255)
    item_creator = models.ForeignKey(User, related_name="user_clothes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

#Outfit Model

class Outfit(models.Model):
    name = models.CharField(max_length=255)
    top = models.ForeignKey(Clothes, related_name="outfit_top")
    bottom = models.ForeignKey(Clothes, related_name="outfit_bottom")
    shoes = models.ForeignKey(Clothes, related_name="outfit_shoes")
    accessory = models.ForeignKey(Clothes, related_name="outfit_accessory")
    outfit_creator = models.ForeignKey(User, related_name="user_outfits")

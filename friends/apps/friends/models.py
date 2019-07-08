from __future__ import unicode_literals
from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt
from datetime import date, datetime

class UserManager(models.Manager):
    def basic_validator(self, form_data):
        errors = {}

        # Name
        if len(form_data['name']) < 2:
            errors['name'] = "Name must be atleast two characters long"
        if not re.match (r'^[a-zA-Z]+$', form_data['name']):
            errors['name_2'] = "Name must only contain letters."

        # Alias
        if len(form_data['alias']) < 2:
            errors['alias_2']="Alias must be atleast two characters long"
        if not re.match (r'^[a-zA-Z]+$', form_data['alias']):
            errors['Alias'] = "Alias must only contain letters."

        # Password
        if len(form_data['password']) < 8:
            errors['password'] = "password must be at least eight characters long"

        # Email
        if not re.match (r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', form_data['email']):
            errors['email'] = "Must enter a valid email."

        # Password Confirmation
        if form_data['password'] != form_data['confirm_password']:
            errors['confirm_password']= "Password and confirmation password must match"

        # Date of Birth
        if not datetime.strptime(form_data['dob'], '%Y-%m-%d') <= datetime.now():
            errors['date']= "Date of birth cannot be in the future."


        return errors;


    def login_validator(self, form_data):
        errors= {}

        # Email
        if len(form_data['email']) < 1:
            errors['email'] = "Email cannot be blank"

        # Password
        if len(form_data['password']) < 1:
            errors['password'] = "Password cannot be blank"

        if len(errors) < 1:
            user= User.objects.filter(email=form_data['email'])
            print user

        if len(user)<1:
                errors['login'] = "Please register."
                return errors;

        obtain_hash =User.objects.get(email=form_data['email']).password
        print obtain_hash

        form_password = bcrypt.hashpw(form_data['password'].encode(), bcrypt.gensalt())
        if not bcrypt.checkpw(form_data['password'].encode(), obtain_hash.encode()):
            errors['password_1'] = "Invalid password."

        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    confirm_password= models.CharField(max_length=255)
    dob = models.DateField()
    created_at= models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()




class Friend(models.Model):
    user= models.ForeignKey(User, related_name="user_id")
    friend= models.ForeignKey(User, related_name="friend_id")
    created_at= models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    # objects = FriendManager()

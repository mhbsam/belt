from __future__ import unicode_literals
from django.db import models
import bcrypt
import re



class UserManager(models.Manager):
    def validator(self, first_name, last_name, email, password, confirm_password):
        error_list=[]
        valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$', re.MULTILINE)

        if len(first_name) <2:
            error_list.append('First name should have atleast two letters!')
            valid = False
        if not first_name.isalpha():
            error_list.append('First name should only contain letters!')
            valid = False

        if len(last_name) < 2:
            error_list.append('Last name should have atleast two letters!')
            valid = False
        if not last_name.isalpha():
            error_list.append('Last name should only contain letters!')
            valid = False

        if len(password) < 8:
            error_list.append('Password should be atleast 8 characters!')
            valid = False
        if not PASSWORD_REGEX.match(password):
            error_list.append('Password must contain one uppercase lettter, one lowercase, one number, and one special character!')
            valid = False
        if (password)!=(confirm_password):
            error_list.append('Passwords do not match!')
            valid = False

        if not EMAIL_REGEX.match(email):
            error_list.append('Invalid email address!')
            valid = False

        if User.objects.filter(email=email):
            error_list.append('Email already exists!')
            valid = False

        if not valid:
            return (False, error_list)

        pw_hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hashed )
        # print '---------> User Added Successfully! <-------------'
        return (True, new_user)


    def enter(self, email, password):
        user = User.objects.filter(email=email)
        error_list=[]

        if user:
            if email == user[0].email:
                pw_hashed_db = user[0].password
                if bcrypt.hashpw(password.encode(), pw_hashed_db.encode()) == pw_hashed_db:
                    return (True, user[0])

            error_list.append('email or password do not match')

        else:
            error_list.append('User do not exist!')

        return (False, error_list)



class User(models.Model):
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add= True)
    objects = UserManager()

# class Favorite(models.Model):
#     name = models.CharField(max_length=350)
#     rating = models.IntegerField()
#     user = models.ForeignKey(User)
#     book = models.ForeignKey(Book)
#     created_at = models.DateTimeField(auto_now_add= True)
#     updated_at = models.DateTimeField(auto_now= True)
#     objects = ReviewManager()

# class Favorite(models.Model):
#     name = models.CharField(max_length=250)
#     author = models.CharField(max_length=50)
#     created_at = models.DateTimeField(auto_now_add= True)
#     updated_at = models.DateTimeField(auto_now= True)
#     objects = BookManager()

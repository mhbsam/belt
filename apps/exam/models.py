from __future__ import unicode_literals
from django.db import models
import bcrypt
import re
import datetime
today = datetime.date.today
#========================================================
#              ******* User Manager *********
#========================================================
class UserManager(models.Manager):
    def validator(self, first_name, last_name, email, password, confirm_password, birthday):
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

        if not birthday:
            error_list.append('Birthday should be provided!')
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


#========================================================
#              ******* Appointment Manager *********
#========================================================
class AppointmentManager(models.Manager):
    def addtask(self, task, date, time, user):
        error_list=[]
        valid = True

        if task == "":
            error_list.append('Task can not be empty!')
            valid = False

        if not time:
            error_list.append('Time can not be empty!')
            valid = False

        if not date:
            error_list.append('Date can not be empty!')
            valid = False
        print date
        if date < today:
            error_list.append('only current and future dates are acceptable!')
            valid = False

        if not valid:
            return (False, error_list)

        new_task = Appointment.objects.create(task=task, date=date, time=time, user=user)
        return (True, new_task)

    def update(self, task_id, task, status, date, time):
        error_list=[]
        valid = True

        if task == "":
            error_list.append('Task can not be empty!')
            valid = False

        if not time:
            error_list.append('Time can not be empty!')
            valid = False

        if not date:
            error_list.append('Date can not be empty!')
            valid = False
        if date < today:
            error_list.append('only current and future dates are acceptable!')
            valid = False

        if not valid:
            return (False, error_list)

        app = Appointment.objects.get(id=task_id)
        app.task = task
        app.status = status
        app.date = date
        app.time = time
        app.save()
        return (True, self)


#========================================================
#              ******* Classes *********
#========================================================
class User(models.Model):
    first_name = models.CharField(max_length= 50)
    last_name = models.CharField(max_length= 50)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=300)
    birthday = models.DateField(default='1111-11-11')
    created_at = models.DateTimeField(auto_now_add= True)
    objects = UserManager()

class Appointment(models.Model):
    task = models.CharField(max_length=550)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=150, default='Pending')
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now= True)
    objects = AppointmentManager()

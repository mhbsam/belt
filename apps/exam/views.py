from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Appointment
import datetime


def index(request):
    return render(request, 'exam/index.html')


def appointments(request):
    if 'user_id' in request.session:
        today =datetime.date.today()
        user_list = User.objects.filter(id=request.session['user_id'])
        current_task_list = Appointment.objects.filter(user=user_list[0]).filter(date = today).order_by('-updated_at')
        future_task_list = Appointment.objects.filter(user=user_list[0]).filter(date__gt= today).order_by('created_at')
        if user_list:
            context = {
                'user': user_list[0],
                'currenttasks' :current_task_list,
                'futuretasks' : future_task_list,
                'today': today,
            }
            return render(request, 'exam/appointments.html', context)
    return redirect('/')  


#========================================================
#                 *** Registration ***
#========================================================
def registration(request):
    if request.method == "POST":
        first_name = request.POST['first_name'].lower()
        last_name = request.POST['last_name'].lower()
        email = request.POST['email'].lower()
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        birthday = request.POST['birthday']
        valid = User.objects.validator(first_name, last_name, email, password, confirm_password, birthday)

        if valid[0]:
            request.session['user_id'] = valid[1].id
            # messages.add_message(request, messages.INFO, 'Successfully Registered')
            return redirect('/appointments')

        for error in valid[1]:
            messages.add_message(request, messages.INFO, error)

    return redirect('/')


#========================================================
#                 *** Login ***
#========================================================
def login(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        password = request.POST['password']
        login_pack = User.objects.enter(email, password)

        if login_pack[0]:
            request.session['user_id'] = login_pack[1].id
            # messages.add_message(request, messages.INFO, 'Successfully logged in!')
            return redirect('/appointments')

        for error in login_pack[1]:
            messages.add_message(request, messages.INFO, error)

    return redirect('/')

#========================================================
#                 *** Logout ***
#========================================================
def logoff(request):
    request.session.flush()
    # User.objects.all().delete()
    return redirect('/')


#========================================================
#                 *** add an appointment ***
#========================================================
def addapp(request):
    task = request.POST['task']
    date = request.POST['date']
    time = request.POST['time']
    user = User.objects.filter(id = request.session['user_id'])[0]
    new_task = Appointment.objects.addtask(task, date, time, user)
    print '=========================> here new task<========================='

    if not new_task[0]:
        error_list = new_task[1]
        print error_list
        for error in error_list:
            messages.add_message(request, messages.INFO, error)
    return redirect('/appointments')

#========================================================
#                 *** delete an appointment ***
#========================================================
def delete(request, task_id):
    Appointment.objects.filter(id = task_id).delete()
    return redirect('/appointments')

#========================================================
#                 *** edit an appointment ***
#========================================================
def edit(request, task_id):
    appointment = Appointment.objects.filter(id = task_id)[0]
    context = {
        'appointment':appointment
    }
    if request.method == "POST":
        task = request.POST['task']
        status = request.POST['status']
        date = request.POST['date']
        time =request.POST['time']
        task_id = task_id
        update = Appointment.objects.update(task_id, task, status, date, time)
        if not update[0]:
            for error in update[1]:
                messages.add_message(request, messages.INFO, error)
                return render(request, 'exam/update.html', context)
        return redirect('/appointments')
    return render(request, 'exam/update.html', context)

#========================================================
#                 *** update an appointment ***
#========================================================

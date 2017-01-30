from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'exam/index.html')

def registration(request):
    if request.method == "POST":
        first_name = request.POST['first_name'].lower()
        last_name = request.POST['last_name'].lower()
        email = request.POST['email'].lower()
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        valid = User.objects.validator(first_name, last_name, email, password, confirm_password)

        if valid[0]:
            request.session['user_id'] = valid[1].id
            messages.add_message(request, messages.INFO, 'Successfully Registered')
            return redirect('/main')

        for error in valid[1]:
            messages.add_message(request, messages.INFO, error)

    return redirect('/')


def main(request):
    if 'user_id' in request.session:
        user_list = User.objects.filter(id=request.session['user_id'])
        if user_list:
            context = {
                'user_name': user_list[0].first_name,
            }
            return render(request, 'exam/success.html', context)
    return redirect('/')


def login(request):
    if request.method == "POST":
        email = request.POST['email'].lower()
        password = request.POST['password']
        login_pack = User.objects.enter(email, password)

        if login_pack[0]:
            request.session['user_id'] = login_pack[1].id
            messages.add_message(request, messages.INFO, 'Successfully logged in!')
            return redirect('/main')

        for error in login_pack[1]:
            messages.add_message(request, messages.INFO, error)

    return redirect('/')


def logoff(request):
    request.session.flush()
    return redirect('/')

import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.

def home(request):
    if not request.user.is_authenticated():
        return redirect('/brent/sign-in')

    if not request.user.has_perm('opentrv_sensor.view_measurement'):
        return redirect('/brent/user-permissions')
    
    today = datetime.date.today()
    today = datetime.datetime(today.year, today.month, today.day)
    tomorrow = today + datetime.timedelta(days=1)
    return render(request, 'brent/home.html', {
        'today': today.isoformat().replace('T', ' '),
        'tomorrow': tomorrow.isoformat().replace('T', ' ')
    })

def sign_in(request):
    context = {}
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if user.has_perm('opentrv_sensor.view_measurement'):
                    return redirect('/brent')
        else:
		    return redirect('/brent/user-permissions')
            else:
                return redirect('/brent/user-permissions')
        else:
            context['email'] = email
            context['errors'] = ['Unrecognised Email and Password']
            return render(request, 'brent/sign-in.html', context=context)

    if request.user.is_authenticated():
        if request.user.has_perm('opentrv_sensor.view_measurement'):
            return redirect('/brent')
        else:
            return redirect('/brent/user-permissions')
    return render(request, 'brent/sign-in.html')

def user_permissions(request):
#    logout(request)
#    return HttpResponse('This user does not have permission or deactivated to view this content, please contact an administrator')
    return render(request, 'brent/user-perm.html')
def sign_up(request):
    email = request.POST['email']
    password = request.POST['password']
    password_confirmation = request.POST['password-confirmation']
    try:
        assert password == password_confirmation, 'Password confirmation does not match'
        assert len(User.objects.filter(username=email)) == 0, 'This email address is already registered'
        User.objects.create_user(username=email, password=password)
    except Exception as e:
        context = {'sign_up_email': email, 'sign_up_errors': [str(e)]}
        return render(request, 'brent/sign-in.html', context)
    return redirect('/brent/user-permissions')

def sign_in_or_sign_up(request):
    if 'password-confirmation' in request.POST:
        return sign_up(request)
    return sign_in(request)

def logout_view(request):
    logout(request)
    return redirect('/brent/sign-in')

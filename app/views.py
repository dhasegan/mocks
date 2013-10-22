from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse

# Decorator to use built-in authentication system
from django.contrib.auth.decorators import login_required

# Used to create and manually log in a user
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate, hashers

from django.core.urlresolvers import reverse

# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator

# Used to send mail from within Django
from django.core.mail import send_mail

# Template shortcuts
from django.template import RequestContext, loader

import datetime
from mimetypes import guess_type
import json

from app.models import *
from app.forms import *

def getAvailableMockInterviews():
    items = []
    allitems = Interview.objects.filter(start__gte=datetime.datetime.now())
    for item in allitems:
        if not item.mockee:
            mocker = MUser.objects.filter(id = item.mocker.id)[0]
            date = item.start
            items.append( { 
                'mocker': mocker,
                'starttime': date,
                'endtime': date + datetime.timedelta(hours=1),
                'id': item.id,
                'price': item.price,
            })
    return sorted( items, key=lambda it:it['starttime'])

def getScheduledMockInterviews(user):
    items = []
    allitems = Interview.objects.filter(start__gte=datetime.datetime.now()-datetime.timedelta(hours=6))
    for item in allitems:
        if item.mockee == user or item.mocker == user:
            mocker = MUser.objects.filter(id = item.mocker.id)[0]
            date = item.start
            items.append( { 
                'mocker': mocker,
                'starttime': date,
                'endtime': date + datetime.timedelta(hours=1),
                'id': item.id,
                'description': item.description,
                'price': item.price,
            })
            if item.mockee:
                mockee = MUser.objects.filter(id = item.mockee.id)[0]
                items[-1]['mockee'] = mockee
    return sorted( items, key=lambda it:it['starttime'])

@login_required
def home(request):
    context = { 'page': 'home' }
    user = get_object_or_404(MUser, username=request.user.username)

    context['items'] = getAvailableMockInterviews()
    return render(request, 'pages/home.html', context)

@login_required
def schedule(request):
    context = { 'page': 'schedule' }
    user = get_object_or_404(MUser, username=request.user.username)

    context['items'] = getScheduledMockInterviews(user)
    return render(request, 'pages/schedule.html', context)

@login_required
def createslot(request):
    context = { 'page': 'createslot' }
    user = get_object_or_404(MUser, username=request.user.username)
    if not user.isMocker:
        return render(request, 'pages/createslot.html', context)
    context['form_submit'] = 'createslot'
    context['form_button'] = 'Create'

    if request.method == 'GET' or request.method != 'POST':
        form = CreateSlotForm()
        context['form'] = form
        return render(request, 'pages/createslot.html', context)

    form = CreateSlotForm(request.POST)

    if not form.is_valid():
        context['form'] = form
        return render(request, 'pages/createslot.html', context)

    mockInterview = Interview(mocker=user, start=form.cleaned_data['datetime'],
            description=form.cleaned_data['description'], price=form.cleaned_data['price'])
    mockInterview.save()

    return redirect('/schedule')

@login_required
def scheduleInterview(request, interviewId):
    context = { 'page': 'home', }
    errors = []

    item = get_object_or_404(Interview, id=interviewId)
    mocker = get_object_or_404(MUser, id=item.mocker.id)
    mockee = get_object_or_404(MUser, id=request.user.id)
    date = item.start

    mockitem = {
        'mocker': mocker,
        'starttime': date,
        'endtime': date + datetime.timedelta(hours=1),
        'id': item.id,
        'description': item.description,
        'price': item.price,
    }
    context['item'] = mockitem
    if mocker.id == mockee.id:
        errors.append("You cannot schedule an interview with yourself")
    if item.mockee:
        errors.append("Someone else just scheduled this interview")
    if errors:
        context['errors'] = errors
        return render(request, 'pages/scheduleInterview.html', context)

    if not request.method == "POST":
        return render(request, 'pages/scheduleInterview.html', context)

    item.mockee = mockee
    item.save()

    context['success'] = "The interview is scheduled! Please talk to your interviewer before the interview time about details on how to talk and what to prepare."
    return render(request, 'pages/scheduleInterview.html', context)

@login_required
def deleteInterview(request, interviewId):
    context = { 'page': 'schedule', }
    errors = []

    item = get_object_or_404(Interview, id=interviewId)
    mocker = get_object_or_404(MUser, id=item.mocker.id)
    if not item.mockee and mocker.id == request.user.id:
        item.delete()
        context['success'] = "Item was deleted. Next time please plan to stick to your schedule better."
        return render(request, 'pages/deleteInterview.html', context) 
    mockee = get_object_or_404(MUser, id=item.mockee.id)
    if (mocker.id == request.user.id) == (mockee.id == request.user.id):
        context['errors'] = ["You cannot interfere with this item."]
        return render(request, 'pages/deleteInterview.html', context) 
    date = item.start

    mockitem = {
        'mocker': mocker,
        'mockee': mockee,
        'starttime': date,
        'endtime': date + datetime.timedelta(hours=1),
        'id': item.id
    }
    context['item'] = mockitem
    context['form_submit'] = '/delete/' + interviewId
    context['form_button'] = 'Delete interview'
    context['no_button'] = True

    if request.method == 'GET':
        form = DeleteInterviewForm()
        context['form'] = form
        return render(request, 'pages/deleteInterview.html', context)

    form = DeleteInterviewForm(request.POST)

    if not form.is_valid():
        context['form'] = form
        return render(request, 'pages/deleteInterview.html', context)

    if mocker.id == request.user.id:
        item.delete()
        context['success'] = """Item was deleted from your schedule and your interviewees schedule.
            Let your interviewee know that you don't have the time to attend the mock interview by emailing him at: """ + mockee.email
    elif mockee.id == request.user.id:
        item.mockee = None
        item.save()
        context['success'] = """Item was deleted from your schedule. Next time please plan to stick to your schedule better. 
            Let your interviewer know that you don't have the time to attend the mock interview by emailing him at: """ + mocker.email
    return render(request, 'pages/deleteInterview.html', context)

@login_required
def profile(request):
    user = get_object_or_404(MUser, id=request.user.id)
    context= {'page': 'profile'}

    context['user'] = user

    return render(request, 'pages/profile.html', context)

@login_required
def profilechange(request):
    user = get_object_or_404(MUser, id=request.user.id)
    context= {'page': 'profile'}
    errors = []
    context['form_submit'] = '/profile-change'
    context['form_button'] = 'Change Profile Details'

    if request.method == 'GET':
        form = ProfileChangeForm(initial={
            'name': user.username,
            'skypeId': user.skypeId,
            'description': user.description,
            'isMocker': user.isMocker,
        })
        context['form'] = form
        return render(request, 'pages/profilechange.html', context)

    form = ProfileChangeForm(userid= request.user.id, data=request.POST)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'pages/profilechange.html', context)

    user.username = form.cleaned_data['name']
    user.skypeId = form.cleaned_data['skypeId']
    user.description = form.cleaned_data['description']
    user.isMocker = form.cleaned_data['isMocker']
    user.save()

    return redirect('/profile')

@login_required
def passwordchange(request):
    user = get_object_or_404(MUser, id=request.user.id)
    context= {'page': 'profile'}
    errors = []
    context['form_submit'] = '/password-change'
    context['form_button'] = 'Change Password'

    if request.method == 'GET':
        form = ProfileChangePasswordForm()
        context['form'] = form
        return render(request, 'pages/passwordchange.html', context)

    form = ProfileChangePasswordForm(user=user, data=request.POST)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'pages/passwordchange.html', context)

    user.set_password( form.cleaned_data['password'] )
    user.save()

    return redirect('/profile')

@login_required
def mlogout(request):
    if request.user:
        user = request.user
    logout(request)
    return redirect('/')

def mlogin(request):
    if request.user.is_authenticated():
        return redirect('/')
    context = { 'page': "login" }
    context['form_submit'] = 'login'
    context['form_button'] = 'Login'

    if request.method == 'GET':
        form = LoginForm()
        context['form'] = form
        return render(request, 'pages/login.html', context)

    form = LoginForm(request.POST)

    if not form.is_valid():
        context['form'] = form
        return render(request, 'pages/login.html', context)

    user = get_object_or_404(MUser, email= form.cleaned_data['email'])
    user = authenticate(username=user.username, password=form.cleaned_data['password'])
    login(request, user)

    return redirect('/')

def mregister(request):
    if request.user.is_authenticated():
        return redirect('/')
    context = { 'page': "register" }
    context['form_submit'] = 'register'
    context['form_button'] = 'Register'

    if request.method == 'GET' or not request.method == 'POST':
        form = RegisterForm()
        context['form'] = form
        context['form_submit'] = 'register'
        return render(request, 'pages/register.html', context)


    form = RegisterForm(request.POST)

    if not form.is_valid():
        context['form'] = form
        return render(request, 'pages/register.html', context)

    new_user = MUser.objects.create_user(
                        username=form.cleaned_data['name'],
                        password=form.cleaned_data['password'],
                        email=form.cleaned_data['email'],
                        description=form.cleaned_data['description'],
                        skypeId=form.cleaned_data['skypeId'],
                        isMocker=form.cleaned_data['isMocker'])
    new_user.is_active = False
    new_user.save()

    return sendConfirmationEmail(request, new_user, context)

def confirm_registration(request, emailId, token):
    if request.user.is_authenticated():
        return redirect('/')
    user = get_object_or_404(MUser, email=emailId)

    if not default_token_generator.check_token(user, token):
        raise Http404

    user.is_active = True
    user.save()

    return redirect('/login')

def about(request):
    context = {}
    if request.user.is_authenticated():
        context['basetemplate'] = "pages/loggedin.html"
    else:
        context['basetemplate'] = "pages/loggedout.html"
    return render(request, "pages/about.html", context)

def sendConfirmationEmail(request, new_user, context):
    token = default_token_generator.make_token(new_user)

    email_body = """
Welcome to Mocks, the place where you get mock interviews for free (for now at least) from other
students that want to give those interviews! We want everyone to have a registered email address to
keep the website secure and trustworthy. 

You registered with the name: %s

Please click the link below to verify your email address and complete the registration of your account:

  http://%s%s

Thanks,
Your friendly bot

P.S. DO NOT REPLY TO THIS MESSAGE
""" % ( new_user.username,
        request.get_host(),
        reverse('confirmEmail', args=(new_user.email.replace('@','%40'), token)))

    send_mail(subject="Verify your email address",
              message= email_body,
              from_email="donotreply.jacobsmocks@gmail.com",
              recipient_list=[new_user.email ])

    context['email'] = new_user.email
    return render(request, 'pages/emailconfirm.html', context)
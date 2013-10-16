from django.shortcuts import render, redirect
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

from datetime import datetime
from mimetypes import guess_type
import json

from app.models import *
from app.forms import *

@login_required
def home(request):
    # Sets up list of just the logged-in user's (request.user's) items
    context = { 'page': 'home' }
    user = GrumblrUser.objects.filter(username=request.user.username)[0]

    following = user.following.all()
    items = []
    items.extend(Grumblr.objects.filter(user=user))

    items = setGrumblrsContext(items, user)
    context['grumblrs'] = sorted(items, key=lambda gr:gr.date, reverse=True)
    context['grumblr_post'] = True
    context['thisuser'] = user
    return render(request, 'pages/index.html', context)

# @login_required
# def profile(request, username):
#     context = { 'page': 'profile' }
#     if (username == request.user.username):
#         context['page'] = 'ownprofile'
#     user = GrumblrUser.objects.filter(username=username)[0]
#     context['grumblruser'] = user

#     nr_following = len(user.following.all())
#     nr_followers = len(user.followers.all())
#     nr_dislikes = calculateDislikes(user)
#     context['aboutitems'] = [{'attr': 'Real Name', 'value': user.realname}, \
#                              {'attr': 'City', 'value': user.city}, \
#                              {'attr': 'Email', 'value': user.email}, \
#                              {'attr': 'Twitter', 'value': user.twitter}, \
#                              {'attr': 'Facebook', 'value': user.facebook}, ]
#     context['statsitems'] = [{'attr': 'Following', 'value': nr_following}, \
#                              {'attr': 'Followers', 'value': nr_followers}, \
#                              {'attr': 'Dislikes', 'value': nr_dislikes}, ]

#     if username == request.user.username:
#         context['statsitems'][0]['link'] = 'following'
#         context['statsitems'][1]['link'] = 'followers'

#     items = []
#     items.extend(Grumblr.objects.filter(user=user))
#     items = setGrumblrsContext(items, user)
#     context['grumblrs'] = sorted(items, key=lambda gr:gr.date, reverse=True)
#     context['thisuser'] = user
#     return render(request, 'pages/profile.html', context)

@login_required
def profile_change(request, username, attr):
    if (username != request.user.username):
        return redirect('/')
    context = {}
    errors = []
    user = GrumblrUser.objects.filter(username=username)[0]
    if request.method != 'POST':
        errors.append('Error processing the request!')
        return create_profile_edit_view(request, request.user, {'errors': errors})
    if not attr in request.POST or not request.POST[attr]:
        errors.append('No value provided!')
        return create_profile_edit_view(request, request.user, {'errors': errors})

    setattr(user, attr, request.POST[attr])
    user.save()

    return redirect('/user/' + username + '/edit/')

# @login_required
# def gr_logout(request):
#     if request.user:
#         user = request.user
#     logout(request)
#     return redirect('/')


# def gr_login(request):
#     if request.user:
#         user = request.user
#         if user.is_authenticated():
#             return redirect('/')
#     context = { 'page': 'login' }

#     if (request.method == 'GET'):
#         return render(request, 'pages/login.html', context)

#     users = GrumblrUser.objects.filter(username= request.POST['username'])
#     if len(users) != 1:
#         context['errors']= ["Invalid username and/or password!"]
#         return render(request, 'pages/login.html', context)
#     user = users[0]

#     username = request.POST['username']
#     password = request.POST['password']
#     user = authenticate(username=username, password=password)
#     if user is not None:
#         if user.is_active:
#             login(request, user)
#             return redirect('/')
#         else:
#             context['errors']= ["Your account may not be activated! Try checking your email!"]
#             return render(request, 'pages/login.html', context)
#     else:
#         context['errors']= ["Invalid username and/or password!"]
#         return render(request, 'pages/login.html', context)

# def gr_signup(request):

#     if request.user:
#         user = request.user
#         if user.is_authenticated():
#             return redirect('/')

#     context = { 'page': 'signup' }

#     if request.method == 'GET':
#         form = SignupForm()
#         context['form'] = form
#         return render(request, 'pages/signup.html', context)

#     form = SignupForm(request.POST, request.FILES)
#     context['form'] = form

#     if not form.is_valid():
#         errors = form.non_field_errors;
#         return render(request, 'pages/signup.html', context)

#     new_user = GrumblrUser.objects.create_user(
#                         username=form.cleaned_data['username'],
#                         password=form.cleaned_data['password'],
#                         email=form.cleaned_data['email'],
#                         city=form.cleaned_data['city'],
#                         twitter=form.cleaned_data['twitter'],
#                         facebook=form.cleaned_data['facebook'],
#                         realname=form.cleaned_data['realname'],
#                         picture=form.cleaned_data['picture'])
#     new_user.is_active = False
#     new_user.save()

#     token = default_token_generator.make_token(new_user)

#     email_body = """
# Welcome to the Grumblr!  Please click the link below to
# verify your email address and complete the registration of your account:

#   http://%s%s
# """ % (request.get_host(),
#        reverse('confirm', args=(new_user.username, token)))

#     send_mail(subject="Verify your email address",
#               message= email_body,
#               from_email="dhasegan@cs.cmu.edu",
#               recipient_list=[new_user.email])

#     context['email'] = form.cleaned_data['email']
#     return render(request, 'pages/needs-confirmation.html', context)


# def confirm_registration(request, username, token):
#     user = GrumblrUser.objects.filter(username=username)
#     if len(user) != 1:
#         raise Http404
#     user = user[0]

#     if not default_token_generator.check_token(user, token):
#         raise Http404

#     user.is_active = True
#     user.save()

#     return redirect('/login')
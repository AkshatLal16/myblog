from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.http import JsonResponse
from .forms import *
from .models import Profile
from django.contrib.auth.models import User
from django.views.generic import RedirectView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
import json
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt
from openforums.settings import CREATE_ACCOUNT_TOKEN
import requests
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import os

@api_view(['POST'])
def create_account(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	print(username, password)
	return HttpResponse(username)

def login(request):
	if request.method == 'POST':
		username_ = request.POST.get('username')
		password_ = request.POST.get('password')
		user = auth.authenticate(username=username_, password=password_)
		print(type(user))
		if user is not None:
			auth.login(request, user)
			return redirect('blog-home')
		else:
			req=  requests.post("https://hhword.website/crm/action/checkmoodleuserapi.php", data={"username": username_, "password": password_})
			response = req.json()
			if response['status']==True:
				password_ = make_password(password_)
				user_ = User.objects.create(username=username_, password=password_)
				auth.login(request, user_)
				return redirect('blog-home')
			else:
				messages.success(request, f'Error wrong username/password')
	return render(request, 'users/login.html')

def profile(request, username):
	posts = Story.objects.filter(author__username=username)
	user = Profile.objects.get(user__username=username)
	context = {
		'posts':posts,
		'user':user,
	}
	return render(request, 'users/profile.html', context)

def profile_claps(request, username):
	user = get_object_or_404(Profile, user__username=username)
	context = {
		'user':user,
	}
	return render(request, 'users/profile_claps.html', context)

def user_followers(request, username):
	user = get_object_or_404(Profile, user__username=username)
	context = {
		'user':user,
	}
	return render(request, 'users/user_followers.html', context)

def user_following(request, username):
	user = get_object_or_404(Profile, user__username=username)
	context = {
		'user':user,
	}
	return render(request, 'users/user_following.html', context)

@login_required
def add_story(request):
	if request.method == 'POST':
		form = AddStoryForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.date_posted = timezone.now()
			post.save()
			return redirect('show-story', username=request.user.username, slug=post.slug)
	else:
		form = AddStoryForm()
	return render(request, 'users/add_story.html', {'form':form})



def show_story(request, username, slug):
	context = {
		'genre': Genre.objects.get(title=Story.objects.get(slug=slug).category),
		'story': Story.objects.get(slug=slug),
		'response': Responses.objects.filter(story__slug=slug)
	}
	return render(request, 'users/show_story.html', context)

@login_required
def delete_story(request, username, slug):
	if request.method == 'POST':
		story = get_object_or_404(Story, slug=slug)
		story.delete()
		return redirect('profile', username=request.user.username)
	context = {
		'story': Story.objects.get(slug=slug)
	}
	return render(request, 'users/delete_story.html', context)

@login_required
def edit_story(request, username, slug):
	if request.user.username == username:
		if request.method == 'POST':
			form = AddStoryForm(request.POST, request.FILES, instance=Story.objects.get(slug=slug))
			if form.is_valid():
				post = form.save(commit=False)
				post.author = request.user
				post.date_posted = timezone.now()
				post.save()
				return redirect('show-story', username=username, slug=slug)
		else:
			form = AddStoryForm(instance=Story.objects.get(slug=slug))
	else:
		return redirect('show-story', username=username, slug=slug)
	context = {
				'form':form
			}
	return render(request, 'users/edit_story.html', context)



@login_required
def bookmarks(request):
	bookmarks_list = Profile.objects.get(user__username=request.user.username).bookmarks.all()
	return render(request, 'users/bookmarks.html', {'bookmarks_list':bookmarks_list})


@login_required
def profile_follow_toggle(request):
    if request.method == 'GET':
    	user_to_toggle = request.GET.get("username")
    	profile_ = Profile.objects.get(user__username=user_to_toggle)
    	user = request.user.profile
    	if user in profile_.followed_by.all():
    		user.follows.remove(profile_ )
    	else:
    		user.follows.add(profile_)
    	return HttpResponse(True)

@login_required
def bookmark_toggle(request):
    if request.method == 'GET':
    	story_to_toggle = request.GET.get("story")
    	story = Story.objects.get(slug=story_to_toggle)
    	user = request.user.profile
    	if story in user.bookmarks.all():
    		user.bookmarks.remove(story)
    	else:
    		user.bookmarks.add(story)
    	return HttpResponse(True)

@login_required
def like_toggle(request):
    if request.method == 'GET':
    	story_to_toggle = request.GET.get("story")
    	story = Story.objects.get(slug=story_to_toggle)
    	user = request.user.profile
    	if story in user.claps.all():
    		pass
    	else:
    		user.claps.add(story)
    	return HttpResponse(True)

@login_required
def response_claps_toggle(request):
    if request.method == 'GET':
    	response_to_toggle = request.GET.get("response")
    	response = Responses.objects.get(id=response_to_toggle)
    	user = request.user.profile
    	if response in user.response_claps.all():
    		pass
    	else:
    		user.response_claps.add(response)
    	return HttpResponse(True)


@login_required
def profile_edit(request):
	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES, instance=get_object_or_404(Profile, user=request.user))
		print(str(request.FILES['image']))
		if form.is_valid():
			profile = form.save(commit=False)
			profile.save()
			return redirect('profile', username=request.user.username)
	else:
		form = EditProfileForm(instance=get_object_or_404(Profile, user=request.user))
		context = {
			'form':form
		}
	return render(request, 'users/profile_edit.html', context)
    
def responses(request, username, slug):
	story = get_object_or_404(Story, slug=slug)
	responses = Responses.objects.filter(story__slug=slug)
	if request.method == 'POST':
		form = AddResponseForm(request.POST, request.FILES)
		if form.is_valid():
			response = form.save(commit=False)
			response.story = get_object_or_404(Story, slug=slug)
			response.writer = request.user
			response.save()
			return redirect('responses', username=username, slug=slug)
	else:
		form = AddResponseForm()
	context = {
		'story':story,
		'form':form,
		'responses': responses
	}
	return render(request, 'users/response.html', context)

@login_required
def response_delete(request, username, slug, id):
	response = Responses.objects.get(id=id)
	story = Story.objects.get(slug=slug)
	if request.method == 'POST':
		response.delete()
		return redirect('responses', username=username, slug=slug)
	context={
		'response':response,
		'story':story
	}
	return render(request, 'users/response_delete.html', context)

@login_required
def response_report(request, username, slug, id):
	current_user = request.user.first_name
	username_ = request.user.username
	response = Responses.objects.get(id=id)
	story = Story.objects.get(slug = slug)
	if request.method == 'POST':
		form = ReportForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = current_user+" as @"+username_
			post.response =  response
			post.story = story
			post.save()
			return redirect('responses', username=username, slug=slug)
	else:
		form = ReportForm()
	context = {
		'form': form,
		'story': story,
		'response': response
	}
	return render(request, 'users/response_report.html', context)

@login_required
def story_report(request, username, slug):
	current_user = request.user.first_name
	username_ = request.user.username
	story = Story.objects.get(slug = slug)
	if request.method == 'POST':
		form = ReportForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = current_user+" as @"+username_
			post.story = story
			post.save()
			return redirect('show-story', username=username, slug=slug)
	else:
		form = ReportForm()
	context = {
		'form': form,
		'story': story
	}
	return render(request, 'users/story_report.html', context)

# @login_required
# def report(request):
# 	reports = Report.objects.all().order_by('date_posted')
# 	form = ReportForm()
# 	if request.method == 'POST':





@csrf_exempt 
def create_account(request):
    if request.method == 'POST':
    	username_ = request.POST.get("username")
    	password_ = request.POST.get("password")
    	token_  = request.POST.get("token")

    	if token_== CREATE_ACCOUNT_TOKEN:

    		if  User.objects.filter(username=username_).exists():
    			return JsonResponse({"status": "200", "success": "true", "message": "User already exist."})
    		else:
    			User.objects.create(username=username_, password=password_)
    			return JsonResponse({"status": "200", "success": "true", "message": "User created successfully."})
    	else:
    		return JsonResponse({"status": "403", "success": "false", "message": "Unauthorised Access"})
    else:
    	return JsonResponse({"status": "403", "success": "false", "message": "Unauthorised Access"})
 	
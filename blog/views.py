from django.shortcuts import render,HttpResponse
from users.models import Profile
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from users.models import *
from blog.models import *
from django.db.models import Count

def home(request):
	homepage_ = HomepageData.objects.all().first()
	backup_st = HomepageData.objects.all().first().BACKUP_HOMEPAGE_STORY.all()
	context = {
		'homepage_story':homepage_.homepage_story.all(),
		'featured_story':homepage_.featured_story.all(),
		'popular_story':homepage_.popular_story.all(),
		'backup_story':backup_st
	}
	return render(request, 'blog/home.html', context)

def topics_list(request):
	genre = Genre.objects.all()
	genre_category = GenreCategory.objects.all()
	context = {
		'genre':genre,
		'genre_category': genre_category
	}
	return render(request, 'blog/topics_list.html', context)

def genre(request, title):
	genre_ = Genre.objects.get(title=title)
	genre = Genre.objects.all().order_by('?')[:5]
	story = Story.objects.filter(category=title).order_by('date_posted')
	popular_story = story.annotate(claps_count=Count('clapped_by')).order_by('-claps_count')
	context = {
		'genre_':genre_,
		'genre':genre,
		'story':story,
		'popular_story': popular_story
	}
	return render(request, 'blog/genre.html', context)

def search_result(request):
	query = request.GET.get('q')
	if query != None:
		story_query = Story.objects.filter(Q(title__icontains=query) |  Q(body__icontains=query))
		people = Story.objects.filter(Q(author__username__icontains=query) |  Q(author__first_name__icontains=query) |  Q(author__profile__bio__icontains=query) | Q(title__icontains=query) |  Q(body__icontains=query)).order_by('author__id').distinct()
		genre = Genre.objects.filter(Q(title__icontains=query) | Q(info__icontains=query) | Q(category__category__icontains=query))
		context = {
			'search_value': query,
			'story_query': story_query,
			'people':people,
			'genre':genre,
			'query':query
		}
		return render(request, 'blog/search_result.html', context)
	else:
		return render(request, 'blog/search_result.html', {'query':query})

def homepage_story5_backup(request):
	story = Story.objects.get(author__username='Akshat').first()
	return render(request, 'blog/snippet/homepage_story5.html', {'story':story})
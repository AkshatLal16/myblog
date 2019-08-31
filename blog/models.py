from django.db import models
from users.models import *
from django.shortcuts import render,HttpResponse

class HomepageData(models.Model):
	homepage_story = models.ManyToManyField(Story, related_name='st1', symmetrical=False, blank=True)
	BACKUP_HOMEPAGE_STORY = models.ManyToManyField(Story, related_name='bkp', symmetrical=False, blank=True)
	featured_story = models.ManyToManyField(Story, related_name='st2', symmetrical=False, blank=True)
	popular_story = models.ManyToManyField(Story, related_name='st3', symmetrical=False, blank=True)

	def __str__(self):
		return "HomepageData"
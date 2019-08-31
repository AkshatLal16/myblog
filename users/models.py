from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from markdown_deux import markdown
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from PIL import Image
from .choices import *
from django.urls import reverse

class GenreCategory(models.Model):
	category = models.CharField(max_length=100)

	def __str__(self):
		return self.category

class Genre(models.Model):
	category = models.ForeignKey(GenreCategory, on_delete=models.CASCADE, null=True)
	# category = models.CharField(max_length=100, choices=GENRE_CATEGORY, null=True)
	title = models.CharField(max_length=100)
	image = models.ImageField(default='default_genre.jpg', upload_to='genre_pics')
	info = models.TextField(blank=True)

	def __str__(self):
		return self.title

	def save(self, *args, **kwargs):
		super().save()

		img = Image.open(self.image.path)

		if img.height > 300 and img.width > 300:
			output_size = (300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)


class Story(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.CharField(max_length=1000)
	body = RichTextUploadingField(blank=True, null=True)
	category = models.CharField(max_length=100, null=True)
	date_posted = models.DateTimeField(default=timezone.now)
	slug = models.SlugField(max_length = 255, editable=False, unique=True, blank=True, allow_unicode=True)

	def save(self, *args, **kwargs):
		super(Story, self).save(*args, **kwargs)
		if not self.slug:
			self.slug = slugify(self.title) + "-" + str(self.id)
			self.save() 

	def __str__(self):
		return self.title+" by @"+self.author.username

def default_value():
	return None

class Responses(models.Model):
	story = models.ForeignKey(Story, on_delete=models.CASCADE)
	writer = models.ForeignKey(User, on_delete=models.CASCADE)
	body = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default_profile.png', upload_to='profile_pics')
	bio = models.TextField(blank = True)
	follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
	bookmarks = models.ManyToManyField(Story, related_name='bookmarked_by', symmetrical=False, blank=True)
	claps = models.ManyToManyField(Story, related_name='clapped_by', symmetrical=False, blank=True)
	response_claps = models.ManyToManyField(Responses, related_name='response_claps_by', symmetrical=False, blank=True)

	def filter_follow(request, self, *args, **kwargs):
		return request.user

	def __str__(self):
		return f'{self.user.username}'

	def save(self, *args, **kwargs):
		super().save()

		img = Image.open(self.image.path)

		if img.height > 200 and img.width > 200:
			output_size = (200,200)
			img.thumbnail(output_size)
			img.save(self.image.path)

	def get_absolute_url(self):
		return reverse('profile', kwargs={'str':self.user.username})

class Report(models.Model):
	response = models.ForeignKey(Responses, on_delete=models.CASCADE, null=True)
	story = models.ForeignKey(Story, on_delete=models.CASCADE, null=True)
	comment = models.TextField()
	user= models.CharField(max_length=100)
	date_posted =  models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.user+"'s complaint"
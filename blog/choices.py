from users.models import *

story_dict = {}

story = Story.objects.all()
for obj in story:
	story_dict[obj.title] = obj.title

STORY_CHOICES = tuple(story_dict.items())
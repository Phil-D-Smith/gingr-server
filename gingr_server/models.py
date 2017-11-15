from django.db import models

from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

# use auth class instead
"""
class User(models.Model):
	user_id = models.CharField(max_length=128, unique=True, primary_key=True)
	email = models.CharField(max_length=256, unique=True)
	password_hash = models.CharField(max_length=256)
	first_name = models.CharField(max_length=256, unique=True)
"""

class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=256, default=None)
	last_name = models.CharField(max_length=256, default=None)
	reg_date = models.DateTimeField(auto_now=False, auto_now_add=True)
	last_login = models.DateTimeField(auto_now=False, auto_now_add=False)
	dob = models.DateField(auto_now=False, auto_now_add=False, default=None, null=True)
	gender = models.CharField(max_length=32, default=None, null=True)
	hair = models.CharField(max_length=32, default=None, null=True)
	bio = models.CharField(max_length=256, default=None, null=True)
	photo = models.ImageField(upload_to='profile-photos/%s', default=None, null=True)
	latitude = models.DecimalField(max_digits=9, decimal_places=6, default=None, null=True)
	longitude = models.DecimalField(max_digits=9, decimal_places=6, default=None, null=True)

	min_age = models.IntegerField(default=18)
	max_age = models.IntegerField(default=100)
	max_distance = models.IntegerField(default=100)
	hair_pref = models.CharField(max_length=32, default=None, null=True)
	gender_pref = models.CharField(max_length=32, default=None, null=True)

	profile_complete = models.BooleanField(default=False)

	def __str__(self):
		return str(self.user)

# match decisions
class Decision(models.Model):
	decision_id = models.AutoField(unique=True, primary_key=True)
	origin_user_id = models.CharField(max_length=128)
	target_user_id = models.CharField(max_length=128)
	origin_user_choice = models.BooleanField(default=None)
	target_user_choice = models.BooleanField(default=None)

	def __str__(self):
		return self.decision_id

# successful matches
class Match(models.Model):
	match_id = models.AutoField(unique=True, primary_key=True)
	user_id_1 = models.CharField(max_length=128)
	user_id_2 = models.CharField(max_length=128)
	date_time = models.DateField(auto_now=False, auto_now_add=False)
	message_count = models.IntegerField()
	last_message = models.CharField(max_length=512)
	last_seen_user_1 = models.IntegerField()
	last_seen_user_2 = models.IntegerField()

	def __str__(self):
		return self.match_id

# all messages between all users
class Message(models.Model):
	message_id = models.AutoField(unique=True, primary_key=True)
	match_id = models.ForeignKey(Match)
	sender_id = models.CharField(max_length=128)
	message_number = models.IntegerField()
	date_time = models.DateField(auto_now=False, auto_now_add=False)
	message_body = models.CharField(max_length=512)

	def __str__(self):
		return self.message_id
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.utils.html import escape

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.views.decorators.csrf import csrf_exempt

from .models import UserProfile, Decision, Match, Message

import json, uuid, datetime
from math import sin, cos, sqrt, atan2

def index(request):
    return HttpResponse("Hello, index")

class Login:
	# login an existing user
	@csrf_exempt
	def login(request):
		# decode data
		data = json.loads(request.body.decode('utf-8'))

		email = escape(data['email'].lower())
		password = escape(data['password'])

		# get user_id for that email from db, if not, account does not exist
		user_check = User.objects.get(email=email)
		user_id = user_check.username

		# authentciate with django auth
		try:
			user = authenticate(username=user_id, password=password)
		except:
			user = None

		if user is not None:
			# authenticated, login and respond
			login(request, user)
			response = {'status': 'correct',
					'id': user_id};
		else:
			# not authenticated, email or password is incorrect
			response = {'status': 'error'};

		return JsonResponse(response)

	# signup a new user
	@csrf_exempt
	def signup(request):
		# decode data
		data = json.loads(request.body.decode('utf-8'))

		email = escape(data['email'].lower())
		password = escape(data['password'])
		#password_again = escape(data['password2'])
		first_name = escape(data['firstname'].title())
		last_name = escape(data['lastname'].title())

		# check if user exists
		try:
			check = User.objects.get(email=email)
		except:
			check = None
		# if it exists, respond with exist
		if check is not None:
			response = {'status': 'exist'}
			return JsonResponse(response)

		# generate a unique userID
		user_id = str(uuid.uuid1())
		# make user object from django auth
		user = User.objects.create_user(user_id, email, password)
		user.first_name = first_name
		user.last_name = last_name
		# save to db
		user.save()

		# make UserInfo object with more detail
		user_profile = UserProfile(	user=user, 
									first_name=first_name,
									last_name=last_name,
									reg_date=datetime.datetime.now(),
									last_login=datetime.datetime.now())
		# save to db
		user_profile.save()

		if user is not None:
			# authenticated, login and respond
			login(request, user)
			response = {'status': 'success',
						'id': user_id};
		else:
			# not authenticated, email or password is incorrect
			response = {'status': 'error'};

		# return response
		return JsonResponse(response)

	# veryify session data of logged in user
	@csrf_exempt
	def verify(request):
		# check if user already logged in
		data = json.loads(request.body.decode("utf-8"))
		user_id = escape(data['userID'])

		#authentciate by checking a row is present in db
		try:
			user_check = User.objects.get(username=user_id)
		except:
			user_check = None

		if user_check is not None:
			# authenticated
			response = {'status': 'success'}
		else:
			# not authenticated, email or password is incorrect
			response = {'status': 'error'}

		return JsonResponse(response)

	@csrf_exempt
	def logout(request):
		# check if user object is authenticated
		if request.user.is_authenticated():
			logout(request)
			respond = {'status': 'success'}
		else:
			# if not, return error
			response = {'status': 'denied'};

	# recover a lost password
	@csrf_exempt
	def recover(request):
		data = json.loads(request.body.decode("utf-8"))

		return JsonResponse(response)

class Matches:
	# load all eligible users
	@csrf_exempt
	def get_users(request):
		#decode data
		data = json.loads(request.body.decode('utf-8'))

		origin_user_id = escape(data['id'])
		limit = escape(data['limit'])
		offset = escape(data['offset'])
		user_lat = escape(data['latitude'])
		user_long = escape(data['longitude'])

		# if no location data, respond error, else convert to float
		if (user_lat == 'None' or user_long == 'None'):
			response = {'status': 'no-location'}
			return JsonResponse(response)
		else:
			user_lat = float(user_lat)
			user_long = float(user_long)

		# get user preferences from user info table
		try:
			user_pref = UserProfile.objects.get(user__username=origin_user_id)
		except:
			response = {'status': 'error'}
			return JsonResponse(response)

		# if no data, profile setup failure
		if (user_pref == None):
			response = {'status': 'no-data'}
			return JsonResponse(response)

		# testing
		print(user_lat)
		print(user_long)
		# preference calcs
		min_dob = datetime.datetime.now() - datetime.timedelta(days=user_pref.max_age*365)
		max_dob = datetime.datetime.now() - datetime.timedelta(days=user_pref.min_age*365)

		# calc a rough maximum to minimise how many profiles are loaded, then calc exact distance later
		max_latitude = user_lat + user_pref.max_distance
		max_longitude = user_long + user_pref.max_distance

		#distance = dist_between(0,50,0,51)
		#print(distance)

		# get next <limit> qualifying users from db, filter by preferences, order by user_id
		all_users = UserProfile.objects.filter(dob__range=(min_dob, max_dob)).order_by('user__username')[offset:limit]
		# check against decision table
		
		# if okay, load photos

		response = {'status': 'success'}
		return JsonResponse(response)

	# load all matches for chat
	@csrf_exempt
	def get_matches(request):
		pass

	# load a detailed user profile for viewing
	@csrf_exempt
	def load_target_profile(request):
		pass

	# submit a yes/no decision on a user
	@csrf_exempt
	def submit_decision(request):
		pass

	# calculate the distance between two coordinates
	def dist_between(lat1_deg, long1_deg, lat2_deg, long2_deg):
		# mean radius earth
		R = 6373.0
		# convert to radians
		lat1 = radians(lat1_deg)
		long1 = radians(long1_deg)
		lat2 = radians(lat2_deg)
		long2 = radians(long2_deg)
		# calc difference
		dlat = lat2 - lat1
		dlong = long2 - long1
		# standard dist between points on sphere calc
		a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlong / 2)**2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))
		dist = R * c

		return dist

# replace with channels websockets
class Chat:
	# load all messages
	@csrf_exempt
	def get_messages(request):

		origin_user_id = escape(data['userID'])
		match_id = escape(data['matchID'])

		datetime.datetime.now(),



	# send a new message
	@csrf_exempt
	def send_message(request):
		pass


class Settings:
	@csrf_exempt
	def get_settings(request):
		pass

	@csrf_exempt
	def modify_settings(request):
		pass
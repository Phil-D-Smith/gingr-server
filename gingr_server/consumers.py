import json, uuid, datetime

from channels import Group, Channel
from channels.auth import channel_session_user, channel_session_user_from_http

from .models import UserProfile, Decision, Match, Message

# reply_channel is channel client sent on, send() is the method to reply
@channel_session_user
def ws_receive(message):
	# get data from json string
	data = json.loads(message['text'])
	# split into variables
	sender_id = escape(data["senderID"])
	match_id = escape(data["matchID"])
	message_body = escape(data["messageBody"])
	target_id = 0

	# get current date time
	date_time = datetime.datetime.now()

	# find match object with the matchID
	match = Match.objects.get(match_id=match_id)

	# update message count, date, and last_message
	match.message_count = match.message_count + 1
	message_number = match.message_count
	match.date_time = datetime.datetime.now()
	match.last_message = message_body

	# find which user sent the message, set target, update the "last_seen" counter of that user
	if (sender_id == match.user_id_1):
		match.last_seen_user_1 = match.message_count
		target_id = match.user_id_2
	if (sender_id == match.user_id_2):
		match.last_seen_user_2 = match.message_count
		target_id = match.user_id_1

	# make new Message object with data
	user_message = Message(	match=match,
							sender_id=sender_id,
							message_number=message_number,
							date_time=date_time,
							message_body=message_body)
	# save changes to db
	match.save()
	user_message.save()

	# message array for response
	message_data = {'dateTime': date_time,
					'messageNumber': message_number,
					'messageBody': message_body,
					'senderID': sender_id}

	message = {
		'text': json.dumps({
			'action': 'message',
			'data': message_data
			})
		}

	# reply with success message
	#message.reply_channel.send('hello')

	# send message to target
	Group('user-%s' % target_id).send(message)


# set up channel, add user to group
@channel_session_user_from_http
def ws_connect(message):
	# accept incoming connection
	message.reply_channel.send({"accept": True})

	# set session variable from query string sent with connection request
	user_id = message.content['query_string'].decode('utf8')
	message.channel_session['user_id'] = user_id

	# add to groups, including individual group for private messages
	Group('all-users').add(message.reply_channel)
	Group('user-%s' % message.channel_session['user_id']).add(message.reply_channel)


# remove channel from group - for groups
@channel_session_user
def ws_disconnect(message):
	# broadcast and discard
	Group('all-users').send({'text': 'removed user'})
	Group('all-users').discard(message.reply_channel)
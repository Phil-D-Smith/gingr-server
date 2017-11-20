import json
import time

from channels import Group, Channel
from channels.auth import channel_session_user, channel_session_user_from_http

# reply_channel is channel client sent on, send() is the method to reply
@channel_session_user
def ws_receive(message):
	# message recieved from client, store in db, send to target + push notification
	print(message['text'])

	data = json.parse(message.data)
	target_id = 0
	# payload = json.loads(message['text'])
	response = {
		'text': json.dumps({
			'data': message.user.username,
			'is_logged_in': True
			})
		}
	
	# make Message object with data
	user_message = Message(	message_id = str(uuid.uuid1()),
							match_id = 0,
							sender_id = 0,
							message_number = 0,
							date_time = datetime.datetime.now(),
							message_body = 0)
	# save to db
	user_message.save()

	# reply with success message
	message.reply_channel.send('success')
	Group('user-%s' % target_id).send("hello")


# set up channel, add user to group
@channel_session_user_from_http
def ws_connect(message):
	# accept incomming connection
	message.reply_channel.send({"accept": True})

	# set session variables
	message.channel_session['user_id'] = "hello"
	# add to groups
	Group('all-users').add(message.reply_channel)
	Group('user-%s' % message.channel_session['user_id']).add(message.reply_channel)
	# broadcast - testing
	Group('all-users').send({'text': 'added new user'})

	print(message)

# remove channel from group - for groups
@channel_session_user
def ws_disconnect(message):
	# broadcast and discard
	Group('all-users').send({'text': 'removed user'})
	Group('all-users').discard(message.reply_channel)
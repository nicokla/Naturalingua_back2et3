# app/server/main/views.py

from flask import Flask, render_template, url_for, jsonify, request, abort, make_response
from flask_mail import Mail, Message
import os
import pickle
from flask import current_app

from flask import render_template, Blueprint, jsonify, request, current_app, redirect


from server.utils import email_util
import uuid

main_blueprint = Blueprint("main", __name__, template_folder='templates')


# https://stackoverflow.com/questions/26980713/solve-cross-origin-resource-sharing-with-flask
# localhost:5000/stripe_pay/french/nicolas.klarsfeld@gmail.com?id=E3Blxs0Wfco&id=StXPXDij6rw
@main_blueprint.route('/stripe_pay/<language>/<languageKnown>/<alphabetId>/<clientEmail>', methods=['GET'])
def stripe_pay(language, languageKnown, alphabetId, clientEmail):
	videoIds = request.args.getlist('id', type=str)
	language=str(language).lower()
	clientEmail=str(clientEmail)
	languageKnown=str(languageKnown).lower()
	alphabetId=str(alphabetId)
	# priceId='price_1KIxBfL309RW9KQTeeiAZIUp'
	priceId='price_1KYmapL309RW9KQTmYazY1r4'
	#'price_1KTjqpL309RW9KQTqNnsBorh'
	#'price_1KQdJIL309RW9KQTUFKNDbVW'
	stripe = current_app.config['stripe']
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price': priceId,
			'quantity': len(videoIds),
		}],
		metadata={
			"language": language,
			"clientEmail": clientEmail,
			"videoIds": ','.join(videoIds),
			"typePurchase":'youtube',
			"languageKnown": languageKnown,
			"alphabetId": alphabetId
		},
		customer_email=clientEmail,
		mode='payment',
		success_url=f'https://getyoutubesubtitles.netlify.app/success/{clientEmail}',
		cancel_url='https://getyoutubesubtitles.netlify.app/cancel' 
		# success_url=f'https://naturalingua.netlify.app/success/{email}',
		# cancel_url='https://naturalingua.netlify.app/cancel' 
	)
	#url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
	#url_for('index', _external=True),
	response=jsonify({
		'checkout_session_id': session['id'], 
	})
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response




@main_blueprint.route('/stripe_pay2/<language>/<alphabetId>/<clientEmail>', methods=['GET'])
def stripe_pay2(language, alphabetId, clientEmail):
	language=str(language).lower()
	alphabetId=str(alphabetId)
	clientEmail=str(clientEmail)
	priceId= 'price_1KYmYpL309RW9KQT577ea5ow'
	#'price_1KVHfCL309RW9KQT03B5fosI'
	stripe = current_app.config['stripe']
	session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=[{
			'price': priceId,
			'quantity': 1,
		}],
		metadata={
			"language": language,
			"clientEmail": clientEmail,
			"typePurchase":'movies',
			"alphabetId": alphabetId
		},
		customer_email=clientEmail,
		mode='payment',
		success_url=f'https://getmoviessubtitles.netlify.app/success/{clientEmail}',
		cancel_url='https://getmoviessubtitles.netlify.app/cancel' 
		# success_url=f'https://naturalingua.netlify.app/success/{email}',
		# cancel_url='https://naturalingua.netlify.app/cancel' 
	)
	#url_for('thanks', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
	#url_for('index', _external=True),
	response=jsonify({
		'checkout_session_id': session['id'], 
	})
	response.headers.add('Access-Control-Allow-Origin', '*')
	return response



# stripe login
# stripe listen --forward-to localhost:5000/turlututu
# stripe trigger payment_intent.succeeded (invoice.payment_succeeded, checkout.session.completed, etc.  --->  stripe trigger --help)
@main_blueprint.route('/turlututu', methods=['POST'])
def stripe_webhook():
	print('WEBHOOK CALLED')
	if request.content_length > 1024 * 1024:
		print('REQUEST TOO BIG')
		abort(400)
	payload = request.get_data()
	sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
	endpoint_secret = 'whsec_q8Zjnt3ApOAF6x68f0Qy9TWEcTQbPql8'
	stripe = current_app.config['stripe']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, sig_header, endpoint_secret
		)
	except ValueError as e:
		# Invalid payload
		print('INVALID PAYLOAD')
		return {}, 400
	except stripe.error.SignatureVerificationError as e:
		# Invalid signature
		print('INVALID SIGNATURE')
		return {}, 400
    # Handle the checkout.session.completed event
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		current_app.logger.info(session)
		line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
		current_app.logger.info(line_items['data'][0]['description'])
		typePurchase = session['metadata']['typePurchase']
		if not (typePurchase in ['youtube', 'movies']):
			return {}
		language=session['metadata']['language']
		clientEmail= session['customer_email'] # session['metadata']['clientEmail']
		if(typePurchase == 'youtube'):
			videoIdsBeforeSplit=session['metadata']['videoIds']
			videoIds = videoIdsBeforeSplit.split(',')
			sessionId=str(uuid.uuid4())
			languageKnown=session['metadata']['languageKnown']
			alphabetId=session['metadata']['alphabetId']
			email_util.send_email(videoIds, language, languageKnown, alphabetId, sessionId, clientEmail, 'Language documents', '<html><body>Please find your documents attached to this email.</body></html>')
		else: # movies
			alphabetId=session['metadata']['alphabetId']
			email_util.send_email_movies(language, alphabetId, clientEmail, clientEmail, 'Language document', '<html><body>Please find your document attached to this email.</body></html>')
	return {}




@main_blueprint.route('/test/<language>/<languageKnown>/<alphabetId>/<clientEmail>', methods=['GET'])
def test(language, languageKnown, alphabetId, clientEmail):
	videoIds = request.args.getlist('id', type=str)
	language=str(language).lower()
	languageKnown=str(languageKnown).lower()
	alphabetId=str(alphabetId)
	clientEmail=str(clientEmail)
	sessionId=str(uuid.uuid4())
	email_util.send_email(videoIds, language, languageKnown, alphabetId, sessionId, clientEmail, 'Language documents', '<html><body>Please find your documents attached to this email.</body></html>')
	return {}


@main_blueprint.route('/test2/<language>/<alphabetId>/<clientEmail>', methods=['GET'])
def test2(language, alphabetId, clientEmail):
	language=str(language).lower()
	clientEmail=str(clientEmail)
	alphabetId=str(alphabetId)
	email_util.send_email_movies(language, alphabetId, clientEmail, clientEmail, 'Language document', '<html><body>Please find your document attached to this email.</body></html>')
	return {}



# ===========================


# localhost:5000/coucou/hebrew/nicolas.klarsfeld@gmail.com?id=E3Blxs0Wfco
# https://yshegsjk.xyz/coucou/hebrew/nicolas.klarsfeld@gmail.com?id=E3Blxs0Wfco
# hebrew    &id=E3Blxs0Wfco
# japanese    Og-a-OMrL7Q
# @main_blueprint.route("/coucou/<language>/<clientEmail>", methods=["GET"])
# def home(language, clientEmail): # async
# 	videoIds = request.args.getlist('id', type=str)
# 	language=str(language)
# 	clientEmail=str(clientEmail)
# 	sessionId=str(uuid.uuid4())
# 	current_app.logger.info('videoIds: %s', videoIds)
# 	current_app.logger.info('language: %s', language)
# 	current_app.logger.info('clientEmail: %s', clientEmail)
# 	email_util.send_email(videoIds, language, sessionId, clientEmail, 'Language documents', '<html><body>Please find your documents attached to this email.</body></html>')
# 	response=jsonify({
# 		'toto': 'prout', 
# 	})
# 	return response


# ===========================

# localhost:5000/coucou2
# @main_blueprint.route("/coucou2", methods=["GET"])
# def home2(): #(language, clientEmail) # async
# 	language='japanese' #str(language)
# 	clientEmail='nicolas.klarsfeld@gmail.com' #str(clientEmail)
# 	sessionId='randomEmail' #str(uuid.uuid4())
# 	email_util.send_email_movies(language, sessionId, clientEmail, 'Language document', '<html><body>Please find your document attached to this email.</body></html>')
# 	response=jsonify({
# 		'toto': 'prout', 
# 	})
# 	return response


# ====================

from werkzeug.utils import secure_filename

# @main_blueprint.route("/upload", methods=["POST"])
# def upload():
# 	file = request.form['image']
# 	fileName=secure_filename(file.filename)
# 	liste = fileName.split('.')
# 	if(len(liste) == 1):
# 		return 'oups'
# 	file.save(f'/opt/app/mytmp/randomEmail/anglais.{liste[-1]}')
# 	# {secure_filename(file.filename)}
# 	return 'Done !'


from server.utils.rq_helpers import redis_connection, scheduler
from uuid import uuid4
from server.utils.utils import createNecessaryFolders
# from server.utils.crypto import mysalt 
# import bcrypt
from datetime import timedelta

import shutil

def deleteFolder(folderName):
	try:
		shutil.rmtree(folderName)
	except:
		return


# jsonify({'message': 'wrong email'})
# emailCrypto= bcrypt.hashpw(email.encode('utf-8'), mysalt).decode('utf-8')
# for file in request.files.getlist('files'):
# current_app.logger.info(f"hello")


@main_blueprint.route('/uploadAnglais', methods=['POST'])
def uploadAnglais():
	listeOfFiles = request.files.getlist('files')
	current_app.logger.info(listeOfFiles)
	try:
		file = listeOfFiles[0]
		filename = secure_filename(file.filename)
		if(filename == ''):
			return 'Missing one of the two subtitles files.', 303
	except:
		return 'Missing one of the two subtitles files.', 303
	email = request.headers.get('email')
	current_app.logger.info(email)
	if('/' in email or '..' in email or '+' in email or not '@' in email or len(email)<=4):
		return 'Wrong email.', 301
	current_app.logger.info(str(redis_connection.get(email)))
	# if(redis_connection.get(email) != 'ok'.encode('utf-8')):
	# 	token=str(uuid4())
	# 	redis_connection.set(email, token, ex=600)
	# 	email_util.sendEmailConfirmation(email, token)
	# 	return 'Please confirm your email by clicking on the link we sent you', 302
	current_app.logger.info(filename)
	suffix = filename.split('.')[-1].lower()
	if file and suffix in ['vtt','xml','srt','ass']:
		folderName=f'/home/flask/mytmp/{email}'
		myPath=os.path.join(folderName, f'anglais.{suffix}')
		createNecessaryFolders(myPath)
		file.save(myPath) # filename
		scheduler.enqueue_in(timedelta(hours=1), deleteFolder, args=[folderName])
	else:
		return 'Wrong file format', 304
	return 'ok', 200 # redirect('/')


@main_blueprint.route('/uploadJaponais', methods=['POST'])
def uploadJaponais():
	listeOfFiles = request.files.getlist('files')
	current_app.logger.info(listeOfFiles)
	try:
		file = listeOfFiles[0]
		filename = secure_filename(file.filename)
		if(filename == ''):
			return 'Missing one of the two subtitles files.', 303
	except:
		return 'Missing one of the two subtitles files.', 303
	email = request.headers.get('email')
	current_app.logger.info(email)
	if('/' in email or '..' in email or '+' in email or not '@' in email  or len(email)<=4):
		return 'Wrong email.', 301
	current_app.logger.info(str(redis_connection.get(email)))
	# if(redis_connection.get(email) != 'ok'.encode('utf-8')):
	# 	token=str(uuid4())
	# 	redis_connection.set(email, token, ex=600)
	# 	email_util.sendEmailConfirmation(email, token)
	# 	return 'Please confirm your email by clicking on the link we sent you', 302
	current_app.logger.info(filename)
	suffix = filename.split('.')[-1].lower()
	if file and suffix in ['vtt','xml','srt','ass']:
		folderName=f'/home/flask/mytmp/{email}'
		myPath=os.path.join(folderName, f'japonais.{suffix}')
		createNecessaryFolders(myPath)
		file.save(myPath) # filename
		scheduler.enqueue_in(timedelta(hours=1), deleteFolder, args=[folderName])
	else:
		return 'Wrong file format', 304
	return 'ok', 200 # redirect('/')


from server.utils.rq_helpers import redis_connection
@main_blueprint.route('/confirm/<clientEmail>/<token>', methods=['GET'])
def confirm(clientEmail, token):
	clientEmail=str(clientEmail)
	token = str(token)
	if(redis_connection.exists(clientEmail)):
		if(redis_connection.get(clientEmail) == token.encode('utf-8')):
			redis_connection.set(clientEmail, 'ok', ex=600)
			return 'ok', 200
	#'Thank you for confirming your email adress, you can now continue your order.'
	return 'not ok', 301




# @app.route('/classification', methods=['POST'])
# def uploadImage():
#     if request.method == 'POST':
#         base64_png =  request.form['image']
#         code = base64.b64decode(base64_png.split(',')[1]) 
#         image_decoded = Image.open(BytesIO(code))
#         image_decoded.save(Path(app.config['UPLOAD_FOLDER']) / 'image.png')
#         return make_response(jsonify({'result': 'success'}))
#     else: 
#         return make_response(jsonify({'result': 'invalid method'}), 400)

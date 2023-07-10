# app/server/__init__.py

#!/usr/bin/env python
import sys
from rq import Queue, Connection, Worker
# import redis
# redis_connection = redis.from_url("redis://redis:6379/0")

#Preload libraries
sys.path.append("/opt/app")
from server.utils.rq_helpers import queue, redis_connection

from server.utils.utils import createNecessaryFolders
from server.transliterateHehe.languageCodes import languageToCodes, getCode
from server.youtube.youtube import absorbYoutubeVideo
from server.utils.createPdfs import createPdf
import os
from server.movies.movies import subsToTxt
from server.utils.email import sendEmail, createMessage, attachFile
import shutil

def prepareMsg(videoIds, language, languageKnown, alphabetId, sessionId, to, subject, template):
	message = createMessage(template, subject)
	createNecessaryFolders(f'/home/flask/mytmp/{sessionId}/titi.txt')
	languageCodes=languageToCodes[language]
	languageCodesKnown=languageToCodes[languageKnown]
	for videoId in videoIds:
		txtFileName = absorbYoutubeVideo(videoId, languageCodes, languageCodesKnown, alphabetId, sessionId, print) # https://testdriven.io/blog/flask-async/ # await
		myPdf = createPdf(videoId, txtFileName, language, alphabetId)
		attachFile(message, f'{videoId}.pdf', myPdf)
		os.remove(txtFileName)
	os.rmdir(f'/home/flask/mytmp/{sessionId}')
	sendEmail(message, to)


def prepareMsgMovies(language, alphabetId, sessionId, to, subject, template):
	message = createMessage(template, subject)
	createNecessaryFolders(f'/home/flask/mytmp/{sessionId}/titi.txt')
	languageCode = getCode(language) #languageToCodes[language]
	txtFileName = subsToTxt(f'/home/flask/mytmp/{sessionId}', languageCode, alphabetId)
	myPdf = createPdf('prout', txtFileName, language, alphabetId, isYoutube=False)
	attachFile(message, 'result.pdf', myPdf)
	os.remove(txtFileName)
	shutil.rmtree(f'/home/flask/mytmp/{sessionId}')
	# os.rmdir(f'/home/flask/mytmp/{sessionId}')
	sendEmail(message, to)


from server.utils.rq_helpers import redis_connection
# from uuid import uuid4
def sendEmailForToken(clientEmail, token):
	# link=f'https://yshegsjk.xyz/confirm/{clientEmail}/{token}'
	link=f'https://getmoviessubtitles.netlify.app/confirm/{clientEmail}/{token}'
	html=f'<html><a href={link}>confirmation link</a></html>'
	subject='confirmation link'
	message = createMessage(html, subject)
	sendEmail(message, clientEmail)

# with Connection(redis_connection):
	# queue = Queue('default')
w = Worker([queue], connection=redis_connection)
w.work()





# ==============
# import sys
# from rq import Connection, Worker
# import redis

# # import server.config
# # server.config.ProductionConfig.REDIS_URL

# redis_connection = redis.from_url("redis://redis:6379/0")
# # redis_connection = redis.Redis()

# # Preload libraries
# # ...

# # Provide queue names to listen to as arguments to this script,
# # similar to rq worker
# with Connection(redis_connection):
# 	w = Worker(['default'])
# 	w.work()



# ======================
# import os
# import redis
# from rq import Worker, Queue, Connection
# from server import config

# listen = ['default'] # 'some_queue', 

# # redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
# # conn = redis.from_url(redis_url)

# redis_connection = redis.from_url(config.ProductionConfig.REDIS_URL)

# from youtube.youtube import absorbYoutubeVideo
# from movies.movies import subsToTxt
# from utils.createPdfs import createPdf
# # from tempfile import TemporaryFile
# from utils.utils import createNecessaryFolders
# from transliterateHehe.languageCodes import languageToCodes, getCode

# if __name__ == '__main__':
# 	with Connection(redis_connection):
# 		worker = Worker(map(Queue, listen))
# 		worker.work()
# # app/server/jobs/worker.py
# #!/usr/bin/env python
# import sys
# from rq import Queue, Connection, Worker
# # import redis
# # redis_connection = redis.from_url("redis://redis:6379/0")

# #Preload libraries
# sys.path.append("/opt/app")
# from server.main.rq_helpers import queue, redis_connection

# # from server import app
# # from server.utils.utils import createNecessaryFolders
# # from server.transliterateHehe.languageCodes import languageToCodes, getCode
# # from server.youtube.youtube import absorbYoutubeVideo
# # from server.utils.createPdfs import createPdf
# # import os
# # from flask_mail import Mail
# # from server.movies.movies import subsToTxt

# # with Connection(redis_connection):
# 	# queue = Queue('default')
# w = Worker([queue], connection=redis_connection)
# w.work()



# # ==============
# # import sys
# # from rq import Connection, Worker
# # import redis

# # # import server.config
# # # server.config.ProductionConfig.REDIS_URL

# # redis_connection = redis.from_url("redis://redis:6379/0")
# # # redis_connection = redis.Redis()

# # # Preload libraries
# # # ...

# # # Provide queue names to listen to as arguments to this script,
# # # similar to rq worker
# # with Connection(redis_connection):
# # 	w = Worker(['default'])
# # 	w.work()



# # ======================
# # import os
# # import redis
# # from rq import Worker, Queue, Connection
# # from server import config

# # listen = ['default'] # 'some_queue', 

# # # redis_url = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
# # # conn = redis.from_url(redis_url)

# # redis_connection = redis.from_url(config.ProductionConfig.REDIS_URL)

# # from youtube.youtube import absorbYoutubeVideo
# # from movies.movies import subsToTxt
# # from utils.createPdfs import createPdf
# # # from tempfile import TemporaryFile
# # from utils.utils import createNecessaryFolders
# # from transliterateHehe.languageCodes import languageToCodes, getCode

# # if __name__ == '__main__':
# # 	with Connection(redis_connection):
# # 		worker = Worker(map(Queue, listen))
# # 		worker.work()
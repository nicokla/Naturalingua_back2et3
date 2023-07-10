# app/server/main/tasks.py


# from rq.decorators import job
# from rq import get_current_job
# from server.main.rq_helpers import redis_connection
# import time
# from rq_scheduler import Scheduler
# from datetime import datetime
# from datetime import timedelta
# from redis import Redis
# from server.youtube.youtube import absorbeEtCreeLesPdfs

# scheduler = Scheduler(connection=Redis()) # Get a scheduler for the "default" queue

# def send(files, clientEmail):
# 	myString='<html><body>coucou</body></html>'
# 	email=current_app.config['EMAIL']
# 	msg = Message(sender=email,recipients=[clientEmail])
# 	msg.html=myString
# 	for file in files:
# 		fileName=file.split('/')[-1]
# 		with current_app.open_resource(file) as fp:
# 			msg.attach(fileName, "application/pdf", fp.read())
# 	mail.send(msg)

# @job('default', connection=redis_connection, timeout=300, result_ttl=7*24*60*60)
# def doWhatINeed(videoIds, language, clientEmail, sessionId):
# 	# videoIds=['E3Blxs0Wfco']
# 	# sessionId='sessionId'
# 	# language='french'
#     # clientEmail='nicolas.klarsfeld@gmail.com'
# 	listePdfs=absorbeEtCreeLesPdfs(videoIds, language, sessionId)
# 	send(listePdfs, clientEmail)



# for file in listePdfs:
# 	os.remove(file)
# scheduler.enqueue_in(timedelta(days=1), deleteDocs, sessionId)
    



# the timeout parameter specifies how long a job may take
# to execute before it is aborted and regardes as failed
# the result_ttl parameter specifies how long (in seconds)
# successful jobs and their results are kept.
# for more detail: https://python-rq.org/docs/jobs/

# @job('default', connection=redis_connection, timeout=90, result_ttl=7*24*60*60)
# def wait(num_iterations):
#     """
#     wait for num_iterations seconds
#     """
#     # get a reference to the job we are currently in
#     # to send back status reports
#     self_job = get_current_job()

#     # define job
#     for i in range(1, num_iterations + 1):  # start from 1 to get round numbers in the progress information
#         time.sleep(1)
#         self_job.meta['progress'] = {
#             'num_iterations': num_iterations,
#             'iteration': i,
#             'percent': i / num_iterations * 100
#         }
#         # save meta information to queue
#         self_job.save_meta()

#     # return job result (can be accesed as job.result)
#     return num_iterations

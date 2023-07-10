from server.utils.rq_helpers import queue
from flask_mail import Message

# https://testdriven.io/blog/flask-async/
def send_email(videoIds, language, languageKnown, alphabetId, sessionId, to, subject, template):
    queue.enqueue("server.prepareMsg", args=(videoIds, language, languageKnown, alphabetId, sessionId, to, subject, template))
    # server.jobs.jobYoutube.prepareMsg
    # queue.empty() # docker exec -it 27bc871cdf57 redis-cli FLUSHALL
    # queue.enqueue(worker_sendmail,args=(msg,))


def send_email_movies(language, alphabetId, sessionId, to, subject, template):
    queue.enqueue("server.prepareMsgMovies", args=(language, alphabetId, sessionId, to, subject, template), timeout=1200)
    # server.jobs.jobMovies.prepareMsgMovies


def sendEmailConfirmation(clientEmail, token):
    queue.enqueue("server.sendEmailForToken", args=(clientEmail,token))

#     createNecessaryFolders(f'/home/flask/mytmp/{sessionId}/titi.txt')
#     languageCode = getCode(language) #languageToCodes[language]
#     print('subsToTxt')
#     txtFileName = subsToTxt(f'/home/flask/mytmp/{sessionId}', languageCode)
#     print('createPdf')
#     myPdf = createPdf('prout', txtFileName, isYoutube=False)
#     print('attach')
#     aaa = msg.attach(f'result.pdf', "application/pdf", myPdf)
#     os.remove(txtFileName)
#     # os.rmdir(f'/home/flask/mytmp/{sessionId}')
#     shutil.rmtree(f'/home/flask/mytmp/{sessionId}')
#     app.config.update(dict(
#         MAIL_PORT = 587,
#         MAIL_USE_TLS = True,
#         MAIL_USE_SSL = False,
#         MAIL_SERVER = 'smtp.gmail.com',
#         MAIL_USERNAME = 'naturalingua.noreply@gmail.com', #app.config['EMAIL'],
#         MAIL_PASSWORD = "gloubiboulga123.M" #app.config['PASSWORD']
#     ))
#     theMail=Mail(app)
#     print('sending email')
#     aaa=theMail.send(msg)







# =======================



# def testMovies(language, sessionId, to, subject, template):
#     msg = Message(
#         subject,
#         recipients=[to],
#         html=template,
#         sender='naturalingua.noreply@gmail.com' #app.config['MAIL_DEFAULT_SENDER']
#     )
#     # queue.enqueue(prepareMsg, args=(msg,videoIds, language, sessionId))
#     createNecessaryFolders(f'/opt/app/mytmp/{sessionId}/titi.txt')
#     languageCodes=languageToCodes[language]
#     # app.logger.info('languageCodes: %s', languageCodes)
#     txtFileName = subsToTxt(f'/opt/app/mytmp/{sessionId}')
#     aaa=createPdf('prout', txtFileName)


    # myPdf = createPdf(videoId, txtFileName)
#     aaa=msg.attach(f'{videoId}.pdf', "application/pdf", myPdf)
#     os.remove(txtFileName)
# os.rmdir(f'/opt/app/mytmp/{sessionId}')
# app.config.update(dict(
#     MAIL_PORT = 587,
#     MAIL_USE_TLS = True,
#     MAIL_USE_SSL = False,
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_USERNAME = 'naturalingua.noreply@gmail.com', #app.config['EMAIL'],
#     MAIL_PASSWORD = "gloubiboulga123.M" #app.config['PASSWORD']
# ))
# theMail=Mail(app)
# aaa=theMail.send(msg)


# ======================


# https://github.com/svee/immunity-passport/blob/d405296fc0e12165b1e21d4657d1aa2fe67497ee/im_pass/gen_pass.py#L72
# Once the report is approved, this is called to send immunity pass through e-mail
# def generate_immunity_pass(email_id, fattach):
#     html = '<html><body>coucou</body></html>' # render_template('passportby_mail.html')
#     subject = "Your immunity pass is approved"
#     try:
#         send_email(email_id, subject, html,fattach,"immunity_passport.png", "png") 
#     except Exception as e:
#         return   #Silent here as user can later download always.



# def generate_temp_report(current_user):
#     im_stream = current_user.reports[-1].lab_report.get()
#     tempFileObj = NamedTemporaryFile(mode='w+b',suffix='pdf')
#     tempFileObj.write(im_stream.read())
#     tempFileObj.seek(0,0)
#     return tempFileObj


# https://github.com/svee/immunity-passport/blob/d405296fc0e12165b1e21d4657d1aa2fe67497ee/im_pass/gen_pass.py#L9

# https://github.com/asim3/notes/blob/794ae4ebd8c7ecd9a07d64336fe39b2c257bcc63/data/python/other/qr_codes.md

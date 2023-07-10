# app/server/jobs/jobMovies.py

# from server.utils.utils import createNecessaryFolders
# from server.transliterateHehe.languageCodes import getCode
# from server.utils.createPdfs import createPdf
# import os
# from server.movies.movies import subsToTxt
# from server.utils.email import sendEmail, createMessage, attachFile
# import shutil



# def prepareMsgMovies(language, sessionId, to, subject, template):
#     message = createMessage(template, subject)
#     createNecessaryFolders(f'/opt/app/mytmp/{sessionId}/titi.txt')
#     languageCode = getCode(language) #languageToCodes[language]
#     txtFileName = subsToTxt(f'/opt/app/mytmp/{sessionId}', languageCode)
#     myPdf = createPdf('prout', txtFileName, isYoutube=False)
#     attachFile(message, 'result.pdf', myPdf)
#     os.remove(txtFileName)
#     shutil.rmtree(f'/opt/app/mytmp/{sessionId}')
#     # os.rmdir(f'/opt/app/mytmp/{sessionId}')
#     sendEmail(message, to)



# msg = Message(
#         subject,
#         recipients=[to],
#         html=template,
#         sender='naturalingua.noreply@gmail.com' #app.config['MAIL_DEFAULT_SENDER']
#     )

#     aaa = msg.attach(f'result.pdf', "application/pdf", myPdf)
# from flask_mail import Mail
# with app.app_context():
# ...
# app.config.update(dict(
#     MAIL_PORT = 587,
#     MAIL_USE_TLS = True,
#     MAIL_USE_SSL = False,
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_USERNAME = 'naturalingua.noreply@gmail.com', #app.config['EMAIL'],
#     MAIL_PASSWORD = "gloubiboulga123.M" #app.config['PASSWORD']
# ))
# theMail=Mail(app)
# print('sending email')
# aaa=theMail.send(msg)
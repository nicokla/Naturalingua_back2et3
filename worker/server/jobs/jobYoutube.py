# app/server/jobs/jobYoutube.py

# from server.utils.utils import createNecessaryFolders
# from server.transliterateHehe.languageCodes import languageToCodes
# from server.youtube.youtube import absorbYoutubeVideo
# from server.utils.createPdfs import createPdf
# import os
# from server.utils.email import sendEmail, createMessage, attachFile


# def prepareMsg(videoIds, language, sessionId, to, subject, template):
#     message = createMessage(template, subject)
#     createNecessaryFolders(f'/opt/app/mytmp/{sessionId}/titi.txt')
#     languageCodes=languageToCodes[language]
#     for videoId in videoIds:
#         txtFileName = absorbYoutubeVideo(videoId, languageCodes, sessionId, print) # https://testdriven.io/blog/flask-async/ # await
#         myPdf = createPdf(videoId, txtFileName)
#         attachFile(message, f'{videoId}.pdf', myPdf)
#         os.remove(txtFileName)
#     os.rmdir(f'/opt/app/mytmp/{sessionId}')
#     sendEmail(message, to)
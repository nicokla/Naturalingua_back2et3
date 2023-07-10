from re import S
import emails
# from emails.template import JinjaTemplate as T
# T("Build passed: {{ project_name }} ...")

def createMessage(html, subject):
	# emails.Message(text=T("Build passed: {{ project_name }} ..."),
	m = emails.Message(html=html,
										subject=subject,
										mail_from=("naturalingua.noreply", "naturalingua.noreply@gmail.com"))
	return m

def attachFile(message, fileName, data):
	# content_disposition="inline"
	message.attach(filename=fileName, data=data)
	# data=open(filePath, "rb")


def sendEmail(message, clientEmail):
	# m.send(render={"project_name": "user/project1", "build_id": 121},
	# 'port': 465, 'ssl': True,
	response = message.send(to=clientEmail,
                  smtp={"host": "smtp.gmail.com",
												"port": 587, 
												'ssl': False,
												'tls': True,
												'user': 'naturalingua.noreply@gmail.com',
												'password': 'gloubiboulga123.M'})
	return response



# html = "<html><p>hello</p></html>"
# subject = "subject"
# clientEmail='nicolas.klarsfeld@gmail.com'
# aaa = sendEmail(html,subject, clientEmail)

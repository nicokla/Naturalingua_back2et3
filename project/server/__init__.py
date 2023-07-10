# app/server/__init__.py


import sys
sys.path.append("/opt/app")

import os
from flask import Flask
import traceback  # error traceback
from flask import Flask, request, jsonify
from werkzeug.exceptions import default_exceptions  # exception handling
from werkzeug.exceptions import HTTPException  # exception handling


from flask_cors import CORS
from dotenv import load_dotenv
import stripe
import logging
import boto3
from botocore.exceptions import ClientError
import requests
import os
from flask_mail import Mail, Message


def doStuff():

    # instantiate the app
    app = Flask(__name__, instance_relative_config=False)
    CORS(app)

    # set config
    # app.config.from_object("server.config.ProductionConfig")

    load_dotenv('/opt/app/server/.env')

    app.config['EMAIL']=os.environ.get('EMAIL')
    app.config['PASSWORD']=os.environ.get('PASSWORD')
    app.config['SECRET_KEY']=os.environ.get('SECRET_KEY')
    app.config['PUBLISHABLE_KEY']=os.environ.get('PUBLISHABLE_KEY')
    app.config['AWS_ACCESS_KEY_ID'] = os.environ.get('AWS_ACCESS_KEY_ID')
    app.config['AWS_SECRET_ACCESS_KEY'] = os.environ.get('AWS_SECRET_ACCESS_KEY')
    # app.config['prices']=get_object('./products.pkl')


    app.config['client'] = boto3.client('s3',
            region_name='eu-west-3',
            aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=app.config['AWS_SECRET_ACCESS_KEY'],)

    # app.config.update(dict(
    #     DEBUG = False,
    #     MAIL_SERVER = 'smtp.gmail.com',
    #     MAIL_PORT = 587,
    #     MAIL_USE_TLS = True,
    #     MAIL_USE_SSL = False,
    #     MAIL_USERNAME = 'naturalingua.noreply@gmail.com', #app.config['EMAIL'],
    #     MAIL_PASSWORD = "gloubiboulga123.M" #app.config['PASSWORD']
    # ))
    # mail = Mail(app)
    app.config.update(dict(
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_SERVER = 'smtp.gmail.com',
        MAIL_USERNAME = 'naturalingua.noreply@gmail.com', #app.config['EMAIL'],
        MAIL_PASSWORD = "gloubiboulga123.M" #app.config['PASSWORD']
    ))

    stripe.api_key = app.config['SECRET_KEY']
    app.config['stripe'] = stripe

    # !!!!!!!!! good for debugging (beginning) !!!!!!!!!!!!!
    # better exception handling
    # @app.errorhandler(Exception)
    # def handle_error(e):
    #     # 400 for https error, 500 for internal error
    #     if isinstance(e, HTTPException):
    #         # status_code = e.code
    #         status_code = 400
    #     else:
    #         status_code = 500
    #     # prepare error message
    #     message = str(e)
    #     # stdout error traceback
    #     print(traceback.format_exc())
    #     # return response
    #     return jsonify(message=message, error_traceback=traceback.format_exc()), status_code

    # for ex in default_exceptions:
    #     app.register_error_handler(ex, handle_error)
    # !!!!!!!!! good for debugging (end) !!!!!!!!!!!!!

    return app #, mail


app = doStuff() #, mail
from server.main.views import main_blueprint
app.register_blueprint(main_blueprint)


# def create_app():
#     return app


# uncomment if running python __init__.py :
# if __name__ == '__main__':
#     app.run(debug=True)



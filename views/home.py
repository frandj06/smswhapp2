import requests, threading, time

from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response
from flask import current_app as app
from models.models import CatalogDevices, CatalogMessages, CatalogOperationsCenter, CatalogUserTestType, SentMessages, SentMessagesProgress, User

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')

# Wassenger Background Task
# Configuration - API Key and Headers
class WassengerTask(threading.Thread):
    # Properties init
    def __init__(self, records, url, sleeptime, msgtype):
        threading.Thread.__init__(self)
        self.headers = {
            "Content-Type": "application/json",
            "Token": app.config['WASS_API_KEY']
        }
        self.msgtype = msgtype
        self.records = records
        self.sleeptime = sleeptime
        self.url = url
    
    # Thread activity task
    def run(self, *args, **kwargs):
        while True:
            for item in self.records.items:
                print(item.name)
            
            if self.records.has_next:
                self.records = self.records.next()
            else:
                print("********* - WassengerTask Thread Finished - *********")
                break


@home.route('/')
def _index():
    app.logger.debug('** SWING_CMS ** - Index')
    return redirect(url_for('home._home'))


@home.route('/acercade/')
def _acercade():
    app.logger.debug('** SWING_CMS ** - AcercaDe')
    return render_template('acercade.html')


@home.route('/home/')
def _home():
    app.logger.debug('** SWING_CMS ** - Home')
    return render_template('home.html')


@home.route('/politicaprivacidad/')
def _politicaprivacidad():
    app.logger.debug('** SWING_CMS ** - PoliticaPrivacidad')
    return render_template('politicaprivacidad.html')


@home.route('/reports/')
def _reportes():
    app.logger.debug('** SWING_CMS ** - Reportes')
    return render_template('reports.html')


# @home.route('/sendSMS/', methods = ['POST'])
# def _sendsms():
#     app.logger.debug('** SWING_CMS ** - Send WhatsApp SMS')
#     try:
#         url = "https://api.wassenger.com/v1/messages"

#         payloadNumbers = ["+12023231111"]

#         for number in payloadNumbers:
#             payloadMedia = {
#                 "phone": number,
#                 "media": {
#                     "file": "606d579347e544420b3dd1c5"
#                 },
#                 "message": "Estamos aquí para apoyarte. Si ves alguna de estas señales, contáctanos por teléfono o escríbenos por WhatsApp, de Lunes a Viernes de 7:30am a 3:00pm, a este número: https://wa.me/50374934298"
#             }
            
#             response = requests.request("POST", url, json=payloadMedia, headers=headers)
#             print(response.text)

#             time.sleep(5)

#         return jsonify({ 'status': 200 })
#     except Exception as e:
#         app.logger.error('** SWING_CMS ** - Send WhatsApp SMS: {}'.format(e))
#         return jsonify({ 'status': 'error' })


@home.route('/sendWASMS/', methods = ['POST'])
def _sendwasms():
    app.logger.debug('** SWING_CMS ** - Send WhatsApp SMS')
    try:
        # Determine which message operation is going to be executed
        if request.method == 'POST':
            # Retrieve JSON variables
            msg_date = request.json['date']
            msg_group = request.json['group']
            msg_msgnumber = request.json['msg']
            msg_msgspeed = request.json['msgxm']
            msg_phone = request.json['phone']
            
            # General variables
            group = None
            msgsxhour = 60 * 4
            msgssleeptime = 60 / 4
            users = None
            url = "https://api.wassenger.com/v1/messages"

            # How many messages are sent every minute
            if msg_msgspeed is not None:
                if msg_msgspeed == 'm2':
                    msgsxhour = 2 * 60
                    msgssleeptime = 60 / 2
                elif msg_msgspeed == 'm3':
                    msgsxhour = 3 * 60
                    msgssleeptime = 60 / 3
                elif msg_msgspeed == 'm4':
                    msgsxhour = 4 * 60
                    msgssleeptime = 60 / 4

            # Control Group
            if msg_group == 'cg':
                group = CatalogUserTestType.query.filter_by(
                    name_short = 'ut_ctr'
                ).first()

                users = User.query.filter_by(
                    usr_tt_id = group.id
                ).order_by(
                    User.id.asc()
                ).paginate(
                    page = 1,
                    per_page = msgsxhour,
                    error_out = True
                )

            # Developer Group
            elif msg_group == 'dg':
                group = CatalogUserTestType.query.filter_by(
                    name_short = 'ut_dev'
                ).first()

                # If option is to validate WhatsApp numbers, we can check them at a rate of
                # 1 number every 2 seconds or 30 numbers every 60 seconds
                if msg_msgnumber == '3' or msg_msgnumber == '4':
                    msgsxhour = 30 * 60
                    msgssleeptime = 60 / 30
                    url = "https://api.wassenger.com/v1/numbers/exists"

                if msg_msgnumber == '1' or msg_msgnumber == '2' or msg_msgnumber == '3':
                    users = User.query.filter_by(
                        usr_tt_id = group.id
                    ).order_by(
                        User.id.asc()
                    ).paginate(
                        page = 1,
                        per_page = msgsxhour,
                        error_out = True
                    )
                elif msg_msgnumber == '4':
                    users = User.query.order_by(
                        User.id.asc()
                    ).paginate(
                        page = 1,
                        per_page = msgsxhour,
                        error_out = True
                    )
                
            # Stakeholders Group
            elif msg_group == 'sg':
                group = CatalogUserTestType.query.filter_by(
                    name_short = 'ut_stk'
                ).first()
                devgroup = CatalogUserTestType.query.filter_by(
                    name_short = 'ut_dev'
                ).first()

                # If option is to validate WhatsApp numbers, we can check them at a rate of
                # 1 number every 2 seconds or 30 numbers every 60 seconds
                if msg_msgnumber == '2':
                    msgsxhour = 30 * 60
                    msgssleeptime = 60 / 30
                    url = "https://api.wassenger.com/v1/numbers/exists"

                users = User.query.filter(
                    (User.usr_tt_id == group.id) | 
                    (User.usr_tt_id == devgroup.id)
                ).order_by(
                    User.id.asc()
                ).paginate(
                    page = 1,
                    per_page = msgsxhour,
                    error_out = True
                )
            
            # Treatment Group
            elif msg_group == 'tg':
                group = CatalogUserTestType.query.filter_by(
                    name_short = 'ut_trt'
                ).first()

                users = User.query.filter_by(
                    usr_tt_id = group.id
                ).order_by(
                    User.id.asc()
                ).paginate(
                    page = 1,
                    per_page = msgsxhour,
                    error_out = True
                )

            # payload = {"phone": "+12023231111"}

            # response = requests.request("POST", url, json=payload, headers=headers)

            # print(response.text)
            
            task = WassengerTask(users, url, msgssleeptime, '')
            task.start()

            print('*********** Function FINISHED! *************')
            return jsonify({
                'status': 200,
                'pages': (users.pages if users is not None else 0),
                'total': (users.total if users is not None else 0)
            })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Send WhatsApp SMS: {}'.format(e))
        return jsonify({ 'status': 'error' })


@home.route('/terminosdelservicio/')
def _terminosdelservicio():
    app.logger.debug('** SWING_CMS ** - TerminosDelServicio')
    return render_template('terminosdelservicio.html')


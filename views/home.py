import json, requests, threading, time

from . import auth, createCookieSession, db
from datetime import datetime as dt
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response
from flask import current_app as app
from models.models import CatalogDevices, CatalogMessages, CatalogOperationsCenter, CatalogUserTestType
from models.models import SentMessages, SentMessagesProgress, User, WebhooksResponse

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')

# Wassenger Background Task
# Configuration - API Key and Headers
class WassengerTask(threading.Thread):
    # Properties init
    def __init__(self, records, url, sleeptime, msgtype):
        threading.Thread.__init__(self)
        self.app = app._get_current_object()
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
        with self.app.app_context():
            try:
                payload = {}
                
                while True:
                    # Validate WhatsApp Number
                    if self.msgtype == 'val_wha':
                        for item in self.records.items:
                            payload['phone'] = item.phonenumber
                            
                            retries = 1
                            response = requests.request("POST", self.url, json=payload, headers=self.headers)
                            json_response = json.loads(response.text)
                            time.sleep(self.sleeptime)

                            # Try to validate the number 2 more times
                            if json_response['exists'] is not True:
                                retries = 2
                                response = requests.request("POST", self.url, json=payload, headers=self.headers)
                                json_response = json.loads(response.text)
                                time.sleep(self.sleeptime)

                                if json_response['exists'] is not True:
                                    retries = 3
                                    response = requests.request("POST", self.url, json=payload, headers=self.headers)
                                    json_response = json.loads(response.text)
                                    time.sleep(self.sleeptime)
                            
                            # Update User Information
                            usr_upd = User.query.filter(
                                User.id == item.id
                            ).first()
                            usr_upd.has_whatsapp = json_response['exists']
                            usr_upd.comments = json.dumps({ 
                                'val_wha': { 
                                    'attempts': retries,
                                    'timestamp': str(dt.now(tz.utc))
                                }
                            })

                            # Commit current data page updates
                            db.session.add(usr_upd)
                            db.session.commit()

                    if self.records.has_next:
                        self.records = self.records.next()
                    else:
                        print("********* - WassengerTask Thread Finished - *********")
                        break

            except Exception as e:
                self.app.logger.error('** SWING_CMS ** - WassengerTask Error: {}'.format(e))
                return jsonify({ 'status': 'error' })


@home.route('/')
def _index():
    app.logger.debug('** SWING_CMS ** - Index')
    return redirect(url_for('home._login'))


@home.route('/acercade/')
def _acercade():
    app.logger.debug('** SWING_CMS ** - AcercaDe')
    return render_template('acercade.html')


@home.route('/home/')
def _home():
    app.logger.debug('** SWING_CMS ** - Home')
    return render_template('home.html')


@home.route('/login/')
def _login():
    app.logger.debug('** SWING_CMS ** - Login')
    return render_template('login.html')


@home.route('/loginuser/', methods=['POST'])
def _loginuser():
    app.logger.debug('** SWING_CMS ** - Login')
    try:
        # Login Process
        # Retrieve the uid from the JWT idToken
        idToken = request.json['idToken']
        decoded_token = auth.verify_id_token(idToken)
        usremail = decoded_token['email']
        uid = decoded_token['uid'] if usremail != 'admusr@smswhapp.com' else 'SMSW-Administrator'

        # Validate Admin
        response = None
        if uid == 'SMSW-Administrator':
            response = createCookieSession(idToken, 'redirectURL', '/wsms/')
        else:
            response = createCookieSession(idToken, 'redirectURL', '/')
        
        return response

    except Exception as e:
        app.logger.error('** SWING_CMS ** - LoginUser Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


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
            msgtype = None
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
                msgtype = 'sms_ctr'

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
                msgtype = 'sms_dev'

                group = CatalogUserTestType.query.filter_by(
                    name_short = 'ut_dev'
                ).first()

                # If option is to validate WhatsApp numbers, we can check them at a rate of
                # 1 number every 2 seconds or 30 numbers every 60 seconds
                if msg_msgnumber == '3' or msg_msgnumber == '4':
                    msgtype = 'val_wha'
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
                msgtype = 'sms_stk'

                group = CatalogUserTestType.query.filter_by(
                    name_short = 'ut_stk'
                ).first()
                devgroup = CatalogUserTestType.query.filter_by(
                    name_short = 'ut_dev'
                ).first()

                # If option is to validate WhatsApp numbers, we can check them at a rate of
                # 1 number every 2 seconds or 30 numbers every 60 seconds
                if msg_msgnumber == '2':
                    msgtype = 'val_wha'
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
                msgtype = 'sms_trt'

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

            # Initiate a Background Task to execute Wassenger Operation
            task = WassengerTask(users, url, msgssleeptime, msgtype)
            task.start()

            print('*********** Function SendWASMS Finalized! *************')
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


@home.route('/wsms/')
def _wsms():
    app.logger.debug('** SWING_CMS ** - WhatsApp SMS')
    return render_template('wassenger.html')


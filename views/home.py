import json, requests, threading, time

from . import auth, createCookieSession, db
from datetime import datetime as dt
from datetime import time as tm
from datetime import timedelta as td
from datetime import timezone as tz
from flask import Blueprint, redirect, render_template, request, url_for, jsonify, make_response
from flask import current_app as app
from models.models import CatalogDevices, CatalogMessages, CatalogOperationsCenter, CatalogUserTestType
from models.models import SentMessages, SentMessagesProgress, User, WebhooksResponse
from sqlalchemy.orm.attributes import flag_modified

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')

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

            print(request.json)

            # General variables
            group = None
            msgphoneid = None
            msgsxhour = 60 * 4
            msgssleeptime = 60 / 4
            msgtype = None
            response = None
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
            
            # Get Phone Number Wassenger Device ID
            if msg_phone is not None:
                device = None
                
                if msg_phone == 't1':
                    device = CatalogDevices.query.filter_by(
                        name_short = 'dv_ctr'
                    ).first()
                elif msg_phone == 't2':
                    device = CatalogDevices.query.filter_by(
                        name_short = 'dv_trt'
                    ).first()

                msgphoneid = device.wid

            # Control Group
            if msg_group == 'cg':
                msgtype = 'sms_ctr'

                group = CatalogUserTestType.query.filter_by(
                    name_short = 'ut_ctr'
                ).first()
                stkgroup = CatalogUserTestType.query.filter_by(
                    name_short = 'ut_stk'
                ).first()

                users = User.query.filter(
                    (
                        (User.usr_tt_id == group.id) |
                        (User.usr_tt_id == stkgroup.id)
                    ) &
                    (User.enabled == True) &
                    (User.said_stop == False) &
                    (User.has_whatsapp == True)
                ).order_by(
                    User.name.asc()
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
                # 1 number every 4 seconds or 15 numbers every 60 seconds
                if msg_msgnumber == '3' or msg_msgnumber == '4':
                    msgtype = 'val_wha'
                    msgsxhour = 30 * 60
                    msgssleeptime = 60 / 15
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
                        User.name.asc()
                    ).paginate(
                        page = 1,
                        per_page = msgsxhour,
                        error_out = True
                    )
                elif msg_msgnumber == '5' or msg_msgnumber == '6':
                    # Control Or Treatment Group
                    cotgroup = None
                    if msg_msgnumber == '5':
                        cotgroup = CatalogUserTestType.query.filter_by(
                            name_short = 'ut_ctr'
                        ).first()
                    elif msg_msgnumber == '6':
                        cotgroup = CatalogUserTestType.query.filter_by(
                            name_short = 'ut_trt'
                        ).first()
                    
                    stkgroup = CatalogUserTestType.query.filter_by(
                        name_short = 'ut_stk'
                    ).first()

                    users = User.query.filter(
                        (
                            (User.usr_tt_id == cotgroup.id) |
                            (User.usr_tt_id == stkgroup.id)
                        ) &
                        (User.enabled == True) &
                        (User.said_stop == False) &
                        (User.has_whatsapp == True)
                    ).order_by(
                        User.name.asc()
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
                    msgssleeptime = 60 / 15
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
                stkgroup = CatalogUserTestType.query.filter_by(
                    name_short = 'ut_stk'
                ).first()

                users = User.query.filter(
                    (
                        (User.usr_tt_id == group.id) |
                        (User.usr_tt_id == stkgroup.id)
                    ) &
                    (User.enabled == True) &
                    (User.said_stop == False) &
                    (User.has_whatsapp == True)
                ).order_by(
                    User.name.asc()
                ).paginate(
                    page = 1,
                    per_page = msgsxhour,
                    error_out = True
                )

            response = jsonify({
                'status': 200,
                'pages': (users.pages if users is not None else 0),
                'total': (users.total if users is not None else 0)
            })
            print('*********** Function SendWASMS Finalized! *************')

            # Initiate a Background Task to execute Wassenger Operation
            task = WassengerTask(users, url, msgssleeptime, msgtype, msg_msgnumber, msgphoneid)
            task.start()

            return  response
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Send WhatsApp SMS: {}'.format(e))
        return jsonify({ 'status': 'error' })


@home.route('/smswh/', methods = ['POST'])
def _smswh():
    app.logger.debug('** SWING_CMS ** - WebHooks')
    response = jsonify({ 'status': 'success' })
    try:
        phone = None
        js = request.json

        if 'event' in js and js['event'] == 'message:in:new':
            if 'data' in js:
                if 'fromNumber' in js['data']:
                    phone = js['data']['fromNumber']
                
                    if 'body' in js['data']:
                        msg = js['data']['body']
                        msg = msg.strip().upper()

                        if msg == 'PARA':
                            user = User.query.filter_by(
                                phonenumber = phone
                            ).first()
                            
                            user.said_stop = True
                            
                            db.session.commit()

        elif 'data' in js and 'toNumber' in js['data']:
            phone = js['data']['toNumber']

        wh = WebhooksResponse(
            phonenumber = phone,
            msg_webhook_response = js,
            date_webhook_response = dt.now(tz.utc)
        )
        db.session.add(wh)
        db.session.commit()

    except Exception as e:
        app.logger.error('** SWING_CMS ** - WebHooks: {}'.format(e))
        response = jsonify({ 'status': 'error' })
    return response, 202


@home.route('/terminosdelservicio/')
def _terminosdelservicio():
    app.logger.debug('** SWING_CMS ** - TerminosDelServicio')
    return render_template('terminosdelservicio.html')


@home.route('/wsms/')
def _wsms():
    app.logger.debug('** SWING_CMS ** - WhatsApp SMS')
    return render_template('wassenger.html')


# **************************************************************************
# Utilities
# **************************************************************************

# Wassenger Utilities
def _isNowTimeValid(startTime, endTime, nowTime = dt.now().time()):
    # Validate Same Day Range
    if startTime < endTime: 
        return nowTime >= startTime and nowTime <= endTime 
    # Validate Midnight Range
    else: 
        return nowTime >= startTime or nowTime <= endTime 

def _returnMessagesRecords(msggroup, msgnumber):
    try:
        records = None

        # Control and Treatment Group Messages
        if msggroup == 'sms_ctr' or msggroup == 'sms_trt':
            msgid = 'msg_ctr_' if msggroup == 'sms_ctr' else 'msg_trt_'

            msgid == (msgid + '0' + msgnumber) if len(msgnumber) == 1 else (msgid + msgnumber)
            
            records = CatalogMessages.query.filter(
                (CatalogMessages.name_short == msgid) &
                (CatalogMessages.enabled == True)
            ).all()
        
        # Developer Group Messages
        elif msggroup == 'sms_dev':
            if msgnumber == '1' or msgnumber == '5' or msgnumber == '6':
                records = CatalogMessages.query.filter(
                    (CatalogMessages.name_short == 'msg_w') &
                    (CatalogMessages.enabled == True)
                ).all()
            elif msgnumber == '2':
                records = CatalogMessages.query.filter(
                    (CatalogMessages.enabled == True)
                ).all()
        
        # Stakeholders Group Messages
        elif msggroup == 'sms_stk':
            if msgnumber == '1':
                records = CatalogMessages.query.filter(
                    (CatalogMessages.enabled == True)
                ).all()
        
        return records
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Return Messages Records: {}'.format(e))
        return jsonify({ 'status': 'error' })


def _returnResponseJSON(res):
    response = {}
    if res is not None:
        if hasattr(res, 'text') and res.text is not None:
            try:
                response = json.loads(res.text)
            except ValueError as e:
                app.logger.error('** SWING_CMS ** - Return Response JSON: {}'.format(e))
                response = { 'exists': False }
                print(res.text)
                time.sleep(30)
    return response

# Wassenger Background Task
# Configuration - API Key and Headers
class WassengerTask(threading.Thread):
    # Properties init
    def __init__(self, users, url, sleeptime, msgtype, msgnumber, deviceid):
        threading.Thread.__init__(self)
        self.app = app._get_current_object()
        self.device = deviceid
        self.headers = {
            "Content-Type": "application/json",
            "Token": app.config['WASS_API_KEY']
        }
        self.msglist = None
        self.msgnumber = msgnumber
        self.msgtype = msgtype
        self.progressid = None
        self.sleeptime = sleeptime
        self.url = url
        self.userlist = users
    
    # Thread activity task
    def run(self, *args, **kwargs):
        with self.app.app_context():
            try:
                payload = {}
                
                while True:
                     # Send Message
                    if self.msgtype != 'val_wha':
                        # Retrieve Messages List
                        if self.msglist is None:
                            self.msglist = _returnMessagesRecords(self.msgtype, self.msgnumber)

                        for msg in self.msglist:
                            payload = {}

                            if msg.media_pic is not None:
                                payload['media'] = { 'file': msg.media_pic}
                            
                            if self.device is not None:
                                payload['device'] = self.device

                            userlist = self.userlist.items
                            for user in userlist:
                                # Validate if it's not Valid Sending Hours
                                # if not _isNowTimeValid(tm(7,30), tm(16,45), dt.now().time()):
                                #     # Pause for 10 minutes until Valid Sending Hours
                                #     while True:
                                #         time.sleep(600)
                                #         print(self.msgtype + ' - ' + self.msgnumber + ' - ' + ' Not Valid Hours.')
                                #         if _isNowTimeValid(tm(7,30), tm(16,45), dt.now().time()):
                                #             break
                                
                                u_msg = msg.message

                                if '[[telnum]]' in u_msg:
                                    wa_link = 'https://wa.me/'
                                    tel_num = user.op_center.phonenumber
                                    wa_link = wa_link + tel_num.replace('+','')
                                    u_msg = u_msg.replace('[[telnum]]', wa_link)
                                
                                if '[[oprctr]]' in u_msg:
                                    u_msg = u_msg.replace('[[oprctr]]', user.op_center.name)
                                
                                payload['message'] = u_msg
                                payload['phone'] = user.phonenumber

                                sent_msg = SentMessages(
                                    usr_id = user.id,
                                    msg_id = msg.id,
                                    msg_request = json.dumps(payload)
                                )
                                
                                # response = requests.request("POST", self.url, json=payload, headers=self.headers)
                                
                                # sent_msg.msg_response = _returnResponseJSON(response)
                                # sent_msg.date_response = dt.now(tz.utc)
                                # db.session.add(sent_msg)
                                
                                # # Update Sent Message Progress Record
                                # if self.progressid is not None:
                                #     self.progressid.msg_last_usr = json.dumps({
                                #             'uid': user.id,
                                #             'uname': user.name,
                                #             'uphone': user.phonenumber
                                #     })
                                #     self.progressid.msg_sent_detail = json.dumps(payload)
                                #     self.progressid.msg_sent_amount += 1
                                #     flag_modified(self.progressid, 'msg_last_usr')
                                #     flag_modified(self.progressid, 'msg_sent_detail')
                                
                                # # Create Sent Message Progress Record
                                # else:
                                #     self.progressid = SentMessagesProgress(
                                #         msg_last_usr = json.dumps({
                                #             'uid': user.id,
                                #             'uname': user.name,
                                #             'uphone': user.phonenumber
                                #         }),
                                #         msg_sent_detail = json.dumps(payload),
                                #         msg_sent_amount = 1
                                #     )
                                #     db.session.add(self.progressid)
                                
                                # db.session.commit()
                                # db.session.refresh(self.progressid)
                                
                                print(user.name)
                                time.sleep(self.sleeptime)
                                
                    # Validate WhatsApp Number
                    elif self.msgtype == 'val_wha':
                        for user in self.userlist.items:
                            payload['phone'] = user.phonenumber
                            
                            retries = 1
                            # response = requests.request("POST", self.url, json=payload, headers=self.headers)
                            # json_response = _returnResponseJSON(response)
                            # time.sleep(self.sleeptime)

                            # # Try to validate the number 2 more times
                            # if 'exists' in json_response and json_response['exists'] is not True:
                            #     retries = 2
                            #     response = requests.request("POST", self.url, json=payload, headers=self.headers)
                            #     json_response = _returnResponseJSON(response)
                            #     time.sleep(self.sleeptime)

                            #     if 'exists' in json_response and json_response['exists'] is not True:
                            #         retries = 3
                            #         response = requests.request("POST", self.url, json=payload, headers=self.headers)
                            #         json_response = _returnResponseJSON(response)
                            #         time.sleep(self.sleeptime)
                            
                            # # Update User Information
                            # usr_upd = User.query.filter(
                            #     User.id == user.id
                            # ).first()
                            # usr_upd.has_whatsapp = json_response['exists'] if 'exists' in json_response else False
                            # usr_upd.comments = json.dumps({ 
                            #     'val_wha': { 
                            #         'attempts': retries,
                            #         'status': response.status_code if response is not None else 410,
                            #         'timestamp': str(dt.now(tz.utc))
                            #     }
                            # })

                            # # Commit current data page updates
                            # db.session.add(usr_upd)
                            # db.session.commit()

                    
                    if self.userlist.has_next:
                        self.userlist = self.userlist.next()
                    else:
                        if self.progressid is not None:
                            self.progressid.msg_sent_completed = True
                            db.session.commit()
                        
                        print("********* - WassengerTask Thread Finished - *********")
                        break

            except Exception as e:
                self.app.logger.error('** SWING_CMS ** - WassengerTask Error: {}'.format(e))
                return jsonify({ 'status': 'error' })

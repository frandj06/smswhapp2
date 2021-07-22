from flask import current_app as app
from flask import jsonify
from models import *

# -----------------------------------------------------------------------------------------------------
# DATABASE MINIMUM REQUIRED DATA
# POPULATION FUNCTIONS
# -----------------------------------------------------------------------------------------------------

# Initialize Database Populate Function
def initPopulateDB():
    populateOperationsCenters()

    populateUserTypes()

    populateMessages()

    populateDevices()

    app.logger.info('** SWING_CMS ** - Populate Database FINISHED.')


# Populate Devices
def populateDevices():
    try:
        app.logger.debug('** SWING_CMS ** - Populate Devices')

        dev_ctr = CatalogDevices(
            wid = '60818e5fa6f763c2431996d2',
            name = '+503 7684 2455 - Control',
            name_short = 'dv_ctr',
            phonenumber = '+50376842455'
        )
        db.session.add(dev_ctr)

        dev_trt = CatalogDevices(
            wid = '60f98df1c28aed43ced3ac44',
            name = '+503 7684 8930 - Tratamiento',
            name_short = 'dv_trt',
            phonenumber = '+50376848930'
        )
        db.session.add(dev_trt)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Devices: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate Messages
def populateMessages():
    try:
        app.logger.debug('** SWING_CMS ** - Populate Messages')

        msg_bienvenida = (
            '¡Hola! Te saludamos desde Ciudad Mujer. Queremos aprender como mejorar la comunicación con nuestras usuarias. '
            'Tú has sido seleccionada para recibir nuestro nuevos mensajes de WhatsApp. En las próximas semanas, te estaremos '
            'enviando mensajes sobre distintos temas que tienen que ver con tu bienestar personal y familiar.\n\nSi en algún momento '
            'quieres dejar de recibir estos mensajes puedes enviar la palabra *PARA* en este chat en cualquier momento.\n\nEn tu Centro '
            'de Ciudad Mujer estamos listas para escucharte, apoyarte y guiarte sobre nuestros servicios.\n\nPuedes llamarnos o escribirnos '
            'por WhatsApp a este número:\n\n[[telnum]]\n\nTu Centro Ciudad Mujer [[oprctr]]'
        )

        msg_experimento = (
            'Estamos aquí para apoyarte. Si ves alguna de estas señales, contáctanos por teléfono o escríbenos por WhatsApp, de Lunes a '
            'Viernes de 7:30am a 3:00pm, a este número:\n\n[[telnum]]\n\nRecuerda que en cualquier momento puedes enviar la palabra *PARA* '
            'si quieres dejar de recibir nuestros mensajes.'
        )

        usr_tt_ctr = CatalogUserTestType.query.filter_by(name_short='ut_ctr').first()
        usr_tt_trt = CatalogUserTestType.query.filter_by(name_short='ut_trt').first()

        msg_w = CatalogMessages(
            name = 'Mensaje de bienvenida',
            name_short = 'msg_w',
            message = msg_bienvenida
        )
        db.session.add(msg_w)

        msg_ctr_01 = CatalogMessages(
            name = 'Control - Mensaje 01',
            name_short = 'msg_ctr_01',
            message = msg_experimento,
            usr_tt_id = usr_tt_ctr.id,
            media_pic = '606d56f09e56c362922b8b1b'
        )
        db.session.add(msg_ctr_01)

        msg_ctr_02 = CatalogMessages(
            name = 'Control - Mensaje 02',
            name_short = 'msg_ctr_02',
            message = msg_experimento,
            usr_tt_id = usr_tt_ctr.id,
            media_pic = '606d57681a8bf59cd8134658'
        )
        db.session.add(msg_ctr_02)

        msg_ctr_03 = CatalogMessages(
            name = 'Control - Mensaje 03',
            name_short = 'msg_ctr_03',
            message = msg_experimento,
            usr_tt_id = usr_tt_ctr.id,
            media_pic = '606d5777f0afa8210a2bb916'
        )
        db.session.add(msg_ctr_03)

        msg_trt_01 = CatalogMessages(
            name = 'Tratamiento - Mensaje 01',
            name_short = 'msg_trt_01',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d579347e544420b3dd1c5'
        )
        db.session.add(msg_trt_01)

        msg_trt_02 = CatalogMessages(
            name = 'Tratamiento - Mensaje 02',
            name_short = 'msg_trt_02',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d57bf8a174c05fbd0031e'
        )
        db.session.add(msg_trt_02)

        msg_trt_03 = CatalogMessages(
            name = 'Tratamiento - Mensaje 03',
            name_short = 'msg_trt_03',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d57d21dcce1c72447e455'
        )
        db.session.add(msg_trt_03)

        msg_trt_04 = CatalogMessages(
            name = 'Tratamiento - Mensaje 04',
            name_short = 'msg_trt_04',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d57df9b27b0fdfe55fe50'
        )
        db.session.add(msg_trt_04)

        msg_trt_05 = CatalogMessages(
            name = 'Tratamiento - Mensaje 05',
            name_short = 'msg_trt_05',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d57ef58a3a1821b1b6716'
        )
        db.session.add(msg_trt_05)

        msg_trt_06 = CatalogMessages(
            name = 'Tratamiento - Mensaje 06',
            name_short = 'msg_trt_06',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d57fc1a8bf5f16213701f'
        )
        db.session.add(msg_trt_06)

        msg_trt_07 = CatalogMessages(
            name = 'Tratamiento - Mensaje 07',
            name_short = 'msg_trt_07',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d580d370b535551e20aed'
        )
        db.session.add(msg_trt_07)

        msg_trt_08 = CatalogMessages(
            name = 'Tratamiento - Mensaje 08',
            name_short = 'msg_trt_08',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d581c58a3a115741b6fec'
        )
        db.session.add(msg_trt_08)

        msg_trt_09 = CatalogMessages(
            name = 'Tratamiento - Mensaje 09',
            name_short = 'msg_trt_09',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d582e1a8bf50e63137a1c'
        )
        db.session.add(msg_trt_09)

        msg_trt_10 = CatalogMessages(
            name = 'Tratamiento - Mensaje 10',
            name_short = 'msg_trt_10',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d583f43050858682a9e47'
        )
        db.session.add(msg_trt_10)

        msg_trt_11 = CatalogMessages(
            name = 'Tratamiento - Mensaje 11',
            name_short = 'msg_trt_11',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d5850b6de204cac58536d'
        )
        db.session.add(msg_trt_11)

        msg_trt_12 = CatalogMessages(
            name = 'Tratamiento - Mensaje 12',
            name_short = 'msg_trt_12',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d586d919bc6355b1cda7d'
        )
        db.session.add(msg_trt_12)

        msg_trt_13 = CatalogMessages(
            name = 'Tratamiento - Mensaje 13',
            name_short = 'msg_trt_13',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d587bce20af22b9649a92'
        )
        db.session.add(msg_trt_13)

        msg_trt_14 = CatalogMessages(
            name = 'Tratamiento - Mensaje 14',
            name_short = 'msg_trt_14',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d5889faa7a512ab23469e'
        )
        db.session.add(msg_trt_14)

        msg_trt_15 = CatalogMessages(
            name = 'Tratamiento - Mensaje 15',
            name_short = 'msg_trt_15',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d589d58a3a1083e1b8f59'
        )
        db.session.add(msg_trt_15)

        msg_trt_16 = CatalogMessages(
            name = 'Tratamiento - Mensaje 16',
            name_short = 'msg_trt_16',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '606d58b847e54438543e2df1'
        )
        db.session.add(msg_trt_16)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Messages: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate Operations Centers
def populateOperationsCenters():
    try:
        app.logger.debug('** SWING_CMS ** - Populate Operations Centers')
        
        oc_lou = CatalogOperationsCenter(
            name = 'Lourdes Colón',
            name_short = 'C_LOU',
            phonenumber = '+50374933204'
        )
        db.session.add(oc_lou)

        oc_mor = CatalogOperationsCenter(
            name = 'Morazán',
            name_short = 'C_MOR',
            phonenumber = '+50374934298'
        )
        db.session.add(oc_mor)

        oc_saa = CatalogOperationsCenter(
            name = 'Santa Ana',
            name_short = 'C_SAA',
            phonenumber = '+50372811860'
        )
        db.session.add(oc_saa)

        oc_sma = CatalogOperationsCenter(
            name = 'San Martín',
            name_short = 'C_SMA',
            phonenumber = '+50372867368'
        )
        db.session.add(oc_sma)

        oc_smi = CatalogOperationsCenter(
            name = 'San Miguel',
            name_short = 'C_SMI',
            phonenumber = '+50372567341'
        )
        db.session.add(oc_smi)

        oc_usu = CatalogOperationsCenter(
            name = 'Usulután',
            name_short = 'C_USU',
            phonenumber = '+50372566787'
        )
        db.session.add(oc_usu)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Operations Centers: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate User Test Types
def populateUserTypes():
    try:
        app.logger.debug('** SWING_CMS ** - Populate User Test Types')

        ut_ctr = CatalogUserTestType(
            name = 'Control',
            name_short = 'ut_ctr'
        )
        db.session.add(ut_ctr)

        ut_dev = CatalogUserTestType(
            name = 'Development',
            name_short = 'ut_dev'
        )
        db.session.add(ut_dev)

        ut_stk = CatalogUserTestType(
            name = 'Stakeholder',
            name_short = 'ut_stk'
        )
        db.session.add(ut_stk)

        ut_trt = CatalogUserTestType(
            name = 'Tratamiento',
            name_short = 'ut_trt'
        )
        db.session.add(ut_trt)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate User Test Types: {}'.format(e))
        return jsonify({ 'status': 'error' })

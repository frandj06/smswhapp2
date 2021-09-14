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
            '👋 Estamos aquí para apoyarte. Si ves alguna de estas señales, RESPONDE a este mensaje, y te atenderemos de L-V de 7:30am a 3:00pm.\n\n'
            'Si quieres dejar de recibir nuestros mensajes, escribe la palabra *PARA*.\n\n'
            '👀 Recuerda eliminar los mensajes luego de leerlos, con la flechita a la derecha del mensaje 🔽.'
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
            media_pic = '611142de122780dffb033c01'
        )
        db.session.add(msg_ctr_01)

        msg_ctr_02 = CatalogMessages(
            name = 'Control - Mensaje 02',
            name_short = 'msg_ctr_02',
            message = msg_experimento,
            usr_tt_id = usr_tt_ctr.id,
            media_pic = '61114314c9b42e2d31d5303a'
        )
        db.session.add(msg_ctr_02)

        msg_ctr_03 = CatalogMessages(
            name = 'Control - Mensaje 03',
            name_short = 'msg_ctr_03',
            message = msg_experimento,
            usr_tt_id = usr_tt_ctr.id,
            media_pic = '611143260b3aff7827f2a057'
        )
        db.session.add(msg_ctr_03)

        msg_trt_01 = CatalogMessages(
            name = 'Tratamiento - Mensaje 01',
            name_short = 'msg_trt_01',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '61114366706a2b081decedaa'
        )
        db.session.add(msg_trt_01)

        msg_trt_02 = CatalogMessages(
            name = 'Tratamiento - Mensaje 02',
            name_short = 'msg_trt_02',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '611143bee878d59ace1ecb6c'
        )
        db.session.add(msg_trt_02)

        msg_trt_03 = CatalogMessages(
            name = 'Tratamiento - Mensaje 03',
            name_short = 'msg_trt_03',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '611143ed91fe7c4f1c00191c'
        )
        db.session.add(msg_trt_03)

        msg_trt_04 = CatalogMessages(
            name = 'Tratamiento - Mensaje 04',
            name_short = 'msg_trt_04',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '6111440c0b3aff21cdf2e8eb'
        )
        db.session.add(msg_trt_04)

        msg_trt_05 = CatalogMessages(
            name = 'Tratamiento - Mensaje 05',
            name_short = 'msg_trt_05',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '611144352bf65b64b38907a2'
        )
        db.session.add(msg_trt_05)

        msg_trt_06 = CatalogMessages(
            name = 'Tratamiento - Mensaje 06',
            name_short = 'msg_trt_06',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '6111445a1227806c1703b258'
        )
        db.session.add(msg_trt_06)

        msg_trt_07 = CatalogMessages(
            name = 'Tratamiento - Mensaje 07',
            name_short = 'msg_trt_07',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '611144712bf65b0bbd891a08'
        )
        db.session.add(msg_trt_07)

        msg_trt_08 = CatalogMessages(
            name = 'Tratamiento - Mensaje 08',
            name_short = 'msg_trt_08',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '6111448a4ebad2c4b0bf2a55'
        )
        db.session.add(msg_trt_08)

        msg_trt_09 = CatalogMessages(
            name = 'Tratamiento - Mensaje 09',
            name_short = 'msg_trt_09',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '6111449de878d50ac81f089e'
        )
        db.session.add(msg_trt_09)

        msg_trt_10 = CatalogMessages(
            name = 'Tratamiento - Mensaje 10',
            name_short = 'msg_trt_10',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '611144b4eb9b621a62c9014c'
        )
        db.session.add(msg_trt_10)

        msg_trt_11 = CatalogMessages(
            name = 'Tratamiento - Mensaje 11',
            name_short = 'msg_trt_11',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '611144c8086b264cd7f1bc9b'
        )
        db.session.add(msg_trt_11)

        msg_trt_12 = CatalogMessages(
            name = 'Tratamiento - Mensaje 12',
            name_short = 'msg_trt_12',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '611144deacb6cd3bbab2abd2'
        )
        db.session.add(msg_trt_12)

        msg_trt_13 = CatalogMessages(
            name = 'Tratamiento - Mensaje 13',
            name_short = 'msg_trt_13',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '611144eac9b42e21fad5b965'
        )
        db.session.add(msg_trt_13)

        msg_trt_14 = CatalogMessages(
            name = 'Tratamiento - Mensaje 14',
            name_short = 'msg_trt_14',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '61114510464e42588fe1c47f'
        )
        db.session.add(msg_trt_14)

        msg_trt_15 = CatalogMessages(
            name = 'Tratamiento - Mensaje 15',
            name_short = 'msg_trt_15',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '611145264ebad29b7abf572d'
        )
        db.session.add(msg_trt_15)

        msg_trt_16 = CatalogMessages(
            name = 'Tratamiento - Mensaje 16',
            name_short = 'msg_trt_16',
            message = msg_experimento,
            usr_tt_id = usr_tt_trt.id,
            media_pic = '61114541c65e2c5dfae07edf'
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

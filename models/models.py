from datetime import datetime as dt
from datetime import timezone as tz
from flask_sqlalchemy import SQLAlchemy

# **************************************************************************
# SQLAlchemy init instances
# **************************************************************************

db = SQLAlchemy()


# **************************************************************************
# Database Models
# **************************************************************************

# Catalog - Devices Class
class CatalogDevices(db.Model):
    __tablename__ = 'catalog_devices'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wid = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(60), unique=True, nullable=False)
    name_short = db.Column(db.String(6), unique=True, nullable=True)
    phonenumber = db.Column(db.String(20), nullable=True)
    enabled = db.Column(db.Boolean, nullable=True, default=True)


# Catalog - Messages Class
class CatalogMessages(db.Model):
    __tablename__ = 'catalog_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    name_short = db.Column(db.String(10), unique=True, nullable=True)
    message = db.Column(db.Text, nullable=True)
    media_pic = db.Column(db.String(100), nullable=True)
    media_audio = db.Column(db.String(100), nullable=True)
    enabled = db.Column(db.Boolean, nullable=True, default=True)
    usr_tt_id = db.Column(db.Integer, db.ForeignKey('catalog_user_test_type.id'), nullable=True)
    smsg_msg = db.relationship('SentMessages', lazy='subquery', back_populates='s_msg_msg')
    test_type = db.relationship('CatalogUserTestType', lazy='subquery', back_populates='msg_test_type')


# Catalog - Operations Center Class
class CatalogOperationsCenter(db.Model):
    __tablename__ = 'catalog_operations_center'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    name_short = db.Column(db.String(6), unique=True, nullable=True)
    phonenumber = db.Column(db.String(20), nullable=True)
    enabled = db.Column(db.Boolean, nullable=True, default=True)
    usr_op_cnt = db.relationship('User', lazy='subquery', back_populates='op_center')


# Catalog - User Test Type Class
class CatalogUserTestType(db.Model):
    __tablename__ = 'catalog_user_test_type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    name_short = db.Column(db.String(6), unique=True, nullable=True)
    enabled = db.Column(db.Boolean, nullable=True, default=True)
    usr_test_type = db.relationship('User', lazy='subquery', back_populates='test_type')
    msg_test_type = db.relationship('CatalogMessages', lazy='subquery', back_populates='test_type')


# Sent Messages Class
class SentMessages(db.Model):
    __tablename__ = 'sent_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usr_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    msg_id = db.Column(db.Integer, db.ForeignKey('catalog_messages.id'), nullable=False)
    msg_request = db.Column(db.JSON, nullable=True)
    date_request = db.Column(db.DateTime, unique=False, nullable=False, index=True, default=dt.now(tz.utc))
    msg_response = db.Column(db.JSON, nullable=True)
    date_response = db.Column(db.DateTime, unique=False, nullable=True, index=True, default=dt.now(tz.utc))
    msg_usr_reply = db.Column(db.JSON, nullable=True)
    date_usr_reply = db.Column(db.DateTime, unique=False, nullable=True, index=True, default=dt.now(tz.utc))
    s_msg_usr = db.relationship('User', lazy='subquery', back_populates='smsg_usr')
    s_msg_msg = db.relationship('CatalogMessages', lazy='subquery', back_populates='smsg_msg')


# Sent Messages Progress Class
class SentMessagesProgress(db.Model):
    __tablename__ = 'sent_messages_progress'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    msg_last_usr = db.Column(db.JSON, nullable=False)
    msg_sent_detail = db.Column(db.JSON, nullable=False)
    msg_sent_amount = db.Column(db.Integer, nullable=False, default=0)
    msg_sent_completed = db.Column(db.Boolean, nullable=False, default=False)


# User Class
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(300), nullable=True)
    phonenumber = db.Column(db.String(20), nullable=True)
    enabled = db.Column(db.Boolean, nullable=True, default=True)
    comments = db.Column(db.JSON, nullable=True)
    said_stop = db.Column(db.Boolean, nullable=True, default=True)
    has_whatsapp = db.Column(db.Boolean, nullable=True, default=True)
    usr_tt_id = db.Column(db.Integer, db.ForeignKey('catalog_user_test_type.id'), nullable=True)
    op_cnt_id = db.Column(db.Integer, db.ForeignKey('catalog_operations_center.id'), nullable=True)
    smsg_usr = db.relationship('SentMessages', lazy='subquery', back_populates='s_msg_usr')
    test_type = db.relationship('CatalogUserTestType', lazy='subquery', back_populates='usr_test_type')
    op_center = db.relationship('CatalogOperationsCenter', lazy='subquery', back_populates='usr_op_cnt')


# Webhooks Response Class
class WebhooksResponse(db.Model):
    __tablename__ = 'webhooks_response'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phonenumber = db.Column(db.String(20), nullable=True)
    msg_webhook_response = db.Column(db.JSON, nullable=True)
    date_webhook_response = db.Column(db.DateTime, unique=False, nullable=True, index=True, default=dt.now(tz.utc))

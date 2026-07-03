from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    role = db.Column(db.String(20))
    zone_id = db.Column(db.Integer, db.ForeignKey('zone.id'))

class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    pincodes = db.Column(db.String(200))

class RateCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_type = db.Column(db.String(10))
    intra_zone_rate = db.Column(db.Float)
    inter_zone_rate = db.Column(db.Float)
    cod_surcharge = db.Column(db.Float)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    pickup_pincode = db.Column(db.String(10))
    drop_pincode = db.Column(db.String(10))
    weight_actual = db.Column(db.Float)
    weight_volumetric = db.Column(db.Float)
    final_charge = db.Column(db.Float)
    status = db.Column(db.String(20), default='Pending')
    order_type = db.Column(db.String(10))
    payment_type = db.Column(db.String(10))

class OrderHistory(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    status = db.Column(db.String(50))
    updated_by = db.Column(db.String(50))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
# pylint: disable= C0116,C0114,C0115
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    lastname = db.Column(db.String(80), unique=False, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.Enum('customer', 'barber', 'admin', name='user_roles'), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    appointments = db.relationship('Appointment', foreign_keys='Appointment.customer_id', back_populates='customer')
    barber_appointments = db.relationship('Appointment', foreign_keys='Appointment.barber_id', back_populates='barber')

    def __repr__(self):
        return f'<User {self.id} {self.name} {self.lastname}>'
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# class BarberProfile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
#     barber_shop_id = db.Column(db.Integer, db.ForeignKey('barber_shop.id'), nullable=False)
#     specialties = db.Column(db.String)
#     rating = db.Column(db.Float)
#     user = db.relationship('User', back_populates='barber_profile')
#     barber_shop = db.relationship('BarberShop', back_populates='barbers')
#     appointments = db.relationship('Appointment', back_populates='barber')
#     availabilities = db.relationship('Availability', back_populates='barber')

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # Adjusted String length
    description = db.Column(db.Text)  # Changed to Text for potentially longer descriptions
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Use SQLAlchemy's function for current timestamp
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    barber_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('service.id'), nullable=False)
    appointment_time = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    status = db.Column(db.Enum('scheduled', 'completed', 'cancelled', name='appointment_statuses'), default='scheduled')
    customer = db.relationship('User', foreign_keys=[customer_id], back_populates='appointments')
    barber = db.relationship('User', foreign_keys=[barber_id], back_populates='barber_appointments')
    service = db.relationship('Service')

# class Availability(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     barber_id = db.Column(db.Integer, db.ForeignKey('barber_profile.id'), nullable=False)
#     start_time = db.Column(db.DateTime, nullable=False)
#     end_time = db.Column(db.DateTime, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow())
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow())
#     barber = db.relationship('BarberProfile', back_populates='availabilities')

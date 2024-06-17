# pylint: disable= C0116,C0114,C0115,W0612
""" Backend testing app to interface with angular frontend"""
import secrets
from flask import Flask, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_restx import Resource, Api, fields
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from models import User, db, Appointment, Service, Availability
from datetime import datetime, timedelta



def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = secrets.token_hex(16)
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIOapi"] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["JWT_SECRET_KEY"] = secrets.token_hex(16)
    db.init_app(app)
    # Initialize JWT Manager
    jwt = JWTManager(app)
    # Create all database tables
    with app.app_context():
        db.create_all()
    return app


app = create_app()
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(app, version='v 0.69', title='Backend Testing',
          description='Can be used to test a variety of endpoints that belong to the API',
          authorizations = authorizations,
          security='Bearer',
          doc='/api/')  # Documentation URL
CORS(app)
# CORS(app, resources={r"/api/*": {"origin": "http://hair-orama.local:4200"}})


### START OF AUTH ###
auth = api.namespace('api/auth', description='Authentication operations')

login_model = api.model('Login', {
    'email': fields.String(required=True, description='The user email address'),
    'password': fields.String(required=True, description='The user password')
})

@auth.route('/login')
class LoginResource(Resource):
    @auth.doc('login_user')
    @auth.expect(login_model)
    def post(self):
        '''Authenticate a user and return a token'''
        data = request.json
        email = data.get('email')
        password = data.get('password')
        user = db.session.query(User).filter_by(email=email).first()

        if user and user.check_password(password):
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401
### END OF AUTH ###

### START OF USERS ###
user = api.namespace('api/users', description='User operations')

user_model = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The user unique identifier'),
    'name': fields.String(required=True, description='The user first name'),
    'lastname': fields.String(required=True, description='The user last name'),
    'password_hash': fields.String(required=True, description='The user password hash'),
    'email': fields.String(required=True, description='The user email address'),
    'role': fields.String(required=True, description='The user role', enum=['customer', 'barber', 'admin']),
    'created_at': fields.DateTime(readOnly=True, description='The user creation date'),
    'updated_at': fields.DateTime(readOnly=True, description='The user last update date'),
})

user_get_model = api.model('UserGet', {
    'name': fields.String(required=True, description='The user first name'),
    'lastname': fields.String(required=True, description='The user last name'),
    'email': fields.String(required=True, description='The user email address'),
    'role': fields.String(required=True, description='The user role', enum=['customer', 'barber', 'admin']),
})

user_create_model = api.model('UserCreate', {
    'name': fields.String(required=True, description='The user first name'),
    'lastname': fields.String(required=True, description='The user last name'),
    'password_hash': fields.String(required=True, description='The user password hash'),
    'email': fields.String(required=True, description='The user email address'),
    'role': fields.String(required=True, description='The user role', enum=['customer', 'barber', 'admin']),
})

user_update_model = api.model('UserUpdate', {
    'name': fields.String(required=True, description='The user first name'),
    'lastname': fields.String(required=True, description='The user last name'),
    'password_hash': fields.String(required=True, description='The user password hash'),
    'email': fields.String(required=True, description='The user email address'),
    'role': fields.String(required=True, description='The user role', enum=['customer', 'barber', 'admin']),
})

simplified_user_model = api.model('SimplifiedUser', {
    'id': fields.Integer(readOnly=True, description='The user unique identifier'),
    'name': fields.String(required=True, description='The user first name'),
    'email': fields.String(required=True, description='The user email address'),
})




@user.route('/')
class UserResource(Resource):
    @jwt_required()
    @user.doc('list_users')
    @user.marshal_list_with(simplified_user_model)
    def get(self):
        '''Fetch all users'''
        possible_admin = db.session.get(User, get_jwt_identity())
        if possible_admin.role != "admin":
            api.abort(403, "Access forbidden")
        users = db.session.query(User).all()
        if not users:
            api.abort(404, "No users found")
        return users

    @user.doc('create_user')
    @user.expect(user_create_model)
    @user.marshal_with(user_model, code=201)
    def post(self):
        '''Create a new user'''
        data = request.json
        name = data.get('name')
        lastname = data.get('lastname')
        password = data.get('password_hash')  # This is actually the plaintext password from the request
        email = data.get('email')
        role = data.get('role')
        if not name or not lastname or not password or not email or not role:
            api.abort(400, "All fields are required")

        new_user = User(name=name, lastname=lastname, email=email, role=role)
        new_user.set_password(password)  # Hash the password
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201

    @user.doc('delete_users')
    @user.response(200, 'Users deleted successfully')
    def delete(self):
        '''Delete all users'''
        db.session.query(User).delete()
        db.session.commit()
        return {"response": "Users deleted successfully"}, 200


@user.route('/<int:user_id>')
@user.param('user_id', 'The user identifier')
class UserDetailResource(Resource):
    @jwt_required()
    @user.doc('get_user')
    @user.marshal_with(user_get_model)
    def get(self, user_id):
        '''Fetch a user given its identifier'''

        current_user = db.session.get(User, user_id)
        if not current_user:
            api.abort(400, "Error user not found")
        print(f"current user role {current_user.role}")
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            possible_admin = db.session.get(User, get_jwt_identity())
            if possible_admin.role != "admin":
                api.abort(403, "Access forbidden")
        return current_user


    @jwt_required()
    @user.doc('update_user')
    @user.expect(user_update_model)
    @user.marshal_with(user_model)
    def post(self, user_id):
        '''Update a user given its identifier'''

        current_user = db.session.get(User, user_id)
        if not current_user:
            api.abort(400, "Error user not found")

        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            possible_admin = db.session.get(User, get_jwt_identity())
            if possible_admin.role != "admin":
                api.abort(403, "Access forbidden")

        data = request.json
        try:
            current_user.name = data['name']
            current_user.lastname = data['lastname']
            if 'password_hash' in data:
                current_user.set_password(data['password_hash'])  # Hash the new password
            current_user.email = data['email']
            current_user.role = data['role']
            db.session.commit()
            return current_user, 201
        except KeyError as e:
            api.abort(400, "All fields are required")

    @jwt_required()
    @user.doc('delete_user')
    def delete(self, user_id):
        '''Delete a user given its identifier'''
        current_user = db.session.get(User, user_id)

        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            if current_user.role != "admin":
                api.abort(403, "Access forbidden")

        if not current_user:
            api.abort(400, "Error user not found")

        db.session.delete(current_user)
        db.session.commit()
        return {"response": "User deleted successfully"}, 200

### END OF USERS ###

### START OF APPOINTMENTS ###
# appoint = api.namespace('api/appointments', description='Appointment endpoint')

# get_appointments = api.model('GetAppointments', {
#     'fullname': fields.String(description='The user full name'),
#     'appointment_id': fields.Integer(description='The appointment unique identifier'),
#     'appointment_time': fields.DateTime(description='The appointment time'),
#     'status': fields.String(description='The appointment status'),
#     'barber': fields.String(description='The barber unique identifier'),
#     'service': fields.Nested(api.model('Service', {
#         'name': fields.String(description='The service name'),
#         'duration': fields.Integer(description='The service duration in minutes'),
#         'price': fields.Float(description='The service price'),
#     })),
# })

# create_appointment = api.model('CreateAppointment', {
#     'barber_id': fields.Integer(required=True, description='The barber unique identifier'),
#     'service_id': fields.Integer(required=True, description='The service unique identifier'),
#     'appointment_time': fields.DateTime(required=True,description='The appointment time'),
#     'created_at': fields.DateTime(readOnly=True, description='The user creation date'),
#     'updated_at': fields.DateTime(readOnly=True, description='The user last update date'),
#     'status': fields.String(required=True, description='The order status', enum=['scheduled', 'completed', 'cancelled'], default='scheduled'),
# })

# update_appointment = api.model('UpdateAppointment', {
#     'barber_id': fields.Integer(required=True, description='The barber unique identifier'),
#     'service_id': fields.Integer(required=True, description='The service unique identifier'),
#     'appointment_time': fields.DateTime(required=True,description='The appointment time'),
#     'created_at': fields.DateTime(readOnly=True, description='The user creation date'),
#     'updated_at': fields.DateTime(readOnly=True, description='The user last update date'),
#     'status': fields.String(required=True, description='The order status', enum=['scheduled', 'completed', 'cancelled'], default='scheduled'),
# })

# appointment = api.model('BasicAppointment', {
#     'id': fields.Integer(readOnly=True, description='The user unique identifier'),
#     'customer_id': fields.Integer(required=True, description='The appointment unique identifier'),
#     'barber_id': fields.Integer(required=True, description='The barber unique identifier'),
#     'service_id': fields.Integer(required=True, description='The service unique identifier'),
#     'appointment_time': fields.DateTime(required=True,description='The appointment time'),
#     'created_at': fields.DateTime(readOnly=True, description='The user creation date'),
#     'updated_at': fields.DateTime(readOnly=True, description='The user last update date'),
#     'status': fields.String(required=True, description='The order status', enum=['scheduled', 'completed', 'cancelled'], default='scheduled'),
# })

# @user.route('/<int:user_id>/appointments')
# @user.param('user_id', 'The user identifier')
# class AppointmentResource(Resource):
#     @user.marshal_with(get_appointments)
#     @user.doc('Get appointments for user')
#     def get(self, user_id):
#         '''Get appointments for user'''
#         current_user = db.session.query(User).filter_by(id=user_id).first()
#         print(current_user.id)
#         if not current_user:
#             api.abort(404, "User not found")
#         appointments = db.session.query(Appointment).filter_by(customer_id=user_id).all()
#         if not appointments:
#             api.abort(404, "Appointments not found")

#         # Create a list of combined data
#         combined_data = []
#         for current_appointment in appointments:
#             barber = db.session.query(User).filter_by(id=current_appointment.barber_id).first()
#             service = db.session.query(Service).filter_by(id=current_appointment.service_id).first()
#             combined_data.append({
#                 'fullname': f"{current_user.name} {current_user.lastname}",
#                 'appointment_id': current_appointment.id,
#                 'appointment_time': current_appointment.appointment_time,
#                 'status': current_appointment.status,
#                 'barber': f"{barber.name} {barber.lastname}",
#                 'service': {
#                     'name': service.name,
#                     'duration': service.duration,
#                     'price': service.price,
#                 }
#             })
#         return combined_data
    
#     @user.doc('Create appointment for user')
#     @user.expect(create_appointment)
#     @user.marshal_with(appointment)
#     def post(self, user_id):
#         '''Create a new appointment for a user'''
#         data = request.json
#         customer_id = user_id
#         barber_id = data.get('barber_id')
#         service_id = data.get('service_id')
#         appointment_time = data.get('appointment_time')
#         status = data.get('status')

#         new_appointment = Appointment(customer_id=customer_id,
#                             barber_id=barber_id, service_id=service_id,
#                             appointment_time=appointment_time, status=status)
#         db.session.add(new_appointment)
#         db.session.commit()
#         return new_appointment, 201


# @user.route('/<int:user_id>/appointments/<int:appointment_id>')
# class SpecificAppointmentResource(Resource):
#     @user.param('user_id', 'The user identifier')
#     @user.param('appointment_id', 'The appointment identifier')
#     @user.marshal_with(get_appointments)
#     @user.doc('Get appointments for user')
#     def get(self, user_id,appointment_id):
#         '''Gets information about specific appointment for user'''
#         current_user = db.session.query(User).filter_by(id=user_id).first()
#         if not current_user:
#             api.abort(404, "User not found")

#         current_appointment = db.session.query(Appointment).filter_by(id=appointment_id).first()
#         if not appointment:
#             api.abort(404, "Appointments not found")

#         barber = db.session.query(User).filter_by(id=current_appointment.barber_id).first()
#         service = db.session.query(Service).filter_by(id=current_appointment.service_id).first()
#         appointment_data = {
#             'fullname': f"{current_user.name} {current_user.lastname}",
#             'appointment_id': current_appointment.id,
#             'appointment_time': current_appointment.appointment_time,
#             'status': current_appointment.status,
#             'barber': f"{barber.name} {barber.lastname}",
#             'service': {
#                 'name': service.name,
#                 'duration': service.duration,
#                 'price': service.price,
#             }
#         }
#         return appointment_data
      


#     @user.doc('Update appointment for user')
#     @user.expect(update_appointment)
#     @user.marshal_with(appointment)
#     def post(self, user_id,appointment_id):
#         '''Update appointment for user'''

#         current_user = db.session.get(User, user_id)
#         if not current_user:
#             api.abort(400, "Error user not found")

#         current_appointment = db.session.get(Appointment,appointment_id)
#         if not current_appointment:
#             api.abort(400, "Error appointment not found")

#         data = request.json
#         try:
#             current_appointment.barber_id = data['barber_id']
#             current_appointment.service_id = data['service_id']
#             current_appointment.appointment_time = data['appointment_time']
#             current_appointment.status = data['status']
#             db.session.commit()
#             return current_appointment, 201
#         except KeyError as e:
#             api.abort(400, "All fields are required")

### ADD NAMESPACES ###
api.add_namespace(user)
api.add_namespace(auth)

### UTILITY FUNCTIONS ###
def create_time_slots(barber_id):
    start_time = datetime.strptime("09:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    delta = timedelta(minutes=15)
    current_time = start_time

    while current_time < end_time:
        slot = Availability(barber_id=barber_id, start_time=current_time, end_time=current_time + delta)
        db.session.add(slot)
        current_time += delta

    db.session.commit()
### UTILITY FUNCTIONS ###
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", ssl_context=('nginx/ssl/hair-orama.local.crt', 'nginx/ssl/hair-orama.local.key'))

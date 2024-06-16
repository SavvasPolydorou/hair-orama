# pylint: disable= C0116,C0114,C0115,W0612
from datetime import datetime
import random
from faker import Faker


import pytz
from werkzeug.security import generate_password_hash
import pymysql

# Initialize Faker and set up timezone
fake = Faker()
GMT_PLUS_2 = pytz.FixedOffset(120)
# MySQL database configuration
MYSQL_HOST = 'localhost'  # or 'mysql-db' if connecting from another Docker container
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'rootpassword'
MYSQL_DB = 'flaskdb'

# Establish connection to MySQL database
connection = pymysql.connect(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    password=MYSQL_PASSWORD,
    db=MYSQL_DB,
    cursorclass=pymysql.cursors.DictCursor  # Return rows as dictionaries
)

# Function to get current time in GMT+2
def current_time_gmt2():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def create_fake_users(cur,conn, n=10) -> list:
    admin_counter = 0
    barber_counter = 0
    id_counter = 0
    user_type = [[], [], []] # 1st: admin, 2nd barber, 3rd customer
    for _ in range(n):
        name = fake.first_name()
        lastname = fake.last_name()
        password = generate_password_hash(fake.password())
        email = fake.email()
        role = random.choice(['customer', 'barber', 'admin'])
        id_counter +=1
        if role == 'admin':
            admin_counter +=1
        elif role == 'barber':
            barber_counter +=1

        if admin_counter > 2 and role == 'admin':
            role = 'customer'
        elif barber_counter > 5 and role == 'barber':
            role = 'customer'

        if role == 'admin':
            user_type[0].append(id_counter)
        elif role == 'barber':
            user_type[1].append(id_counter)
        elif role == 'customer':
            user_type[2].append(id_counter)

            
            
        
        created_at = current_time_gmt2()
        updated_at = current_time_gmt2()

        sql = "INSERT INTO user (name , lastname, password_hash,  email, role, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (name, lastname, password, email, role, created_at, updated_at)
        cur.execute(sql,val)

    conn.commit()
    return user_type

def create_mock_services(cur,conn, n=3):
    for _ in range(n):
        name = fake.word().capitalize() + ' Service'
        description = fake.sentence()
        price = round(fake.random_number(digits=2), 2)
        duration = random.choice([30,45,60])  # Duration in minutes
        created_at = current_time_gmt2()
        updated_at = current_time_gmt2()
        
        sql = "INSERT INTO service (name, description, price, duration, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (name, description, price, duration, created_at, updated_at)
        cur.execute(sql,val)

    conn.commit()

def create_fake_appointment(cur,conn, user_id_type):
    print(f"Barbers: {user_id_type[1]}")
    print(f"Customers: {user_id_type[2]}")
    barber_ids_opt = user_id_type[1]
    customer_id_opt = user_id_type[2]
    service_opt = [1,2,3]
    for id in customer_id_opt:
        customer_id = id
        barber_id = random.choice(barber_ids_opt)
        service_id = random.choice(service_opt)
        start_hour = random.choice([10,11,12,13,14,15,16,17])
        start_minute = random.choice([0,30])
        appointment_time = datetime.now().replace(hour=start_hour,minute=start_minute, second=0, microsecond=0)  # Start at 9 AM
        status = "scheduled"
        created_at = current_time_gmt2()
        updated_at = current_time_gmt2()
        print(f"{customer_id} {barber_id} {service_id} {appointment_time}, {status}")
        sql = "INSERT INTO appointment (customer_id , barber_id, service_id, appointment_time, created_at, updated_at, status) VALUES (%s, %s, %s, %s, %s, %s,%s)"
        val = (customer_id, barber_id, service_id, appointment_time.strftime('%Y-%m-%d %H:%M:%S'),created_at, updated_at,status)
        cur.execute(sql,val)

    conn.commit()

def test_connection():
    try:
        # Establish connection to MySQL database
        temp_connect = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            db=MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor  # Return rows as dictionaries
        )
        print("Connection to MySQL database successful!")

    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL database: {e}")

if __name__ == '__main__':

    try:
        with connection.cursor() as cursor:
            user_types = create_fake_users(cur=cursor, conn=connection, n=20)
            create_mock_services(cur=cursor, conn=connection)
            # create_fake_appointment(cur=cursor, conn=connection, user_id_type=user_types)
            # print("Mock entries have been added to the database.")
    finally:
    # Close connection
        connection.close()

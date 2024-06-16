import sqlite3
from faker import Faker
from datetime import datetime, timedelta
import random
import pytz
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize Faker and set up timezone
fake = Faker()
GMT_PLUS_2 = pytz.FixedOffset(120)

# Connect to the SQLite database
conn = sqlite3.connect('database.db')
cur = conn.cursor()


# Function to get current time in GMT+2
def current_time_gmt2():
    return datetime.now(GMT_PLUS_2).strftime('%Y-%m-%d %H:%M:%S%z')

# Generate mock data for services
def create_mock_services(n=10):
    for _ in range(n):
        name = fake.word().capitalize() + ' Service'
        description = fake.sentence()
        price = round(fake.random_number(digits=2), 2)
        duration = fake.random_int(min=15, max=120)  # Duration in minutes
        created_at = current_time_gmt2()
        updated_at = current_time_gmt2()

        cur.execute('''
            INSERT INTO service (name, description, price, duration, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, description, price, duration, created_at, updated_at))

    conn.commit()

# Generate mock data for 
def create_mock_barber_shops(n=3):
    for _ in range(n):
        name = fake.company()
        address = fake.address().replace('\n', ', ')
        phone = fake.phone_number()
        created_at = current_time_gmt2()
        updated_at = current_time_gmt2()

        cur.execute('''
            INSERT INTO barber_shop (name, address, phone, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, address, phone, created_at, updated_at))

    conn.commit()

def create_fake_availabilities():
    barber_ids = [11, 14 ,17, 2, 20, 5, 8]
    for id in barber_ids:
        barber_id = id
        start_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)  # Start at 9 AM
        end_time = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0)  # End at 6 PM

        cur.execute('''
            INSERT INTO availability (barber_id, start_time, end_time, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (barber_id, start_time.strftime('%Y-%m-%d %H:%M:%S'), end_time.strftime('%Y-%m-%d %H:%M:%S'), current_time_gmt2(), current_time_gmt2()))

    conn.commit()


def create_fake_appointment():
    barber_ids_opt = [11, 14 ,17, 2, 20, 5, 8]
    customer_id_opt = [1, 4, 7, 10, 13, 16, 19]
    barber_shop_opt = [1,2,3]
    service_opt = [1,2,3,4,5,6,7,8,9,10]
    for id in customer_id_opt:
        customer_id = id
        barber_id = random.choice(barber_ids_opt)
        barber_shop_id = random.choice(barber_shop_opt)
        service_id = random.choice(service_opt)
        start_hour = random.choice([10,11,12,13,14,15,16,17,18])
        start_minute = random.choice([0,30])
        appointment_time = datetime.now().replace(hour=start_hour,minute=start_minute, second=0, microsecond=0)  # Start at 9 AM
        status = "False"
        cur.execute('''
            INSERT INTO appointment (customer_id , barber_id, barber_shop_id, service_id, appointment_time, created_at, updated_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (customer_id, barber_id, barber_shop_id, service_id, appointment_time.strftime('%Y-%m-%d %H:%M:%S'),current_time_gmt2(), current_time_gmt2(),status))

    conn.commit()


def create_fake_users(n=10):
    for _ in range(n):
        name = fake.first_name()
        lastname = fake.last_name()
        password = generate_password_hash(fake.password())
        email = fake.email()
        role = random.choice(['customer', 'barber', 'admin'])
        cur.execute('''
            INSERT INTO user (name , lastname, password_hash,  email, role, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, lastname, password, email, role, current_time_gmt2(), current_time_gmt2()))

    conn.commit()


if __name__ == '__main__':
    with conn:
        create_fake_users(20)
        # create_mock_services()
        # create_mock_barber_shops()
        # create_fake_availabilities()
        # create_fake_appointment()
        print("Mock entries have been added to the database.")

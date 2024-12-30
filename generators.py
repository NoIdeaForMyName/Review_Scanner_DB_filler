from db_data import *
from sqlalchemy import select, insert, Table
from faker import Faker
import random
from datetime import timedelta, datetime
from generators_settings import *
import os
import json
import hashlib


Faker.seed(SEED)
fake = Faker()


def insert_rows(table: Table, rows: list[dict]):
    with engine.connect() as conn:
        conn.execute(insert(table), rows)
        conn.commit()

def get_all_ids(table: Table) -> list[int]:
    stmt = table.select()
    exe = conn.execute(stmt)
    return list(map(lambda row: row[0], exe.fetchall()))

def hash_password(password: str, salt: str) -> str:
    """
    Hash a password using a salt.
    """
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()


def users(n):
    rows = []
    credentials = []

    used_emails = set()
    used_nicknames = set()

    for i in range(n):
        email = fake.email()
        while email in used_emails:
            email = fake.email()
        used_emails.add(email)
        nickname = fake.name().replace(' ', '_')
        while nickname in used_nicknames:
            nickname = fake.name().replace(' ', '_')
        used_nicknames.add(nickname)
        password_raw = fake.password()
        salt = os.urandom(32).hex()
        password = hash_password(password_raw, salt)
        rows.append(
            {
                'email': email,
                'nickname': nickname,
                'password': password,
                'salt': salt
            }
        )
        credentials.append(
            {
                'email': email,
                'password': password_raw
            }
        )
    insert_rows(User, rows)
    with open("users_credentials.json", "w") as file:
        json.dump(credentials, file)


def shops(n):
    rows = []

    used_names = set()

    for i in range(n):
        name = fake.word()
        while name in used_names:
            name = fake.word()
        used_names.add(name)
        rows.append(
            {
                'shop_name': name
            }
        )
    insert_rows(Shop, rows)


def products(n):
    rows = []

    used_barcodes = set()
    used_names = set()

    for i in range(n):
        barcode = ''.join([str(random.randint(0, 9)) for _ in range(BARCODE_LENGTH)])
        while barcode in used_barcodes:
            barcode = ''.join([str(random.randint(0, 9)) for _ in range(BARCODE_LENGTH)])
        used_barcodes.add(barcode)
        name = fake.word()
        while name in used_names:
            name = fake.word()
        used_names.add(name)
        description = fake.text(max_nb_chars=MAX_TEXT_CHARACTER_NUMBER)
        image = f'{IMG_NAME_FORMAT}{random.randint(1, IMAGES_NB)}.{IMG_EXTENSION}'
        rows.append(
            {
                'product_barcode': barcode,
                'product_name': name,
                'product_description': description,
                'product_image': image
            }
        )
    insert_rows(Product, rows)
    with open('barcodes.txt', 'w') as file:
        for barcode in used_barcodes:
            file.write(f'{barcode}\n')


# we are storing only the last scan of a specific product in DB (if such product was already scanned - its timestamp is updated)
def scan_histories(n):
    rows = []

    user_prod_PKs_used = set()

    user_ids = get_all_ids(User)
    prod_ids = get_all_ids(Product)
    for i in range(n):
        user_fk = random.choice(user_ids)
        product_fk = random.choice(prod_ids)
        while (user_fk, product_fk) in user_prod_PKs_used:
            user_fk = random.choice(user_ids)
            product_fk = random.choice(prod_ids)
        user_prod_PKs_used.add((user_fk, product_fk))
        timestamp = MIN_DATETIME + timedelta(seconds=random.randint(0, int((datetime.now() - MIN_DATETIME).total_seconds())))
        rows.append(
            {
                'scan_history_user_fk': user_fk,
                'scan_history_product_fk': product_fk,
                'scan_timestamp': timestamp
            }
        )
    insert_rows(Scan_history, rows)
    

def reviews(n):
    rows = []

    prev_reviews = set()

    user_ids = get_all_ids(User)
    prod_ids = get_all_ids(Product)
    shop_ids = get_all_ids(Shop)
    for i in range(n):
        user_fk = random.choice(user_ids)
        prod_fk = random.choice(prod_ids)
        while(user_fk, prod_fk) in prev_reviews:
            user_fk = random.choice(user_ids)
            prod_fk = random.choice(prod_ids)
        prev_reviews.add((user_fk, prod_fk))
        grade = random.choice(GRADES)
        title = fake.word()
        description = fake.text(max_nb_chars=MAX_TEXT_CHARACTER_NUMBER)
        price = round(random.random() * MAX_PRICE, 2)
        shop_fk = random.choice(shop_ids)
        timestamp = MIN_DATETIME + timedelta(seconds=random.randint(0, int((datetime.now() - MIN_DATETIME).total_seconds())))
        rows.append(
            {
                'reviews_user_fk': user_fk,
                'review_product_fk': prod_fk,
                'review_grade': grade,
                'review_title': title,
                'review_description': description,
                'review_price': price,
                'review_shop_fk': shop_fk,
                'review_timestamp': timestamp
            }
        )
    insert_rows(Review, rows)


def reviews_media(n):
    rows = []

    rev_ids = get_all_ids(Review)
    for i in range(n):
        review_fk = random.choice(rev_ids)
        path = f'image{random.randint(0, IMAGES_NB-1)}.png'
        rows.append(
            {
                'media_review_fk': review_fk,
                'media_path': path
            }
        )
    insert_rows(Review_media, rows)

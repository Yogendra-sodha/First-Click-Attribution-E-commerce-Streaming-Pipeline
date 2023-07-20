import argparse
import json
import random
from datetime import datetime
from uuid import uuid4

import psycopg2
from confluent_kafka import Producer
from faker import Faker

fake = Faker()

# Creating connection


def gen_user_data(num_users: int) -> None:
    """
    This function generates fake user profile by adding num_users specified
    in num_user param
    """
    for id in range(num_users):
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            host='postgres',
            password='postgres',
        )

        curr = conn.cursor()
        curr.execute(
            """
            INSERT INTO commerce.users
            (id,username,password) VALUES(%s,%s,%s)
            """,
            (id, fake.user_name(), fake.password()),
        )
        curr.execute(
            """
            INSERT INTO commerce.products
            (id,name,description,price) VALUES(%s,%s,%s,%s)
            """,
            (id, fake.name(), fake.text(), fake.random_int(min=1, max=100)),
        )

        conn.commit()
        curr.close()
    return


def random_user_agent():
    return fake.user_agent()


def random_ipv4():
    return fake.ipv4()


def gen_click_event(user_id, product_id=None):
    '''
    This functions takes user_id and creates fake click event
    for that uid
    '''
    click_id = str(uuid4())
    user_id = user_id
    product_id = product_id or str(uuid4())
    product = fake.word()
    price = fake.pyfloat(left_digits=2, right_digits=2, positive=True)
    url = fake.uri()
    user_agent = random_user_agent()
    ip_address = random_ipv4()
    datetime_occured = datetime.now()

    click_event = {
        "click_id": click_id,
        "product_id": product_id,
        "product": product,
        "price": price,
        "url": url,
        "user_agent": user_agent,
        "ip_address": ip_address,
        "datetime_occured": datetime_occured.strftime("%Y-%m-%d %H:%M:%S.%f")[
            :-3
        ],
    }

    return click_event


def gen_checkout_event(user_id, product_id):
    payment_method = fake.credit_card_provider()
    total_amount = fake.pyfloat(left_digits=3, right_digits=2, positive=True)
    shipping_address = fake.address()
    billing_adddress = fake.address()
    user_agent = random_user_agent()
    ip_address = random_ipv4()
    datetime_occured = datetime.now()

    checkout_event = {
        "payment_method": payment_method,
        "total_amount": total_amount,
        "shipping_address": shipping_address,
        "billing_adddress": billing_adddress,
        "user_agent": user_agent,
        "ip_address": ip_address,
        "datetime_occured": datetime_occured.strftime("%Y-%m-%d %H:%M:%S.%f")[
            :-3
        ],
    }
    return checkout_event


def push_to_kafka(event, topic):
    producer = Producer({'bootstrap.servers': 'kafka:9092'})
    producer.produce(topic, json.dumps(event).encode('utf-8'))
    producer.flush()


def push_clickstream_data(num_clicks: int) -> None:
    for i in range(num_clicks):
        user_id = random.randint(1, 200)
        click_event = gen_click_event(user_id)
        push_to_kafka(click_event, 'clicks')

        if random.randint(1, 200) <= 160:
            click_event = gen_click_event(user_id, click_event['product_id'])
            push_to_kafka(click_event, 'clicks')

            push_to_kafka(
                gen_checkout_event(
                    click_event['user_id'], click_event['product_id']
                ),
                'checkouts',
            )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-nu",
        "--num_users",
        type=int,
        help="Number of users to generate",
        default=200,
    )
    parser.add_argument(
        "-nc",
        "--num_clicks",
        type=int,
        help="Numbers of clicks to generate",
        default=150000000,
    )
    args = parser.parse_args()
    gen_user_data(args.num_users)
    push_clickstream_data(args.num_clicks)

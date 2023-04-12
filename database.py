from sqlalchemy import create_engine, text
import base64
import os
import random

try:
    with open('local.txt') as f:
        lines = [line for line in f]
        db_connection = lines[0]
except:
    db_connection = os.environ["DATABASE_CREDENTIALS"]


engine = create_engine(db_connection, connect_args= 
    {
    "ssl": {
        "sll_ca": "/etc/ssl/cert.pem"
            }
    })

def encode_binary_response(response):
        """ encode the icon response from the database. remember that Json type do not natively support binary data"""
        cities_dict = []
        for row in response:
            row_dict = dict(row)
            if row_dict["city_icon"] == None:
                cities_dict.append(row_dict)
            else:
                base64_encoded_image = base64.b64encode(row_dict["city_icon"]).decode("utf-8")
                row_dict.update({"city_icon": base64_encoded_image})
                cities_dict.append(row_dict)
        return cities_dict

def load_cities_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from cities"))
        cities = result.mappings().all()
    cities_list = encode_binary_response(cities)
    return cities_list

def load_city_from_db():
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM cities ORDER BY RAND() LIMIT 1"))
        city = result.mappings().all()
    city_dict = encode_binary_response(city)
    return city_dict[0]


def update_like_dislike(id, ld):
    with engine.connect() as conn:
        query = text(f'UPDATE cities.cities SET city_like = "{ld}" WHERE id = {id}')
        conn.execute(query)

from sqlalchemy import create_engine, text
import base64
import os

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
            if row_dict["im"] == None:
                cities_dict.append(row_dict)
            else:
                base64_encoded_image = base64.b64encode(row_dict["im"]).decode("utf-8")
                row_dict.update({"im": base64_encoded_image})
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
    
    return city[0]

def load_city_image_from_db(id_city):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT im FROM images WHERE id_city = {id_city}"))
    encoded_image = encode_binary_response(result)
    return [d['im'] for d in encoded_image]

def update_like_dislike(id, like, user):
    with engine.connect() as conn:
        query = text(f'UPDATE `cities`.`user{user}` SET `like` = "{like}" WHERE city_id = {id}')

        print(query)
        conn.execute(query)

def load_lat_long_from_db(id):
    with engine.connect() as conn:
        query = text(f'SELECT city_name, city_lat, city_long FROM cities.cities where id = {id};')
        result = conn.execute(query).mappings().all()[0]
        markers=[
            {
            'lat':result["city_lat"],
            'lon':result["city_long"],
            'popup':result["city_name"]
                }
            ]
        return markers
    
def try_login(username):
     with engine.connect() as conn:
        query = text(f'SELECT * FROM cities.users WHERE user_id = "{username}";')
        result = conn.execute(query).mappings().all()
        if len(result) == 0:
            return False
        else:
            return result[0]

def create_account(username, pswrd):
    with engine.connect() as conn:
        create_user = text(f'CREATE TABLE `cities`.`user{username}` (`id` INT NOT NULL AUTO_INCREMENT,`city_id` INT NULL,`like` VARCHAR(45) NULL,PRIMARY KEY (`id`));')
        conn.execute(create_user)
    with engine.connect() as conn2:
        create_user_pswrd = text(f"INSERT INTO `cities`.`users` (`user_id`, `user_psw`) VALUES ('{username}', '{pswrd}');")
        conn2.execute(create_user_pswrd)

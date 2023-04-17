from flask import Flask, render_template, jsonify, request, session, redirect
from database import load_cities_from_db, update_like_dislike, load_city_from_db, load_city_image_from_db,load_lat_long_from_db

app = Flask(__name__)

@app.route("/")
def home():
    city = load_city_from_db()
    images = load_city_image_from_db(city['id'])
    return render_template('home.html', city=city, images = images, enumerate = enumerate)


@app.route("/api/cities")
def get_list_of_cities():
    cities_list = load_cities_from_db()
    return cities_list


@app.route("/update/<int:id>", methods=['POST'])
def update_like(id):
    action = request.form['action']
    if action == "like":
        update_like_dislike(id, "like")
    elif action == "dislike":
        update_like_dislike(id, "dislike")
    return redirect("/")


@app.route("/map/<int:id>")
def root(id):
   lat_long = load_lat_long_from_db(id)
   markers=[
   {
   'lat':lat_long["city_lat"],
   'lon':lat_long["city_long"],
   'popup':lat_long["city_name"]
    }
   ]
   return render_template('map.html', markers=markers)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

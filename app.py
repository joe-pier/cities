from flask import Flask, render_template, jsonify, request, session, redirect
from database import load_cities_from_db, update_like_dislike, load_city_from_db

app = Flask(__name__)

@app.route("/")
def home():
    city = load_city_from_db()
    return render_template('home.html', city=city)


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

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

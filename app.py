from flask import Flask, render_template, jsonify, request, session, redirect
from database import try_login,load_cities_from_db, update_like_dislike, load_city_from_db, load_city_image_from_db,load_lat_long_from_db

app = Flask(__name__)
app.secret_key = "oifnwefnoienbgpwemfpw124nn2135kn4og3n43i"
@app.route("/")
def home():
    city = load_city_from_db()
    images = load_city_image_from_db(city['id'])
    return render_template('home.html', city=city, images = images, enumerate = enumerate, session= session)

@app.route("/api/cities")
def get_list_of_cities():
    cities_list = load_cities_from_db()
    return cities_list

@app.route("/update/<int:id>", methods=['POST'])
def update_like(id):
    if len(session) != 0:
        print(session["username"])
        action = request.form['action']
        if action == "like":
            update_like_dislike(id, "like", session["username"])
        elif action == "dislike":
            update_like_dislike(id, "dislike", session["username"])
        return redirect("/")
    else:
        return "please login"

@app.route("/map/<int:id>")
def root(id):
   markers = load_lat_long_from_db(id)
   return render_template('map.html', markers=markers)

@app.route("/login", methods = ["POST"])
def login():
    user_pswrd = request.form["user_pswrd"]
    user_name = request.form["user_name"]
    try_login_bool = try_login(user_name)
    if try_login_bool:
        user_db_pswrd = try_login_bool["user_psw"]
        user_db_name = try_login_bool["user_id"]
        if (user_name == user_db_name) & (user_pswrd == user_db_pswrd):
            session["username"] = user_name
            session["password"] = user_pswrd
            print("correct login")
            return redirect("/")
        else:
            print("wrong password")
            return redirect("/")
    else:
        print("wrong username")
        return redirect("/")

@app.route("/logout")
def logout():
    if len(list(session.keys())) == 0:
        return redirect("/")
    else:
        try:
            session.pop("username")
        except:
            pass
        try:
            session.pop("password")
        except:
            pass
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

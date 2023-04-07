from flask import Flask, render_template, jsonify, request, session
from database import load_cities_from_db

app = Flask(__name__)  

@app.route("/")
def home():
    cities = load_cities_from_db()
    return render_template('home.html', cities = cities)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

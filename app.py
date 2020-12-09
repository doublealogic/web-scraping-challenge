from flask import Flask, render_template, jsonify, redirect
import flask_pymongo
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mission_to_mars_app")

@app.route("/")
def index():
    mars_data = mongo.db.Mission_to_Mars.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    # Activates Scrape function which scrapes websites for facts and news about Mars
    mtm_scrape = scrape_mars.scrape()

    # Updates Mission to Mars database
    mongo.db.Mission_to_Mars.update({}, mtm_scrape, upsert = True)

    # Takes you back to the home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
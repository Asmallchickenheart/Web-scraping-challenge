# use the framework from the flask library
from flask import Flask, app, render_template
from scrape_mars import scrape
from pymongo import MongoClient

app = Flask(__name__)

# create a connection to the mongo database
client = MongoClient('localhost', 27017)
db = client.mars_app
collection = db.mars_data


# create a route to the index page
@app.route('/')
def render_data():
    # find the data in the mongo database
    mars_data = collection.find_one({'data_id': 1})
    # render the index page
    return render_template('index.html', mars_data=mars_data)


# create a route to the index page
@app.route('/scrape')
def scrape_mars():
    # store the result in a Mongo database as a python dictionary
    mars_data = scrape()
    # update the mongo database
    collection.update_one({"data_id": 1}, {'$set': mars_data}, upsert=True)
    # redirect to the index page
    print(type(mars_data))
    return render_template('index.html', mars_data=mars_data)


if __name__ == '__main__':
    app.run(debug=True)

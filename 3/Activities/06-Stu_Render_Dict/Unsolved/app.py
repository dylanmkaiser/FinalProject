# import necessary libraries
from flask import Flask, render_template

# @TODO: Initialize your Flask app here
app = Flask(__name__)

# @TODO: Create a list of dictionaries
profile=[
    {"name":"fluff","type":"cat"},
    {"name":"aluff","type":"bat"},
]

# @TODO:  Create a route and view function that takes in a dictionary and renders index.html template
@app.route("/")
def home():
    return render_template("index.html",dict=profile)

if __name__ == "__main__":
    app.run(debug=True)

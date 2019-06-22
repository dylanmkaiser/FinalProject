# import necessary libraries
from flask import Flask, render_template

# @TODO: Initialize your Flask app here
app = Flask(__name__)

# @TODO:  Create a route and view function that takes in a string and renders index.html template
@app.route("/")
def echo():
    return render_template("index.html", hobby = "golf",name = "bob")

if __name__ == "__main__":
    app.run(debug=True)

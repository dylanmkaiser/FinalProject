# import necessary libraries
from flask import Flask, render_template

# @TODO: Initialize your Flask app here
app = Flask(__name__)

# @TODO:  Create a route and view function that takes in a list of strings and renders index.html template
# CODE GOES HERE


@app.route("/")
def index():
    movie_list = ["Dumbo", "Dumbo 2: Return", "Dribblers", "Passers"]
    return render_template("index.html", list=movie_list)

if __name__ == "__main__":
    app.run(debug=True)

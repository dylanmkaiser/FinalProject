from flask import Flask, render_template
import pymongo

app = Flask(__name__)

@app.route('/')
def index():
    # @TODO: write a statement that finds all the items in the db and sets it to a variable
    produce_list = list(db.produce.find())

    # @TODO: render an index.html template and pass it the data you retrieved from the database
    return render_template(index.html,list=produce_list)


if __name__ == "__main__":
    app.run(debug=True)

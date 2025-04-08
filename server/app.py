#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os
from sqlalchemy.orm import joinedload
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''


@app.route('/campers', methods=['GET'])
def campers():
    campers = []
    
    # Loop through all campers and collect the necessary data
    for camper in Camper.query.all():
        camper_dict = {
            "id": camper.id,
            "name": camper.name,
            "age": camper.age
        }
        campers.append(camper_dict)

    # Return the JSON response with all campers
    response = make_response(
        jsonify(campers),
        200
    )
    return response


    
@app.route('/campers/<int:id>', methods=['GET'])
def camper_by_id(id):
    # Retrieve the camper by ID and eagerly load signups and related activities
    camper = Camper.query.filter(Camper.id == id).options(
        joinedload(Camper.signups).joinedload(Signup.activity)  # Eagerly load signups and activities
    ).first()


    # Check if the camper was found
    if camper is None:
        return jsonify({"error": "Camper not found"}), 404

    # Prepare the camper data
    camper_dict = {
        "age": camper.age,
        "id": camper.id,
        "name": camper.name,
        "signups": [
            {
                "id": signup.id,
                "time": signup.time,
                "camper_id": signup.camper_id,
                "activity_id": signup.activity_id,
                "activity": {
                    "id": signup.activity.id,
                    "name": signup.activity.name,
                    "difficulty": signup.activity.difficulty
                }
            }
            for signup in camper.signups
        ]
    }

    response = make_response(
        camper_dict,
        200
    )

    return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)

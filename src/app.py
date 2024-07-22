"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }

    return jsonify(response_body), 200

@app.route('/add_member', methods=['POST'])
def handel_add_member():
    request_body = request.json.get
    member = {
        "id": FamilyStructure._generateId(FamilyStructure) ,
        "first_name": request_body("first_name"), 
        "last_name": jackson_family.last_name,  
        "age": request_body('age'),
        "lucky_numbers": request_body("lucky_numbers")
        
        }
    new_member = jackson_family.add_member(member)
    return jsonify(new_member)



@app.route('/member/<int:id>', methods=['GET'])
def handel_single_member(id):
    member = jackson_family.get_member(id)
    if member == None:
        return "Memmber not found", 400
    else: 
        return jsonify(member), 200



@app.route('/delete_member/<int:id>', methods=['DELETE'])
def handel_delete_member(id):
    result = jackson_family.delete_member(id)
    if result == False: 
        return "Error: member not deleted", 400
    return "member has been deleted", 204



    


    

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

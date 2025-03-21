import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from random import randint

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name
     
        self._members = [
            {"id": 3443, "first_name": "Tommy", "age": 22, "lucky_numbers": [7, 13, 22]},
            {"id": 4446, "first_name": "Jane", "age": 35, "lucky_numbers": [10, 14, 3]},
            {"id": 125,  "first_name": "Jimmy", "age": 5, "lucky_numbers": [1]}
        ]

    def _generateId(self):
        return randint(0, 99999999)

    def add_member(self, member):
        
        if "id" not in member or member["id"] is None:
            member["id"] = self._generateId()
       
        self._members.append(member)
        return member

    def delete_member(self, id):
        for index, member in enumerate(self._members):
            if member["id"] == id:
                del self._members[index]
                return True
        return False

    def update_member(self, member):
        for index, current_member in enumerate(self._members):
            if current_member["id"] == member.get("id"):
                self._members[index].update(member)
                return self._members[index]
        return None

    def get_member(self, id):
        for member in self._members:
            if member["id"] == id:
                return member
        return None

    def get_all_members(self):
        return self._members

class APIException(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

def generate_sitemap(app):
    links = []
    for rule in app.url_map.iter_rules():
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append(url)
    links_html = "".join(["<li><a href='" + y + "'>" + y + "</a></li>" for y in links])
    return (
        "<div style='text-align: center;'>"
        "<img src='https://github.com/breatheco-de/exercise-family-static-api/blob/master/rigo-baby.jpeg?raw=true' />"
        "<h1>Hello Rigo!!</h1>"
        "This is your API home, remember to specify a real endpoint path like: "
        "<ul style='text-align: left;'>" + links_html + "</ul></div>"
    )


jackson_family = FamilyStructure("Jackson")

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def get_all_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200

@app.route('/member', methods=['POST'])
def add_member():
    new_member = request.get_json()
    if not new_member:
        return jsonify({"error": "Invalid JSON data"}), 400

    required_fields = ["first_name", "age", "lucky_numbers"]
    for field in required_fields:
        if field not in new_member:
            return jsonify({"error": f"Missing required member field: {field}"}), 400

    member = jackson_family.add_member(new_member)
    return jsonify(member), 200

@app.route('/member/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    updated_data = request.get_json()
    if not updated_data:
        return jsonify({"error": "Invalid JSON data"}), 400
    updated_data["id"] = member_id
    member = jackson_family.update_member(updated_data)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    result = jackson_family.delete_member(member_id)
    if result:
        return jsonify({"done": True}), 200
    else:
        return jsonify({"error": "Member not found"}), 404


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)

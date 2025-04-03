from app import app, auth
from flask import jsonify, abort, make_response, request
from structures.models import *
from structures.serializers import buildings_schema, building_schema

@app.route('/structures/api/v1/buildings', methods=['GET'])
@auth.login_required
def get_buildings():
    buildings = get_all_buildings()

    return jsonify({"buildings": buildings_schema.dump(buildings)})


@app.route('/structures/api/v1/buildings/<int:id>', methods=['GET'])
@auth.login_required
def get_one_building(id):
    building = get_building(id)
    if building is None:
        abort(404)
    return jsonify({"building": building_schema.dump(building)})


@app.route('/structures/api/v1/buildings', methods=['POST'])
@auth.login_required
def create_building():
    if (not request.json
            or 'title' not in request.json
            or 'type_building_id' not in request.json
            or 'city_id' not in request.json):
        abort(400)

    new_building = request.get_json()

    if 'height' not in request.json:
        new_building['height'] = 0
    if 'year' not in request.json:
        new_building['year'] = 2000

    try:
        building_new = insert_building(new_building)
    except Exception as e:
        abort(400, e.args)

    return jsonify({'building': building_schema.dump(building_new)}), 201


@app.route('/structures/api/v1/buildings/<int:id>', methods=['PUT'])
@auth.login_required
def update_one_building(id):
    # получить информацию о здании с указанным id
    building = get_building(id)
    if building is None or not request.json:
        abort(404)
    if 'title' in request.json and type(request.json['title']) is not str:
        abort(400)
    if ('type_building_id' in request.json and
            type(request.json['type_building_id']) is not int):
        abort(400)
    if 'city_id' in request.json and type(request.json['city_id']) is not int:
        abort(400)
    if 'year' in request.json and type(request.json['year']) is not int:
        abort(400)
    if 'height' in request.json and type(request.json['height']) is not int:
        abort(400)

    building_update = update_building(id, request.get_json())

    return jsonify({'building': building_schema.dump(building_update)})


@app.route('/structures/api/v1/buildings/<int:id>', methods=['DELETE'])
@auth.login_required
def delete_one_building(id):
    try:
        delete_building(id)
    except Exception as e:
        abort(400, e.args)
    return make_response(jsonify({'message': 'No content'}), 204)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

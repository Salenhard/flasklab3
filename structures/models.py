from flask import session

from config import db
from models import Country, City, Building, TypeBuilding
from sqlalchemy import func
from structures.serializers import building_schema, buildings_schema


def get_all_buildings():

    query = Building.query.all()

    return query


def get_building(building_id):
    query = Building.query.filter(Building.id == building_id).one_or_none()
    return query

def insert_building(building):
    item = building_schema.load(building, session=db.session)
    db.session.add(item)
    db.session.commit()
    # возвращаем вставленную запись, то есть запись с максимальным id
    return ((Building.query
            .filter(Building.id == db.session.query(func.max(Building.id))))
            .one_or_none())

def update_building(id, data):
    building = Building.query.get(id)
    if not building:
        raise ValueError("Building not found")

    if 'title' in data and not isinstance(data['title'], str):
        raise ValueError("Title must be a string")
    if 'type_building_id' in data:
        if not isinstance(data['type_building_id'], int):
            raise ValueError("type_building_id must be an integer")
        if not TypeBuilding.query.get(data['type_building_id']):
            raise ValueError("Invalid type_building_id")
    if 'city_id' in data:
        if not isinstance(data['city_id'], int):
            raise ValueError("city_id must be an integer")
        if not City.query.get(data['city_id']):
            raise ValueError("Invalid city_id")
    if 'year' in data and not isinstance(data['year'], int):
        raise ValueError("year must be an integer")
    if 'height' in data and not isinstance(data['height'], int):
        raise ValueError("height must be an integer")

    for key, value in data.items():
        if hasattr(building, key):
            setattr(building, key, value)

    try:
        db.session.commit()
        return building
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error updating building: {str(e)}")

def delete_building(id):
    building = Building.query.get(id)
    if not building:
        raise ValueError("Building not found")

    try:
        db.session.delete(building)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Error deleting building: {str(e)}")
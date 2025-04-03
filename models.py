from config import db, app


class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Страна', db.String(100), nullable=False)
    cities = db.relationship("City", back_populates="country", cascade="all, delete")

    def __init__(self, name):
        self.name = name


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Город', db.String(100), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
    country = db.relationship("Country", back_populates="cities")
    buildings = db.relationship("Building", back_populates="city")

    def __init__(self, name, country_id):
        self.name = name
        self.country_id = country_id


class Building(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column('Название', db.String(200))
    type_building_id = db.Column(db.Integer, db.ForeignKey('type_building.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
    year = db.Column(db.Integer)
    height = db.Column(db.Integer)
    type_building = db.relationship("TypeBuilding", back_populates="buildings")
    city = db.relationship("City", back_populates="buildings")

    def __init__(self, title, type_building_id, city_id, year, height):
        self.title = title
        self.type_building_id = type_building_id
        self.city_id = city_id
        self.year = year
        self.height = height

    def __str__(self):
        return f"Building(id={self.id}, title={self.title}, type_building_id={self.type_building_id}, city_id={self.city_id}, year={self.year}, height={self.height})"

    def __repr__(self):
        return str(self)

class TypeBuilding(db.Model):
    __tablename__ = "type_building"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column('Тип', db.String(50), nullable=False)
    buildings = db.relationship("Building", back_populates="type_building")

    def __init__(self, name):
        self.name = name


app.app_context().push()

with app.app_context():
    db.create_all()

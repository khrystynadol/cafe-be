from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.sql import func
import enum

app = Flask(__name__)
app.secret_key = 'just secret key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12345@localhost:5432/al-trecolore-menu"
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:databasesql2022@localhost:5432/al-trecolore-menu"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqldb://root:databasesql2022@localhost:3306/al-trecolore-menu"

db = SQLAlchemy(app)


class PersonStatus(enum.Enum):
    client = "client"
    manager = "manager"


class CustomStatus(enum.Enum):
    registered = "registered"
    processed = "processed"
    accepted = "accepted"
    prepared = "prepared"
    delivered = "delivered"
    done = "done"
    cancelled = "cancelled"


class Person(db.Model):
    __tablename__ = 'person'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    surname = db.Column(db.String(45), nullable=False)
    phone = db.Column(db.String(13), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    role = db.Column(db.Enum(PersonStatus), nullable=False, default="client")

    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}

    # def is_authenticated(self) -> bool:
    #     return True
    #
    # def is_active(self) -> bool:
    #     return True
    #
    # def is_anonymous(self) -> bool:
    #     return False
    #
    # def get_id(self):
    #     return self.id


class Address(db.Model):
    __tablename__ = 'address'

    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(45), nullable=False)
    house = db.Column(db.String(45), nullable=False)
    flat = db.Column(db.Integer, nullable=True)


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    price = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}


class Menu(db.Model):
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, nullable=False, default=False)
    demand = db.Column(db.Boolean, nullable=False, default=False)

    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}


class Custom(db.Model):
    __tablename__ = 'custom'

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(CustomStatus), nullable=False, default="registered")
    address_id = db.Column(db.Integer, db.ForeignKey('address.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('person.id'))

    def as_dict(self):
        return {p.name: getattr(self, p.name) for p in self.__table__.columns}


class Details(db.Model):
    __tablename__ = 'details'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    custom_id = db.Column(db.Integer, db.ForeignKey('custom.id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))


class Ingredient(db.Model):
    __tablename__ = 'ingredient'

    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    percent = db.Column(db.Integer, nullable=False, default=20)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    def get_menu_id(self):
        return self.menu_id

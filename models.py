from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import enum

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://user:databasesql2022@localhost:3306/al-trecolore-menu"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+mysqldb://root:databasesql2022@localhost:3306/al-trecolore-menu"

db = SQLAlchemy(app)


class UserStatus(enum.Enum):
    CLIENT='client'
    MANAGER='manager'


class User(db.Model):
    __tablename__ = 'user'

    idUser = db.Column(db.Integer, primary_key=True)
    u_name = db.Column(db.String(45), nullable=False)
    u_surname = db.Column(db.String(45), nullable=False)
    u_phone = db.Column(db.Integer, nullable=False)
    u_email = db.Column(db.String(45),unique=True, nullable=True)
    u_password = db.Column(db.String(45), nullable=False)
    u_role = db.Column(db.Enum(UserStatus), nullable=True,default=UserStatus.CLIENT.value)

"""     def __repr__(self):
        return "<User: '{}' '{}', email: '{}'>" \
            .format(self.first_name, self.last_name, self.email) """

class Address(db.Model):
    __tablename__ = 'address'

    idAddress = db.Column(db.Integer, primary_key=True)
    a_street = db.Column(db.String(45), nullable=False)
    a_house = db.Column(db.String(45), nullable=False)
    a_flat = db.Column(db.Integer, nullable=True, default='0')

"""     def __repr__(self):
        return "<Additional passenger : '{}' '{}', email: '{}'>" \
            .format(self.first_name, self.last_name, self.email) """


class Product(db.Model):
    __tablename__ = 'product'

    idProduct= db.Column(db.Integer, primary_key=True)
    p_name = db.Column(db.String(45), nullable=True)
    p_price = db.Column(db.Integer, nullable=True)
    p_weight = db.Column(db.Integer, nullable=True)

"""     def __repr__(self):
        return "<Booking by user id: '{}', price: '{} >" \
            .format( self.userid, self.total_price) """


class Custom(db.Model):
    __tablename__ = 'custom'

    idCustom = db.Column(db.Integer, primary_key=True)
    c_price = db.Column(db.Integer, nullable=True, default='0')
    Address_id = db.Column(db.Integer, db.ForeignKey('address.idAddress'))
    User_id = db.Column(db.Integer, db.ForeignKey('user.idUser'))

"""     def __repr__(self):
        return "<Booking by user id: '{}', price: '{} >" \
            .format( self.userid, self.total_price) """


class Details(db.Model):
    __tablename__ = 'details'

    idDetails = db.Column(db.Integer, primary_key=True)
    d_quantity = db.Column(db.Integer, nullable=True, default='1')
    Custom_id = db.Column(db.Integer, db.ForeignKey('custom.idCustom'))
    Menu_id = db.Column(db.Integer, db.ForeignKey('menu.idMenu'))

"""
    def __repr__(self):
        return "<Flight  '{}' - '{}' on '{}'>" \
            .format(self.flight_from, self.flight_to, self.flight_date) """


class Menu(db.Model):
    __tablename__ = 'menu'

    idMenu = db.Column(db.Integer, primary_key=True)
    m_name = db.Column(db.String(45), nullable=True)
    m_price = db.Column(db.Integer, nullable=True, default='0' )
    m_availability = db.Column(db.Boolean, nullable=True, default='0' )
    m_demand = db.Column(db.Boolean, nullable=True, default='0')

"""     def __repr__(self):
        return "<Sit number : '{}', availability : '{}', price: '{}'>" \
            .format(self.sitnumber, self.available, self.price) """


class Ingredient(db.Model):
    __tablename__ = 'ingredient'

    idIngredient = db.Column(db.Integer, primary_key=True)
    i_weight = db.Column(db.Integer, nullable=False)
    i_percent = db.Column(db.Integer, nullable=False, default='20')
    Menu_id = db.Column(db.Integer, db.ForeignKey('menu.idMenu'))
    Product_id = db.Column(db.Integer, db.ForeignKey('product.idProduct'))

"""     def __repr__(self):
        return "<Flight  '{}' - '{}' on '{}'>" \
            .format(self.flight_from, self.flight_to, self.flight_date) """


@app.route("/")
def home():
    return 'Home'


@app.route("/api/v1/hello-world-<value>")
def hello_world(value):
    return "Hello world " + value, 200


if __name__ == "__main__":
    app.run()
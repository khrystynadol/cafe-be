from database.models import db
import datetime
from marshmallow import Schema, fields, validate, validates, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash


class PersonSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=0))
    name = fields.Str(validate=[validate.Regexp("[a-zA-z]*$"),
                                validate.Length(min=3, max=45)],
                      required=True)
    surname = fields.Str(validate=[validate.Regexp("[a-zA-z]*$"),
                                   validate.Length(min=5, max=45)],
                         required=True)
    phone = fields.Str(required=True,
                       validate=[validate.Length(equal=10)])
    email = fields.Email(required=True)
    password = fields.Function(  # validate=validate.Length(min=5, max=15),
                               deserialize=lambda password: generate_password_hash(password),
                               load_only=True, required=True
                               )
    role = fields.Str(dump_default='client',
                      validate=validate.OneOf('client', 'manager'),
                      required=False)

    @validates('phone')
    def validate_phone(self, phone):
        try:
            res = int(phone)
        except ValueError:
            res = 0
        if (not phone.isdigit()) or res == 0:
            raise ValidationError(f'Incorrect phone number.')


class PersonToUpdateSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=0))
    name = fields.Str(validate=[validate.Regexp("[a-zA-z]*$"),
                                validate.Length(min=3, max=45)])
    surname = fields.Str(validate=[validate.Regexp("[a-zA-z]*$"),
                                   validate.Length(min=5, max=45)])
    phone = fields.Str(validate=[validate.Length(equal=10)])
    email = fields.Email()
    password = fields.Function(deserialize=lambda password: generate_password_hash(password),
                               load_only=True)
    role = fields.Str()

    @validates('phone')
    def validate_phone(self, phone):
        try:
            res = int(phone)
        except ValueError:
            res = 0
        if (not phone.isdigit()) or res == 0:
            raise ValidationError(f'Incorrect phone number.')


class CustomSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=0))
    price = fields.Float(validate=validate.Range(min=0), required=True)
    time = fields.DateTime(format='%Y-%m-%dT%H:%M:%S',
                           default=datetime.datetime.now(),
                           validate=lambda x: x <= datetime.datetime.now())
    status = fields.Str(dump_default='registered',
                        validate=validate.OneOf(['registered', 'processed', 'accepted',
                                                'prepared', 'delivered', 'done',
                                                'cancelled']),
                        required=False)
    address_id = fields.Integer(validate=validate.Range(min=0), required=True)
    user_id = fields.Integer(validate=validate.Range(min=0), required=True)


class CustomToUpdateSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=0))
    price = fields.Float(validate=validate.Range(min=0))
    time = fields.DateTime(format='%Y-%m-%dT%H:%M:%S',
                           validate=lambda x: x <= datetime.datetime.now())
    address_id = fields.Integer(validate=validate.Range(min=0))
    user_id = fields.Integer(validate=validate.Range(min=0))


class CustomUpdateStatusSchema(Schema):
    status = fields.Str(dump_default='registered',
                        validate=validate.OneOf(['registered', 'processed', 'accepted',
                                                'prepared', 'delivered', 'done',
                                                'cancelled']),
                        required=True)


class MenuSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=0))
    name = fields.Str(validate=[validate.Length(min=3, max=45)],
                      required=True)
    price = fields.Float(validate=validate.Range(min=0), required=True)
    availability = fields.Boolean()
    demand = fields.Boolean()


class MenuToUpdateSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=0))
    name = fields.Str(validate=[validate.Length(min=3, max=45)])
    price = fields.Float(validate=validate.Range(min=0))
    availability = fields.Boolean()
    demand = fields.Boolean()


class ProductSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=0))
    name = fields.Str(validate=[validate.Length(min=3, max=45)],
                      required=True)
    price = fields.Float(validate=validate.Range(min=0), required=True)
    weight = fields.Float(validate=validate.Range(min=0), required=True)


class ProductToUpdateSchema(Schema):
    id = fields.Integer(validate=validate.Range(min=0))
    name = fields.Str(validate=[validate.Length(min=3, max=45)])
    price = fields.Float(validate=validate.Range(min=0))
    weight = fields.Float(validate=validate.Range(min=0))


def add_input(model_class, **kwargs):
    input_to_add = model_class(**kwargs)
    db.session.add(input_to_add)
    db.session.commit()
    return input_to_add


def update_input(input_to_update, **kwargs):
    for key, value in kwargs.items():
        setattr(input_to_update, key, value)
    db.session.commit()
    return input_to_update


def delete_input(input_to_delete):
    db.session.delete(input_to_delete)
    db.session.commit()

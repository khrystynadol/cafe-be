import base64
import io

from flask import request, jsonify, render_template, Response, send_file, make_response
from main_folder.models import app, PersonStatus, Person, Custom, Menu, Product, Details, Ingredient, \
    ArchiveCustom, ArchivePerson, MenuPicture  # Address, Details
from werkzeug.security import check_password_hash
from validation.schemas import *
from flask_cors import CORS
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from flask_httpauth import HTTPBasicAuth
import json
from werkzeug.utils import secure_filename

app.debug = True

CORS(app)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(u_email, u_password):
    user_to_verify = Person.query.filter_by(email=u_email).first()
    if user_to_verify and check_password_hash(user_to_verify.password, u_password):
        # print("email: " + u_email + ", password: " + u_password)
        return user_to_verify
    else:
        return None


@auth.error_handler
def auth_error_handler(status):
    message = ""
    if status == 401:
        message = "Wrong email or password"
    if status == 403:
        message = "Access denied"
    return {"code": status, "message": message}, status


@auth.get_user_roles
def get_user_roles(user_to_get_role):
    # print(user_to_get_role.role.value)
    return user_to_get_role.role.value


def error_handler(func):
    def wrapper(**kwargs):  # *args,
        try:
            # result = 0
            if len(kwargs) == 0:
                result = func()
                print(1, result)
            else:
                result = func(**kwargs)
                print(2, result)
            if result.__class__ == tuple and result[1] >= 400:
                print(3, result[0])
                return {"code": result[1],
                        "message": result[0]
                        }, result[1]
            else:
                return result
        except ValidationError as err:
            print(4, err.messages)
            return {"code": 400,
                    "message": err.messages
                    }, 400
        except IntegrityError as err:
            print(5, err.args)
            return {"code": 409,
                    "message": err.args
                    }, 409

    wrapper.__name__ = func.__name__
    return wrapper


@app.route("/user", methods=['POST'])
@error_handler
def user():
    if request.method == 'POST' and request.is_json:
        data_user = PersonSchema().load(request.json)
        new_user = add_input(Person, **data_user)
        return jsonify(PersonSchema().dump(new_user)), 201


@app.route("/user/login", methods=['POST'])
@error_handler
# @auth.login_required(role=['client', 'manager'])
def login():
    if request.method == 'POST':
        login_data = request.get_json()
        user_login = Person.query.filter_by(email=login_data['email']).first()

        if user_login is None:
            return {
                "message": "There is no user with such email"
            }, 412
        elif not check_password_hash(user_login.password, login_data['password']):
            return {
                "message": "Incorrect password"
            }, 412
        else:
            return {
                "id": user_login.id,
                'role': user_login.role.value,
                "message": "Success"
            }, 201
        # print("Person data", jsonify(PersonSchema().dump(auth.current_user())))
    return jsonify(PersonSchema().dump(auth.current_user())), 201


@app.route("/user/logout", methods=['DELETE'])
@auth.login_required(role=['client', 'manager'])
def logout():
    if request.method == 'DELETE':
        return {"message": "Success"}, 200


@app.route("/user/<int:user_id>", methods=['PUT'])
@error_handler
@auth.login_required(role=['client', 'manager'])
def user_update(user_id):
    current_user = auth.current_user()
    # print(user_id, current_user.id)
    if current_user.id != int(user_id):
        return "Access denied", 403
    if request.method == 'PUT':
        person_data = PersonToUpdateSchema().load(request.json)
        person_to_update = Person.query.filter_by(id=user_id).first()
        update_input(person_to_update, **person_data)
        return jsonify(PersonToUpdateSchema().dump(person_to_update)), 200


@app.route("/user/<int:user_id>", methods=['GET', 'DELETE'])
@error_handler
@auth.login_required(role=['client', 'manager'])
def user_to(user_id):
    current_user = auth.current_user()
    # print(user_id, current_user.id)
    if request.method == 'GET':
        u_role = current_user.role.value
        if u_role == 'client' and current_user.id != int(user_id):
            return "Access denied", 403

        person_to_get_info = Person.query.filter_by(id=user_id).first()
        if person_to_get_info is None:
            return "Not found user with such id", 404
        else:
            return jsonify(PersonSchema().dump(person_to_get_info)), 200
    elif request.method == 'DELETE':
        if current_user.id != int(user_id):
            return "Access denied", 403
        elif current_user.id == int(user_id):
            person_to_delete = Person.query.filter_by(id=user_id).first()
            order_to_delete = Custom.query.filter_by(user_id=user_id).all()
            # if person_to_delete is None:
            #     return {"message": "There is no user with such id"}, 404
            # else:
            archive_person = ArchivePerson(name=person_to_delete.name, surname=person_to_delete.surname,
                                           phone=person_to_delete.phone, email=person_to_delete.email,
                                           password=person_to_delete.password, role=person_to_delete.role)
            db.session.add(archive_person)
            archive_person_info = ArchivePerson.query.filter_by(email=person_to_delete.email).first()
            for i in order_to_delete:
                details_to_delete = Details.query.filter_by(custom_id=i.id).all()
                for j in details_to_delete:
                    delete_input(j)
                archive_custom = ArchiveCustom(price=i.price, time=i.time, status=i.status,
                                               user_id=archive_person_info.id)
                db.session.add(archive_custom)
                delete_input(i)
            delete_input(person_to_delete)
            return {"message": "Success"}, 200
        # else:
        #     return {"message": "You try to delete another user"}, 408


@app.route("/user/<int:user_id>/makeManager", methods=['PUT'])
@auth.login_required(role='manager')
def make_m(user_id):
    user_to_work = Person.query.filter_by(id=user_id).first()
    if request.method == 'PUT':
        if user_to_work is None:
            return "Not found user with such id", 404
        elif user_to_work.role == PersonStatus.manager:
            return {"message": "The user already has role manager"}, 408
        else:
            user_to_work.role = PersonStatus.manager.value
            db.session.commit()
            return {"message": "Success"}, 200


@app.route("/user/getAll", methods=['GET'])
@auth.login_required(role='manager')
def get_all_user():
    if request.method == 'GET':
        return json.dumps([p.as_dict() for p in Person.query.all()],
                          indent=4, sort_keys=True, default=str), 200


@app.route("/custom", methods=['POST'])
@error_handler
@auth.login_required(role='client')
def custom():
    current_user = auth.current_user()
    custom_data = CustomSchema().load(request.json)
    if request.method == 'POST' and request.is_json:
        if_details = False
        if "details" in custom_data:
            details = custom_data['details']
            if_details = True
        custom_data.pop('details')
        new_custom = Custom(**custom_data)
        new_custom.time = datetime.datetime.now()
        if new_custom.user_id != current_user.id:
            return "Access denied", 403
        db.session.add(new_custom)
        db.session.commit()
        if if_details:
            # print("Here")
            for detail in details:
                # print("Here", detail)
                details_data = DetailsSchema().load(detail)
                new_detail = Details(**details_data)
                new_detail.custom_id = new_custom.id
                db.session.add(new_detail)
                db.session.commit()
        return jsonify(CustomSchema().dump(new_custom)), 201
        # find_email = Person.query.filter_by(email=data_user.email).first()
        # return {"id": new_custom.id}, 201


@app.route("/custom/<int:custom_id>", methods=['GET', 'DELETE'])
@error_handler
@auth.login_required(role=['client', 'manager'])
def custom_to(custom_id):
    current_user = auth.current_user()
    u_role = current_user.role.value
    custom_info = Custom.query.filter_by(id=custom_id).first()
    if request.method == 'GET':
        custom_to_get_info = Custom.query.filter_by(id=custom_id).first()
        if not custom_to_get_info:
            return {"message": "There is no custom with such id"}, 404
        elif u_role == 'client' and current_user.id != custom_info.user_id:
            return "Access denied", 403
        else:
            return jsonify(CustomSchema().dump(custom_to_get_info)), 200
    elif request.method == 'DELETE':
        custom_to_delete = Custom.query.filter_by(id=custom_id).first()

        if custom_to_delete is None:
            return {"message": "There is no custom with such id"}, 404
        else:
            if current_user.id != custom_info.user_id:
                return "Access denied", 403
            details_to_delete = Details.query.filter_by(custom_id=custom_id).all()
            for i in details_to_delete:
                delete_input(i)
            delete_input(custom_to_delete)
            return {"message": "Success"}, 200


@app.route("/custom/<int:custom_id>", methods=['PUT'])
@error_handler
@auth.login_required(role='manager')
def custom_to_update(custom_id):
    if request.method == 'PUT' and request.is_json:
        custom_data = CustomToUpdateSchema().load(request.json)
        custom_to_update_1 = Custom.query.filter_by(id=custom_id).first()
        if custom_to_update_1 is None:
            return {"message": "There is no custom with such id"}, 404
        else:
            for key, value in custom_data.items():
                setattr(custom_to_update_1, key, value)
            custom_to_update_1.time = datetime.datetime.now()
            db.session.commit()
            return jsonify(CustomToUpdateSchema().dump(custom_to_update_1)), 200


@app.route("/custom/<int:custom_id>/updateStatus", methods=['PUT'])
@error_handler
@auth.login_required(role='manager')
def update_cust_status(custom_id):
    if request.method == 'PUT':
        status_data = CustomUpdateStatusSchema().load(request.json)
        status_to_update = Custom.query.filter_by(id=custom_id).first()
        if status_to_update is None:
            return {"message": "Custom not found"}, 404
        else:
            update_input(status_to_update, **status_data)
            return jsonify(CustomUpdateStatusSchema().dump(status_to_update)), 200


@app.route("/custom/getAll", methods=['GET'])
@auth.login_required(role='manager')
def get_all_cust():
    if request.method == 'GET':
        return json.dumps([p.as_dict() for p in Custom.query.all()],
                          indent=4, sort_keys=True, default=str), 200


@app.route("/menu", methods=['POST'])
@error_handler
@auth.login_required(role='manager')
def menu():
    if request.method == 'POST' and request.is_json:
        menu_data = MenuSchema().load(request.json)
        print(menu_data)
        ingredients = menu_data['ingredients']
        menu_data.pop('ingredients')
        new_menu = add_input(Menu, **menu_data)
        for ingredient in ingredients:
            ingredient_data = IngredientSchema().load(ingredient)
            product_name = ingredient_data['product_name']
            product_info = Product.query.filter_by(name=product_name).first()
            new_ingredient = Ingredient()
            new_ingredient.weight = ingredient_data['weight']
            new_ingredient.product_id = product_info.id
            new_ingredient.menu_id = new_menu.id
            db.session.add(new_ingredient)
            db.session.commit()
        return jsonify(MenuSchema().dump(new_menu)), 201


@app.route("/menu/<int:menu_id>", methods=['GET'])
@error_handler
def menu_to_get(menu_id):
    menu_to_get_info = Menu.query.filter_by(id=menu_id).first()
    if menu_to_get_info is None:
        return {"message": "There is no menu item with such id"}, 404
    else:
        return jsonify(MenuSchema().dump(menu_to_get_info)), 200


@app.route("/menu/<int:menu_id>", methods=['DELETE', 'PUT'])
@error_handler
@auth.login_required(role='manager')
def menu_to(menu_id):
    if request.method == 'DELETE':
        menu_to_delete = Menu.query.filter_by(id=menu_id).first()
        if menu_to_delete is None:
            return {"message": "There is no menu item with such id"}, 404
        else:
            ingredients_to_delete = Ingredient.query.filter_by(menu_id=menu_id).all()
            for i in ingredients_to_delete:
                delete_input(i)
            details_to_delete = Details.query.filter_by(menu_id=menu_id).all()
            for i in details_to_delete:
                delete_input(i)
            delete_input(menu_to_delete)
            return {"message": "Success"}, 200
    elif request.method == 'PUT' and request.is_json:
        menu_data = MenuToUpdateSchema().load(request.json)
        menu_to_update = Menu.query.filter_by(id=menu_id).first()
        if menu_to_update is None:
            return {"message": "Menu item not found"}, 404
        else:
            update_input(menu_to_update, **menu_data)
            return jsonify(MenuToUpdateSchema().dump(menu_to_update)), 200


@app.route("/menu/<int:menu_id>/AddToDemand", methods=['PUT'])
@auth.login_required(role=['client', 'manager'])
def add_to_demand(menu_id):
    if request.method == 'PUT':
        menu_to_demand = Menu.query.filter_by(id=menu_id).first()
        if menu_to_demand is None:
            return {"message": "Menu item not found"}, 404
        else:
            menu_to_demand.demand = True
            db.session.commit()
            return {"message": "Success"}, 200


@app.route("/menu/getAll", methods=['GET'])
def get_all_menu():
    if request.method == 'GET':
        return json.dumps([p.as_dict() for p in Menu.query.all()],
                          indent=4, sort_keys=True, default=str), 200


@app.route("/menu/filter", methods=['PUT'])
@error_handler
@auth.login_required(role=['client', 'manager'])
def menu_filter():
    if request.method == 'PUT' and request.is_json:
        menu_data = request.get_json()
        name_filter = ""
        if "name" in menu_data and menu_data["name"] != []:
            name_filter = menu_data["name"]
        if "products" in menu_data and menu_data["products"] != []:
            products_filter = menu_data["products"]
            ingredients_filter_res = (p.get_menu_id() for p in
                                      Ingredient.query.filter(Ingredient.product_id.in_(products_filter)))
        else:
            ingredients_filter_res = (p.get_menu_id() for p in
                                      Ingredient.query.all())
        all_filter = Menu.query.filter(Menu.id.in_(ingredients_filter_res), Menu.name.like(f"%{name_filter}%"))
        return json.dumps([p.as_dict() for p in all_filter]), 200


@app.route("/product", methods=['POST'])
@error_handler
@auth.login_required(role='manager')
def product():
    if request.method == 'POST' and request.is_json:
        product_data = ProductSchema().load(request.json)
        new_product = add_input(Product, **product_data)
        return jsonify(ProductSchema().dump(new_product)), 201


@app.route("/product/<int:product_id>", methods=['GET', 'DELETE', 'PUT'])
@auth.login_required(role='manager')
def product_to(product_id):
    if request.method == 'GET':
        product_to_get_info = Product.query.filter_by(id=product_id).first()
        if product_to_get_info is None:
            return {"message": "There is no product item with such id"}, 404
        else:
            return jsonify(ProductSchema().dump(product_to_get_info)), 200
    elif request.method == 'DELETE':
        product_to_delete = Product.query.filter_by(id=product_id).first()
        if product_to_delete is None:
            return {"message": "There is no product item with such id"}, 404
        else:
            ingredients_to_delete = Ingredient.query.filter_by(product_id=product_id).all()
            for i in ingredients_to_delete:
                delete_input(i)
            delete_input(product_to_delete)
            return {"message": "Success"}, 200
    elif request.method == 'PUT' and request.is_json:
        product_data = ProductToUpdateSchema().load(request.json)
        product_to_update = Product.query.filter_by(id=product_id).first()
        if product_to_update is None:
            return {"message": "Menu item not found"}, 404
        else:
            update_input(product_to_update, **product_data)
            return jsonify(MenuToUpdateSchema().dump(product_to_update)), 200


@app.route("/product/getAll", methods=['GET'])
@auth.login_required(role='manager')
def get_all_prod():
    if request.method == 'GET':
        return json.dumps([p.as_dict() for p in Product.query.all()],
                          indent=4, sort_keys=True, default=str), 200


@app.route('/upload', methods=['POST'])
@auth.login_required(role='manager')
def upload():
    pic = request.files['picture_data']
    menu_id = request.form.get('menu_id')

    if not pic:
        return 'No pic uploaded!', 400

    filename = secure_filename(pic.filename)
    mimetype = pic.mimetype
    if not filename or not mimetype:
        return 'Bad upload!', 400

    # img = MenuPicture(img=pic['img'], mimetype=pic['mimetype'], name=pic['filename'], menu_id=menu_id)
    img = MenuPicture(img=pic.read(), name=filename, mimetype=mimetype, menu_id=menu_id)
    db.session.add(img)
    db.session.commit()
    return 'Img Uploaded!', 200

    # response = make_response('Img Uploaded!', 200)
    # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:63342')
    # return response
    # response = make_response('Img Uploaded!', 200)
    # response.headers['Access-Control-Allow-Origin'] = '*'


@app.route('/image/getAll', methods=['GET'])
@auth.login_required(role='manager')
def upload_all():
    if request.method == 'GET':
        return json.dumps([p.as_dict() for p in MenuPicture.query.all()],
                          indent=4, sort_keys=True, default=str), 200


@app.route('/image/<int:img_id>', methods=['GET'])
def get_img(img_id):
    image_to_send = MenuPicture.query.filter_by(menu_id=img_id).first()
    if not image_to_send:
        return 'Image Not Found!', 404
    else:
        return {"id": image_to_send.id,
                "img": image_to_send.img,
                "name": image_to_send.name,
                "mimetype": image_to_send.mimetype,
                "menu_id": image_to_send.menu_id
                }
    # padding = b'=' * (4 - len(image_to_send.img) % 4)
    # image_data = base64.b64decode(image_to_send.img.encode() + padding)
    #
    # response = make_response(image_data)
    # response.headers.set('Content-Type', image_to_send.mimetype)
    # response.headers.set('Content-Disposition', 'inline', filename=image_to_send.name)

    # return response
    # padding = b'=' * (4 - len(image_to_send.img) % 4)
    # image_data = base64.b64decode(image_to_send.img.encode() + padding)
    # return send_file(io.BytesIO(image_data), mimetype=image_to_send.mimetype)
    # return {
    #     "image": image_to_send.img,
    #     "mimetype": image_to_send.mimetype
    # }, 200


@app.route('/user/role', methods=['GET'])
@auth.login_required(role=['client', 'manager'])
def get_user_role():
    email = request.args.get('email')
    person = Person.query.filter_by(email=email).first()

    if person is None:
        return jsonify({'error': 'User not found'}), 404

    return jsonify({'role': person.role.value})

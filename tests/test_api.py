import json

from werkzeug.security import generate_password_hash
from validation.schemas import *
from database.models import *
from flask_testing import TestCase
from flask import url_for
# from lab4.blueprint import *
from menuapp import app
import base64

class TestApi(TestCase):
    # def create_tables(self):
    #     db.metadata.drop_all(db)
    #     db.metadata.create_all(db)

    def create_app(self):
        return app

    def get_basic_client_headers(self):
        return {
            "Authorization": "Basic " + base64.b64encode(b"user2@gmail.com:12345").decode("utf8")
        }
    def get_basic_manager_headers(self):
        return {
            "Authorization": "Basic " + base64.b64encode(b"hrystyna@gmail.com:12345").decode("utf8")
        }

    def setUp(self):
        super().setUp()

    def close_session(self):
        db.session.close()

    def tearDown(self):
        self.close_session()


class RoutesTest(TestApi):
    #URL = "http://127.0.0.1:5000/"

    def setUp(self):
        #self.create_tables()
        self.email = 'check2u@gmail.com'
        self.password = "12345"
        self.password_hash = generate_password_hash('12345')
        self.address_data_ok = {"street": "Konyskogo",
                                "house": "125а",
                                "flat": 15}
        self.client_data_ok = {
            "name": "Ivan",
            "surname": "Ivanov",
            "phone": "0934864659",
            "email": "user2@gmail.com",
            "password": "12345",
            "role": PersonStatus.client.value
        }
        self.client2_data_ok = {
            "name": "Ivan",
            "surname": "Ivanov",
            "phone": "0934864659",
            "email": "user3@gmail.com",
            "password": "12345",
            "role": PersonStatus.client.value
        }
        self.manager_data = {
            "name": "Man",
            "surname": "Manager",
            "phone": "0934864659",
            "email": "m1@gmail.com",
            "password": "12345",
            "role": "manager"#PersonStatus.manager.value
        }
        self.product_data_ok = {
            "name": "Coffee",
            "price": 255,
            "weight": 1000
        }
        self.product2_data_ok = {
            "name": "Flour",
            "price": 255,
            "weight": 1000
        }
        self.menu_data_ok = {
            "name": "Late",
            "price": 56,
            "availability": 1,
            "demand": 0
        }
        self.menu2_data_ok = {
            "name": "Cupcake",
            "price": 99,
            "availability": 0,
            "demand": 0
        }
        self.custom_data_ok = {
            "price": 2550,
            "time": '2022-11-10T15:32:11',
            "address_id": 1,
            "user_id": 1
        }
        self.custom2_data_ok = {
            "price": 3000,
            "time": '2022-11-10T20:32:11',
            "address_id": 1,
            "user_id": 1
        }
        self.ingredient_data_ok = {
            "weight": 30,
            "percent": 30,
            "menu_id": 1,
            "product_id": 1}
        self.ingredient2_data_ok = {
            "weight": 70,
            "percent": 10,
            "menu_id": 1,
            "product_id": 1}
        self.details_data_ok = {
            "quantity": 4,
            "custom_id": 1,
            "menu_id": 1
        }

        self.client_data_fail_email = {
            "name": "Ivan",
            "surname": "Ivanov",
            "phone": "0934864659",
            "email": "ivanko@gmail.com",
            "password": "12345",
            "role": PersonStatus.client.value
        }
        self.client_data_fail_password = {
            "name": "Ivan",
            "surname": "Ivanov",
            "phone": "0934864659",
            "email": "user23@gmail.com",
            "password": "123456",
            "role": PersonStatus.client.value
        }


    def test_authenticate_success(self):
        # personSh = PersonSchema().load(self.client_data_ok)
        # person = Person(**personSh)
        # db.session.add(person)
        # db.session.commit()
        resp = self.client.post(url_for("login"), headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)
        self.assertEqual(resp.json["email"], "user2@gmail.com")


    def  test_authenticate_fail_email(self):
        personSh = PersonSchema().load(self.client_data_fail_email)
        person = Person(**personSh)
        db.session.add(person)
        db.session.commit()
        resp = self.client.post(url_for("login"), headers=self.get_basic_client_headers())
        self.assertEqual(400, resp.status_code)

    def test_authenticate_fail_password(self):
        personSh = PersonSchema().load(self.client_data_fail_password)
        person = Person(**personSh)
        db.session.add(person)
        db.session.commit()
        resp = self.client.post(url_for("login"), headers=self.get_basic_client_headers())
        self.assertEqual(400, resp.status_code)#412?

    def test_create_user(self):
        payload = json.dumps(
            self.client_data_ok
        )
        resp = self.client.post(url_for("user"), headers={"Content-Type": "application/json"}, data=payload)
        self.assertEqual(201, resp.status_code)

    def test_logout(self):
        # personSh = PersonSchema().load(self.client_data_ok)
        # person = Person(**personSh)
        # db.session.add(person)
        # db.session.commit()
        resp = self.client.delete(url_for("logout"), headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_update_user(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)
        db.session.add(person)
        db.session.commit()
        payload = json.dumps(
            self.client_data_ok
        )
        headers = self.get_basic_client_headers() # header can be also with manager credentials
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("user_update", user_id=person.id),  headers=headers, data=payload )
        self.assertEqual(200, resp.status_code)

    def test_update_user_status(self):
        personSh = PersonSchema().load(self.client_data_ok)
        person = Person(**personSh)

        personSh = PersonSchema().load(self.manager_data)
        person2 = Person(**personSh)
        db.session.add(person)
        db.session.add(person2)
        db.session.commit()
        payload = json.dumps(
            self.client_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("make_m", id=person.id), headers=headers, data=payload)
        self.assertEqual(201, resp.status_code)

    def test_delete_user(self):
        # personSh = PersonSchema().load(self.client2_data_ok)
        # person1 = Person(**personSh)

        # personSh = PersonSchema().load(self.manager_data)
        # person2 = Person(**personSh)
        # db.session.add(person1)
        # db.session.add(person2)
        # db.session.commit()
        resp = self.client.delete(url_for("user_to", user_id=2), headers=self.get_basic_manager_headers())
        self.assertEqual(201, resp.status_code)

    def test_get_user(self):
        # personSh = PersonSchema().load(self.client_data_ok)
        # person = Person(**personSh)
        # db.session.add(person)
        # db.session.commit()
        resp = self.client.get(url_for("user_to", user_id=1),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_all_users(self):
        # personSh = PersonSchema().load(self.client_data_ok)
        # person1 = Person(**personSh)
        # personSh = PersonSchema().load(self.manager_data)
        # person2 = Person(**personSh)
        # db.session.add(person1)
        # db.session.add(person2)
        # db.session.commit()
        resp = self.client.get(url_for("get_all_user"),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)


    #####################   CUSTOM    #####################
    def test_update_custom(self):

        custommSh = CustomSchema().load(self.custom_data_ok)
        customm = Custom(**custommSh)

        customSh = CustomToUpdateSchema().load(self.custom2_data_ok)
        custom = Custom(**customSh)

        db.session.add(customm)
        db.session.add(custom)
        db.session.commit()
        payload = json.dumps(
            self.custom2_data_ok
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("custom_to", custom_id=customm.id), headers=headers, data=payload)
        self.assertEqual(201, resp.status_code)

    def test_create_custom(self):
        payload = json.dumps(
            self.custom2_data_ok
        )
        customSh = CustomSchema().load(self.custom2_data_ok)
        custom = Custom(**customSh)
        db.session.add(custom)
        db.session.commit()
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("custom"), headers=headers, data=payload)
        self.assertEqual(201, resp.status_code)

    def test_get_custom(self):
        resp = self.client.get(url_for("custom_to", custom_id=1),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)


    def test_get_all_customs(self):
        resp = self.client.get(url_for("get_all_cust"),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    def test_delete_custom(self):
        resp = self.client.delete(url_for("custom_to", custom_id=2), headers=self.get_basic_manager_headers())
        self.assertEqual(201, resp.status_code)

 #####################   MENU   #####################

    def test_update_menu(self):
        menuSh = MenuSchema().load(self.menu_data_ok)
        menu = Menu(**menuSh)

        # customSh = CustomToUpdateSchema().load(self.customUpdate_data_ok)
        # custom = Custom(**customSh)
        #
        # db.session.add(customm)
        db.session.add(menu)
        db.session.commit()
        payload = json.dumps(
            self.menu2_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("menu_to", menu_id=menu.id), headers=headers, data=payload)
        self.assertEqual(201, resp.status_code)


    def test_create_menu(self):
        menuSh = MenuSchema().load(self.menu2_data_ok)
        menu = Menu(**menuSh)
        db.session.add(menu)
        db.session.commit()
        payload = json.dumps(
            self.menu2_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("menu"), headers=headers, data=payload)
        self.assertEqual(201, resp.status_code)


    def test_get_menu(self):
        resp = self.client.get(url_for("menu_to_get", menu_id=1),
                               headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)


    def test_get_all_menues(self):
        resp = self.client.get(url_for("get_all_menu"),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)


    def test_delete_menu(self):
        resp = self.client.delete(url_for("menu_to", menu_id=1), headers=self.get_basic_manager_headers())
        self.assertEqual(201, resp.status_code)

     #####################   Product   #####################

    def test_update_product(self):
        productSh = ProductSchema().load(self.product_data_ok)
        product = Product(**productSh)

        db.session.add(product)
        # db.session.add(custom)
        db.session.commit()
        payload = json.dumps(
            self.product_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("product_to", product_id=product.id), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)


    def test_create_product(self):
        payload = json.dumps(
            self.product_data_ok
        )
        productSh = ProductSchema().load(self.product_data_ok)
        product = Product(**productSh)
        db.session.add(product)
        db.session.commit()
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("product"), headers=headers, data=payload)
        self.assertEqual(201, resp.status_code)


    def test_get_product(self):
        resp = self.client.get(url_for("product_to", product_id=1),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)


    def test_get_all_products(self):
        resp = self.client.get(url_for("get_all_prod"),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)


    def test_delete_product(self):
        resp = self.client.delete(url_for("product_to", product_id=1), headers=self.get_basic_manager_headers())
        self.assertEqual(201, resp.status_code)
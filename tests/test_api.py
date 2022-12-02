import json
from validation.schemas import *
from main_folder.models import *
from flask_testing import TestCase
from flask import url_for
from main_folder.menuapp import app
import base64


class TestApi(TestCase):
    def create_tables(self):
        db.drop_all()
        db.create_all()

    def setUp(self):
        super().setUp()

    def get_basic_client_headers(self):
        return {
            "Authorization": "Basic " + base64.b64encode(b"user2@gmail.com:12345").decode("utf8")
        }

    def get_basic_manager_headers(self):
        return {
            "Authorization": "Basic " + base64.b64encode(b"m1@gmail.com:12345").decode("utf8")
        }

    def close_session(self):
        db.session.close()

    def tearDown(self):
        self.close_session()

    def create_app(self):
        return app


class RoutesTest(TestApi):
    # URL = "http://127.0.0.1:5000/"

    def setUp(self):
        self.create_tables()
        self.email = 'check2u@gmail.com'
        self.password = "12345"
        self.password_hash = generate_password_hash('12345')
        self.address_data_ok = {"street": "Konyskogo",
                                "house": "125а",
                                "flat": 15}
        self.address1_data_ok = Address(street="Konyskogo", house="125а", flat=15)
        self.address2_data_ok = Address(street="Franka", house="55", flat=2)
        self.address3_data_ok = Address(street="Naukova", house="29", flat=24)
        self.client_data_ok = {
            "name": "Ivan",
            "surname": "Ivanov",
            "phone": "0934864659",
            "email": "user2@gmail.com",
            "password": "12345",
            "role": "client"
        }
        self.client2_data_ok = {
            "name": "Ivan",
            "surname": "Ivanov",
            "phone": "0934864659",
            "email": "user3@gmail.com",
            "password": "12345",
            "role": "client"
        }
        self.client_data_bad_phone = {
            "name": "Ivan",
            "surname": "Ivanov",
            "phone": "0934gp64659",
            "email": "user3@gmail.com",
            "password": "12345",
            "role": "client"
        }
        self.client2_data_bad_phone = {
            "name": "Ivan",
            "surname": "Ivanov",
            "phone": "0934g64659",
            "email": "user3@gmail.com",
            "password": "12345",
            "role": "client"
        }
        self.client_data_bad_phone_update = {
            "phone": "0934gp64659"
        }
        self.client2_data_bad_phone_update = {
            "phone": "0934g64659"
        }
        self.manager_data = {
            "name": "Man",
            "surname": "Manager",
            "phone": "0934864659",
            "email": "m1@gmail.com",
            "password": "12345",
            "role": "manager"
        }
        self.product_data_ok = {
            "name": "Coffee",
            "price": 1000,
            "weight": 1000
        }
        self.product2_data_ok = {
            "name": "Flour",
            "price": 30,
            "weight": 1000
        }
        self.menu_data_ok = {
            "name": "Late",
            "price": 56,
            "availability": 1,
            "demand": 0,
            "ingredients": [
                {
                    "weight": 30,
                    "percent": 30,
                    "product_id": 1
                },
                {
                    "weight": 30,
                    "percent": 30,
                    "product_id": 2
                }
            ]
        }
        self.menu2_data_ok = {
            "name": "Cupcake",
            "price": 99,
            "availability": 0,
            "demand": 0,
            "ingredients": [
                {
                    "weight": 30,
                    "percent": 30,
                    "product_id": 1
                }
            ]
        }
        self.menu2_data_ok_to_update = {
            "name": "Cupcake",
            "price": 99,
            "availability": 0,
            "demand": 0
        }
        self.custom_data_ok = {
            "price": 2550,
            "time": '2022-11-10T15:32:11',
            "address_id": 1,
            "user_id": 1,
            "details": [
                {
                    "quantity": 4,
                    "menu_id": 1
                },
                {
                    "quantity": 2,
                    "menu_id": 2
                }
            ]
        }
        self.custom_data_ok_to_update = {
            "price": 2550,
            "time": '2022-11-10T15:32:11',
            "address_id": 1,
            "user_id": 1
        }
        self.custom_status_data_ok = {
            "status": "cancelled"
        }
        self.custom2_data_ok = {
            "price": 3000,
            "time": '2022-11-10T20:32:11',
            "address_id": 1,
            "user_id": 2,
            "details": [
                {
                    "quantity": 4,
                    "menu_id": 1
                }
            ]
        }
        self.custom2_data_ok_to_update = {
            "price": 3000,
            "time": '2022-11-10T20:32:11',
            "address_id": 1,
            "user_id": 2
        }
        self.ingredient_data_ok = {
            "weight": 30,
            "percent": 30,
            "menu_id": 1,
            "product_id": 1
        }
        self.ingredient2_data_ok = {
            "weight": 70,
            "percent": 10,
            "menu_id": 1,
            "product_id": 1
        }
        self.details_data_ok = {
            "quantity": 4,
            "custom_id": 1,
            "menu_id": 1
        }
        self.filter_data_ok = {
            "name": "Late",
            "products": [1]
        }
        self.filter_data_ok_no_ingredients = {
            "name": "Late"
        }
        self.details_1 = Details(quantity=4, custom_id=1, menu_id=1)
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
        person_data = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data)
        resp = self.client.post(url_for("login"),
                                headers=self.get_basic_client_headers())
        self.assertEqual(201, resp.status_code)
        self.assertEqual(resp.json["email"], "user2@gmail.com")

    def test_authenticate_fail_email(self):
        person_data = PersonSchema().load(self.client_data_fail_email)
        add_input(Person, **person_data)
        resp = self.client.post(url_for("login"),
                                headers=self.get_basic_client_headers())
        self.assertEqual(401, resp.status_code)

    def test_authenticate_fail_password(self):
        person_data = PersonSchema().load(self.client_data_fail_password)
        add_input(Person, **person_data)
        resp = self.client.post(url_for("login"),
                                headers=self.get_basic_client_headers())
        self.assertEqual(401, resp.status_code)

    def test_create_user(self):
        payload = json.dumps(
            self.client_data_ok
        )
        resp = self.client.post(url_for("user"),
                                headers={"Content-Type": "application/json"},
                                data=payload)
        self.assertEqual(201, resp.status_code)

    def test_create_user_fail_email(self):
        person_data = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data)
        payload = json.dumps(
            self.client_data_ok
        )
        resp = self.client.post(url_for("user"),
                                headers={"Content-Type": "application/json"},
                                data=payload)
        self.assertEqual(409, resp.status_code)

    def test_create_user_fail_phone(self):
        payload = json.dumps(
            self.client_data_bad_phone
        )
        resp = self.client.post(url_for("user"),
                                headers={"Content-Type": "application/json"},
                                data=payload)
        self.assertEqual(400, resp.status_code)

    def test_create_user_fail_phone_size(self):
        payload = json.dumps(
            self.client2_data_bad_phone
        )
        resp = self.client.post(url_for("user"),
                                headers={"Content-Type": "application/json"},
                                data=payload)
        self.assertEqual(400, resp.status_code)

    def test_logout(self):
        person_data = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data)
        resp = self.client.delete(url_for("logout"),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_update_user(self):
        person_data = PersonSchema().load(self.client_data_ok)
        person_to_update = add_input(Person, **person_data)
        payload = json.dumps(
            self.client_data_ok
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("user_update", user_id=person_to_update.id),
                               headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_update_user_bad_phone(self):
        person_data = PersonSchema().load(self.client_data_ok)
        person_to_update = add_input(Person, **person_data)
        payload = json.dumps(
            self.client_data_bad_phone_update
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("user_update", user_id=person_to_update.id),
                               headers=headers, data=payload)
        self.assertEqual(400, resp.status_code)

    def test_update_user_bad_phone_size(self):
        person_data = PersonSchema().load(self.client_data_ok)
        person_to_update = add_input(Person, **person_data)
        payload = json.dumps(
            self.client2_data_bad_phone_update
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("user_update", user_id=person_to_update.id),
                               headers=headers, data=payload)
        self.assertEqual(400, resp.status_code)

    def test_update_user_access_denied(self):
        person_data = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data)
        payload = json.dumps(
            self.client_data_ok
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("user_update", user_id=2),
                               headers=headers, data=payload)
        self.assertEqual(403, resp.status_code)

    def test_update_user_status(self):
        person_data_1 = PersonSchema().load(self.client_data_ok)
        person = add_input(Person, **person_data_1)

        person_data_2 = PersonSchema().load(self.manager_data)
        add_input(Person, **person_data_2)

        payload = json.dumps(
            self.client_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("make_m", user_id=person.id),
                               headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_update_user_status_no_user(self):
        person_data_2 = PersonSchema().load(self.manager_data)
        add_input(Person, **person_data_2)

        payload = json.dumps(
            self.client_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("make_m", user_id=2),
                               headers=headers, data=payload)
        self.assertEqual(404, resp.status_code)

    def test_update_user_status_already_manager(self):
        person_data_2 = PersonSchema().load(self.manager_data)
        add_input(Person, **person_data_2)

        payload = json.dumps(
            self.client_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("make_m", user_id=1),
                               headers=headers, data=payload)
        self.assertEqual(408, resp.status_code)

    def test_get_user(self):
        person_data = PersonSchema().load(self.client_data_ok)
        person_1 = add_input(Person, **person_data)

        resp = self.client.get(url_for("user_to", user_id=person_1.id),
                               headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_user_no_user(self):
        person_data = PersonSchema().load(self.manager_data)
        person_1 = add_input(Person, **person_data)

        resp = self.client.get(url_for("user_to", user_id=2),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(404, resp.status_code)

    def test_get_user_access_denied(self):
        person_data = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data)
        person_data_2 = PersonSchema().load(self.client2_data_ok)
        add_input(Person, **person_data_2)

        resp = self.client.get(url_for("user_to", user_id=2),
                               headers=self.get_basic_client_headers())
        self.assertEqual(403, resp.status_code)

    def test_delete_user(self):
        menu_data = MenuSchema().load(self.menu_data_ok)
        menu_data.pop('ingredients')
        add_input(Menu, **menu_data)
        person_data = PersonSchema().load(self.client_data_ok)
        person_1 = add_input(Person, **person_data)
        db.session.add(self.address1_data_ok)
        db.session.commit()
        custom_data_1 = CustomSchema().load(self.custom_data_ok)
        custom_data_1.pop('details')
        add_input(Custom, **custom_data_1)
        db.session.add(self.details_1)
        db.session.commit()

        resp = self.client.delete(url_for("user_to", user_id=person_1.id),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_delete_user_access_denied(self):
        person_data = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data)
        person_data_2 = PersonSchema().load(self.client2_data_ok)
        add_input(Person, **person_data_2)

        resp = self.client.delete(url_for("user_to", user_id=2),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(403, resp.status_code)

    def test_get_all_users(self):
        person_data_1 = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_1)
        person_data_2 = PersonSchema().load(self.manager_data)
        add_input(Person, **person_data_2)

        resp = self.client.get(url_for("get_all_user"),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    #   CUSTOM    #
    def test_create_custom(self):
        person_data_1 = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_1)
        menu_data_1 = MenuSchema().load(self.menu_data_ok)
        menu_data_1.pop('ingredients')
        add_input(Menu, **menu_data_1)
        menu_data_2 = MenuSchema().load(self.menu2_data_ok)
        menu_data_2.pop('ingredients')
        add_input(Menu, **menu_data_2)
        # address_data_1 = AddressSchema().load(self.address_data_ok)
        # address = add_input(Address, **self.address2_data_ok)
        db.session.add(self.address1_data_ok)
        db.session.commit()
        payload = json.dumps(
            self.custom_data_ok
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("custom"), headers=headers, data=payload)
        self.assertEqual(201, resp.status_code)

    def test_create_custom_access_denied(self):
        person_data_2 = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_2)
        person_data_1 = PersonSchema().load(self.client2_data_ok)
        add_input(Person, **person_data_1)
        db.session.add(self.address1_data_ok)
        db.session.commit()
        payload = json.dumps(
            self.custom2_data_ok
        )
        # custom_to_add = CustomSchema().load(self.custom2_data_ok)
        # add_input(Custom, **custom_to_add)
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("custom"), headers=headers, data=payload)
        self.assertEqual(403, resp.status_code)

    def test_get_custom(self):
        person_data_for_custom = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_for_custom)
        db.session.add(self.address1_data_ok)
        db.session.commit()
        custom_data_1 = CustomSchema().load(self.custom_data_ok)
        custom_data_1.pop('details')
        custom_1 = add_input(Custom, **custom_data_1)

        resp = self.client.get(url_for("custom_to", custom_id=custom_1.id),
                               headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_custom_no_custom(self):
        person_data_for_custom = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_for_custom)

        resp = self.client.get(url_for("custom_to", custom_id=1),
                               headers=self.get_basic_client_headers())
        self.assertEqual(404, resp.status_code)

    def test_get_custom_access_denied(self):
        person_data_2 = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_2)
        person_data_1 = PersonSchema().load(self.client2_data_ok)
        add_input(Person, **person_data_1)
        db.session.add(self.address1_data_ok)
        db.session.commit()
        custom_data_1 = CustomSchema().load(self.custom2_data_ok)
        custom_data_1.pop('details')
        custom_1 = add_input(Custom, **custom_data_1)

        resp = self.client.get(url_for("custom_to", custom_id=custom_1.id),
                               headers=self.get_basic_client_headers())
        self.assertEqual(403, resp.status_code)

    def test_delete_custom(self):
        person_data_for_custom = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_for_custom)
        menu_data = MenuSchema().load(self.menu_data_ok)
        menu_data.pop('ingredients')
        add_input(Menu, **menu_data)
        db.session.add(self.address1_data_ok)
        db.session.commit()
        custom_data_1 = CustomSchema().load(self.custom_data_ok)
        custom_data_1.pop('details')
        custom_1 = add_input(Custom, **custom_data_1)
        detail_data = DetailsSchema().load(self.details_data_ok)
        add_input(Details, **detail_data)
        resp = self.client.delete(url_for("custom_to", custom_id=custom_1.id),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(200, resp.status_code)

    def test_delete_custom_no_custom(self):
        person_data_for_custom = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_for_custom)

        resp = self.client.delete(url_for("custom_to", custom_id=1),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(404, resp.status_code)

    def test_delete_custom_access_denied(self):
        person_data_1 = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_1)
        person_data_for_custom_2 = PersonSchema().load(self.client2_data_ok)
        add_input(Person, **person_data_for_custom_2)
        db.session.add(self.address1_data_ok)
        db.session.commit()
        custom_data_1 = CustomSchema().load(self.custom2_data_ok)
        custom_data_1.pop('details')
        custom_1 = add_input(Custom, **custom_data_1)
        resp = self.client.delete(url_for("custom_to", custom_id=custom_1.id),
                                  headers=self.get_basic_client_headers())
        self.assertEqual(403, resp.status_code)

    def test_update_custom(self):
        person_data_1 = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_1)
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)
        db.session.add(self.address1_data_ok)
        db.session.commit()
        custom_data_1 = CustomSchema().load(self.custom_data_ok)
        custom_data_1.pop('details')
        custom_1 = add_input(Custom, **custom_data_1)

        payload = json.dumps(
            self.custom_data_ok_to_update
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("custom_to", custom_id=custom_1.id), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_update_custom_no_custom(self):
        person_data_1 = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_1)
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)

        payload = json.dumps(
            self.custom_data_ok_to_update
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("custom_to", custom_id=1), headers=headers, data=payload)
        self.assertEqual(404, resp.status_code)

    def test_update_custom_access_denied(self):
        person_data_2 = PersonSchema().load(self.client2_data_ok)
        add_input(Person, **person_data_2)
        person_data_1 = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_1)
        db.session.add(self.address3_data_ok)
        db.session.commit()
        custom_data_1 = CustomSchema().load(self.custom_data_ok)
        custom_data_1.pop('details')
        custom_1 = add_input(Custom, **custom_data_1)

        payload = json.dumps(
            self.custom_data_ok_to_update
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("custom_to", custom_id=custom_1.id), headers=headers, data=payload)
        self.assertEqual(403, resp.status_code)

    def test_update_cust_status(self):
        db.session.add(self.address1_data_ok)
        db.session.commit()
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)
        person_data_1 = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_1)
        custom_data_1 = CustomSchema().load(self.custom_data_ok)
        custom_data_1.pop('details')
        custom_1 = add_input(Custom, **custom_data_1)

        payload = json.dumps(
            self.custom_status_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("update_cust_status", custom_id=custom_1.id),
                               headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_update_cust_status_no_cust(self):
        person_data_1 = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_1)
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)

        payload = json.dumps(
            self.custom_status_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("update_cust_status", custom_id=1),
                               headers=headers, data=payload)
        self.assertEqual(404, resp.status_code)

    def test_get_all_customs(self):
        db.session.add(self.address1_data_ok)
        db.session.commit()
        person_data_for_custom = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_for_custom)
        custom_data_1 = CustomSchema().load(self.custom_data_ok)
        custom_data_1.pop('details')
        add_input(Custom, **custom_data_1)
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)

        resp = self.client.get(url_for("get_all_cust"),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    #  MENU   #
    def test_create_menu(self):
        product_data_1 = ProductSchema().load(self.product_data_ok)
        add_input(Product, **product_data_1)
        product_data_2 = ProductSchema().load(self.product2_data_ok)
        add_input(Product, **product_data_2)
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)
        payload = json.dumps(
            self.menu_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("menu"), headers=headers, data=payload)
        self.assertEqual(201, resp.status_code)

    def test_get_menu(self):
        menu_data = MenuSchema().load(self.menu_data_ok)
        menu_data.pop('ingredients')
        menu = add_input(Menu, **menu_data)
        resp = self.client.get(url_for("menu_to_get", menu_id=menu.id))
        self.assertEqual(200, resp.status_code)

    def test_get_menu_no_menu(self):
        resp = self.client.get(url_for("menu_to_get", menu_id=1))
        self.assertEqual(404, resp.status_code)

    def test_delete_menu(self):
        menu_data = MenuSchema().load(self.menu_data_ok)
        menu_data.pop('ingredients')
        menu = add_input(Menu, **menu_data)
        product_data_1 = ProductSchema().load(self.product_data_ok)
        add_input(Product, **product_data_1)
        ingredient_data_1 = IngredientSchema().load(self.ingredient_data_ok)
        add_input(Ingredient, **ingredient_data_1)
        person_data_for_custom = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data_for_custom)
        db.session.add(self.address1_data_ok)
        db.session.commit()
        custom_data_1 = CustomSchema().load(self.custom_data_ok)
        custom_data_1.pop('details')
        add_input(Custom, **custom_data_1)
        detail_data = DetailsSchema().load(self.details_data_ok)
        add_input(Details, **detail_data)
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)

        resp = self.client.delete(url_for("menu_to", menu_id=menu.id), headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    def test_delete_menu_no_menu(self):
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)

        resp = self.client.delete(url_for("menu_to", menu_id=1), headers=self.get_basic_manager_headers())
        self.assertEqual(404, resp.status_code)

    def test_update_menu(self):
        menu_data = MenuSchema().load(self.menu2_data_ok)
        menu_data.pop('ingredients')
        menu = add_input(Menu, **menu_data)
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)

        payload = json.dumps(
            self.menu2_data_ok_to_update
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("menu_to", menu_id=menu.id), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_update_menu_no_menu(self):
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)

        payload = json.dumps(
            self.menu2_data_ok_to_update
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("menu_to", menu_id=1), headers=headers, data=payload)
        self.assertEqual(404, resp.status_code)

    def test_add_to_demand(self):
        menu_data = MenuSchema().load(self.menu_data_ok)
        menu_data.pop('ingredients')
        menu = add_input(Menu, **menu_data)
        person_data = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data)

        headers = self.get_basic_client_headers()
        resp = self.client.put(url_for("add_to_demand", menu_id=menu.id), headers=headers)
        self.assertEqual(200, resp.status_code)

    def test_add_to_demand_no_menu(self):
        person_data = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data)

        headers = self.get_basic_client_headers()
        resp = self.client.put(url_for("add_to_demand", menu_id=1), headers=headers)
        self.assertEqual(404, resp.status_code)

    def test_get_all_menus(self):
        menu_data = MenuSchema().load(self.menu_data_ok)
        menu_data.pop('ingredients')
        add_input(Menu, **menu_data)
        # person_data = PersonSchema().load(self.client_data_ok)
        # person_1 = add_input(Person, **person_data)
        resp = self.client.get(url_for("get_all_menu"))
        # headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    def test_menu_filter(self):
        person_data = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data)
        product_data_1 = ProductSchema().load(self.product_data_ok)
        add_input(Product, **product_data_1)
        product_data_2 = ProductSchema().load(self.product2_data_ok)
        add_input(Product, **product_data_2)
        menu_data = MenuSchema().load(self.menu_data_ok)
        menu_data.pop('ingredients')
        add_input(Menu, **menu_data)
        payload = json.dumps(
            self.filter_data_ok
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("menu_filter"),
                               headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_menu_filter_no_ingredients(self):
        product_data_1 = ProductSchema().load(self.product_data_ok)
        add_input(Product, **product_data_1)
        menu_data = MenuSchema().load(self.menu2_data_ok)
        menu_data.pop('ingredients')
        add_input(Menu, **menu_data)
        person_data = PersonSchema().load(self.client_data_ok)
        add_input(Person, **person_data)
        payload = json.dumps(
            self.filter_data_ok_no_ingredients
        )
        headers = self.get_basic_client_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("menu_filter"),
                               headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    #   Product   #

    def test_create_product(self):
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)
        payload = json.dumps(
            self.product_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.post(url_for("product"), headers=headers, data=payload)
        self.assertEqual(201, resp.status_code)

    def test_get_product(self):
        product_data = ProductSchema().load(self.product_data_ok)
        product = add_input(Product, **product_data)
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)

        resp = self.client.get(url_for("product_to", product_id=product.id),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    def test_get_product_no_product(self):
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)

        resp = self.client.get(url_for("product_to", product_id=1),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(404, resp.status_code)

    def test_delete_product(self):
        menu_data = MenuSchema().load(self.menu_data_ok)
        menu_data.pop('ingredients')
        add_input(Menu, **menu_data)
        product_data = ProductSchema().load(self.product_data_ok)
        product = add_input(Product, **product_data)
        ingredient_data_1 = IngredientSchema().load(self.ingredient_data_ok)
        add_input(Ingredient, **ingredient_data_1)
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)

        resp = self.client.delete(url_for("product_to", product_id=product.id),
                                  headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

    def test_delete_product_no_product(self):
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)

        resp = self.client.delete(url_for("product_to", product_id=1),
                                  headers=self.get_basic_manager_headers())
        self.assertEqual(404, resp.status_code)

    def test_update_product(self):
        product_data = ProductSchema().load(self.product_data_ok)
        product = add_input(Product, **product_data)
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)

        payload = json.dumps(
            self.product_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("product_to", product_id=product.id), headers=headers, data=payload)
        self.assertEqual(200, resp.status_code)

    def test_update_product_no_product(self):
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)

        payload = json.dumps(
            self.product_data_ok
        )
        headers = self.get_basic_manager_headers()
        headers["Content-Type"] = "application/json"
        resp = self.client.put(url_for("product_to", product_id=1), headers=headers, data=payload)
        self.assertEqual(404, resp.status_code)

    def test_get_all_products(self):
        product_data = ProductSchema().load(self.product_data_ok)
        add_input(Product, **product_data)
        manager_data_1 = PersonSchema().load(self.manager_data)
        add_input(Person, **manager_data_1)

        resp = self.client.get(url_for("get_all_prod"),
                               headers=self.get_basic_manager_headers())
        self.assertEqual(200, resp.status_code)

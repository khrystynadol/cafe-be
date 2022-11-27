from database.models import app, db, PersonStatus, Person, Product, Menu, Ingredient, Details, Custom, Address
from werkzeug.security import generate_password_hash
with app.app_context():

      person1 = Person(name="Khrystyna", surname="Dolynska", phone="0962250511",
                      email="hrystyna@gmail.com", password=generate_password_hash("12345"), role=PersonStatus.manager.value)
      db.session.add(person1)
    # person2 = Person(name="Ivan", surname="Ivanov", phone="0934864659",
    #                  email="user2@gmail.com", password=generate_password_hash("12345"), role=PersonStatus.client.value)
    # person3 = Person(name="Kate", surname="Lover", phone="0685222554",
    #                  email="user3@gmail.com", password=generate_password_hash("12345"), role=PersonStatus.client.value)

      address1 = Address(street="Konyskogo", house="125а", flat=15)
      address2 = Address(street="Franka", house="55", flat=2)
    #
      product1 = Product(name="Coffee", price=255, weight=1000)
      product2 = Product(name="Flour", price=100, weight=1000)

      menu1 = Menu(name="Late", price=56, availability=1, demand=0)
      menu2 = Menu(name="Cupcake", price=99, availability=0, demand=0)


    # db.session.add(person2)
    # db.session.add(person3)
      db.session.add(address1)
      db.session.add(address2)
      db.session.add(product1)
      db.session.add(product2)
      db.session.add(menu1)
      db.session.add(menu2)
      db.session.commit()

      ingredient1 = Ingredient(weight=30, percent=30, menu_id=menu1.id, product_id=product1.id)
      ingredient2 = Ingredient(weight=70, percent=15, menu_id=menu2.id, product_id=product2.id)
    #
      custom1 = Custom(price=2550, time='2022-11-10 15:32:11',
                      address_id=address1.id, user_id=person1.id)
    # custom2 = Custom(price=999, time='2022-11-7 10:01:55',
    #                  address_id=address2.id, user_id=person3.id)
    # custom3 = Custom(price=1500, time='2022-10-20 10:01:00',
    #                  address_id=address2.id, user_id=person3.id)

      db.session.add(ingredient1)
      db.session.add(ingredient2)
    # db.session.add(custom1)
    # db.session.add(custom2)
    # db.session.add(custom3)
      db.session.commit()
    #
      details1 = Details(quantity=4, custom_id=custom1.id, menu_id=menu2.id)
    # details2 = Details(quantity=1, custom_id=custom3.id, menu_id=menu2.id)
    # details3 = Details(quantity=3, custom_id=custom2.id, menu_id=menu1.id)
    #
      db.session.add(details1)
    # db.session.add(details2)
    # db.session.add(details3)
      db.session.commit()

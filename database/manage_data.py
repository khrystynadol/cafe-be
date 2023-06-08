from main_folder.models import app, db, PersonStatus, Person, Product, Menu, Ingredient, Details, Custom, Address
from werkzeug.security import generate_password_hash

with app.app_context():
    person1 = Person(name="Khrystyna", surname="Dolynska", phone="0962250511",
                     email="manager1@gmail.com", password=generate_password_hash("12345a"),
                     role=PersonStatus.manager.value)
    db.session.add(person1)
    person2 = Person(name="Ivan", surname="Ivanov", phone="0934864659",
                     email="user2@gmail.com", password=generate_password_hash("12345a"),
                     role=PersonStatus.client.value)
    person3 = Person(name="Kate", surname="Lover", phone="0685222554",
                     email="user3@gmail.com", password=generate_password_hash("12345a"),
                     role=PersonStatus.client.value)

    address1 = Address(street="Konyskogo", house="125а", flat=15)
    address2 = Address(street="Franka", house="55", flat=2)

    product1 = Product(name="Coffee", price=1000, weight=1000)
    product2 = Product(name="Milk", price=35, weight=1000)
    product3 = Product(name="Water", price=10, weight=1000)
    product4 = Product(name="Flour", price=30, weight=1000)
    product5 = Product(name="Sugar", price=150, weight=1000)
    product6 = Product(name="Oil", price=100, weight=1000)
    product7 = Product(name="Cinnamon", price=2000, weight=1000)
    product8 = Product(name="Kakao", price=100, weight=1000)
    product9 = Product(name="Eggs", price=750, weight=1000)
    product10 = Product(name="Butter", price=300, weight=1000)
    product11 = Product(name="Salt", price=400, weight=1000)

    # menu1 = Menu(name="Late", description="tasty", price=75, weight=250, availability=1, demand=0, percent=30)
    # menu2 = Menu(name="Cupcake", description="tasty", price=55, weight=150, availability=1, demand=0, percent=25)
    # menu3 = Menu(name="Cappuccino", description="tasty", price=70, weight=250, availability=1, demand=0, percent=30)
    # menu4 = Menu(name="Kakao", description="tasty", price=65, weight=250, availability=1, demand=0, percent=30)
    # menu5 = Menu(name="Tea", description="tasty", price=65, weight=250, availability=1, demand=0, percent=30)

    # menu1 = Menu(name="Ice cream muffin",
    #              description="Satisfy your sweet tooth with our Ice Cream Muffin, which features a warm, moist "
    #                          "muffin topped with a scoop of creamy ice cream",
    #              price=55, weight=100, availability=1, demand=0, percent=10)
    # menu2 = Menu(name="", description="", price=, weight=, availability=1, demand=0, percent=10)
    # menu3 = Menu(name="", description="", price=, weight=, availability=1, demand=0, percent=15)
    # menu4 = Menu(name="", description="", price=, weight=, availability=1, demand=0, percent=15)
    # menu5 = Menu(name="", description="", price=, weight=, availability=1, demand=0, percent=20)
    db.session.add_all([person1, person2, person3])
    db.session.add(address1)
    db.session.add(address2)
    db.session.add_all([product1, product2, product3, product4, product5,
                        product6, product7, product8, product9, product10,
                        product11])
    # db.session.add_all([menu1, menu2, menu3, menu4, menu5])
    db.session.commit()
    #
    # ingredient1 = Ingredient(weight=250, menu_id=menu1.id, product_id=product2.id)
    # ingredient2 = Ingredient(weight=30, menu_id=menu1.id, product_id=product1.id)
    # ingredient3 = Ingredient(weight=3, menu_id=menu1.id, product_id=product7.id)
    # ingredient4 = Ingredient(weight=15, menu_id=menu3.id, product_id=product1.id)
    # ingredient5 = Ingredient(weight=200, menu_id=menu3.id, product_id=product2.id)
    # ingredient6 = Ingredient(weight=50, menu_id=menu4.id, product_id=product8.id)
    # ingredient7 = Ingredient(weight=200, menu_id=menu4.id, product_id=product2.id)
    # ingredient8 = Ingredient(weight=30, menu_id=menu2.id, product_id=product4.id)
    # ingredient9 = Ingredient(weight=30, menu_id=menu2.id, product_id=product5.id)
    # ingredient10 = Ingredient(weight=20, menu_id=menu2.id, product_id=product9.id)
    # ingredient11 = Ingredient(weight=30, menu_id=menu2.id, product_id=product2.id)
    # ingredient12 = Ingredient(weight=20, menu_id=menu2.id, product_id=product10.id)
    # ingredient13 = Ingredient(weight=1, menu_id=menu2.id, product_id=product11.id)
    #
    # custom1 = Custom(price=2550, time='2022-11-10 15:32:11',
    #                  address_id=address1.id, user_id=person1.id)
    # custom2 = Custom(price=999, time='2022-11-7 10:01:55',
    #                  address_id=address2.id, user_id=person3.id)
    # custom3 = Custom(price=1500, time='2022-10-20 10:01:00',
    #                  address_id=address2.id, user_id=person3.id)
    #
    # db.session.add_all([ingredient1, ingredient2, ingredient3, ingredient4, ingredient5,
    #                     ingredient6, ingredient7, ingredient8, ingredient9, ingredient10,
    #                     ingredient11, ingredient12, ingredient13])
    # db.session.add(custom1)
    # db.session.add(custom2)
    # db.session.add(custom3)
    # db.session.commit()
    #
    # details_1 = Details(quantity=2, custom_id=custom1.id, menu_id=menu2.id)
    # details2 = Details(quantity=1, custom_id=custom3.id, menu_id=menu3.id)
    # details3 = Details(quantity=3, custom_id=custom2.id, menu_id=menu1.id)
    #
    # db.session.add(details_1)
    # db.session.add(details2)
    # db.session.add(details3)
    # db.session.commit()

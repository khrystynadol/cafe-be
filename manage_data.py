from models import app, db, User, Product, Menu, Ingredient, details, Custom, Address

with app.app_context():
    user=User(u_name="Ivan",u_surname="Ivanov",u_phone="0934864659",
         u_email="user@gmail.com", u_password="rwwwwrwrrw", u_role="client")
    user2=User(u_name="Kate",u_surname="Lover",u_phone="0685222554",
         u_email="user2@gmail.com", u_password="iiiissijjx", u_role="manager")

    address=Address(a_street="Konyskogo",a_house="125а", a_flat=15)
    address2=Address(a_street="Franka",a_house="55", a_flat=2)

    product=Product(p_name="Coffee",p_price=255, p_weight=1000)
    product2=Product(p_name="Flour",p_price=100, p_weight=1000)

    menu=Menu(m_name="Late", m_price=56, m_availability=1, m_demand=0)
    menu2=Menu(m_name="Cupcake", m_price=99, m_availability=0, m_demand=0)

    db.session.add(user)
    db.session.add(user2)
    db.session.add(address)
    db.session.add(address2)
    db.session.add(product)
    db.session.add(product2)
    db.session.add(menu)
    db.session.add(menu2)
    db.session.commit()

    ingredient=Ingredient(i_weight=30,i_percent=50, Menu_id=menu.idMenu,Product_id=product.idProduct)
    ingredient2=Ingredient(i_weight=70,i_percent=15, Menu_id=menu1.idMenu,Product_id=product1.idProduct)

    custom=Custom(c_price=2550,Address_id=address.idAddress,User_id=user.idUser)
    custom2=Custom(c_price=999,Address_id=address1.idAddress,User_id=user1.idUser)
    custom3=Custom(c_price=1500,Address_id=address1.idAddress,User_id=user.idUser)

    db.session.add(ingredient)
    db.session.add(ingredient2)
    db.session.add(custom)
    db.session.add(custom2)
    db.session.add(custom3)
    db.session.commit()


    details=Details(d_quantity=4,Custom_id=custom.idCustom,Menu_id=menu2.idMenu)
    details2=Details(d_quantity=1,Custom_id=custom3.idCustom,Menu_id=menu2.idMenu)
    details3=Details(d_quantity=3,Custom_id=custom2.idCustom,Menu_id=menu.idMenu)

    db.session.add(details)
    db.session.add(details2)
    db.session.add(details3)
    db.session.commit()
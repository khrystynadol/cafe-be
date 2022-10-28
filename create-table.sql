CREATE TABLE `user` (
  `idUser` int NOT NULL,
  `u_name` varchar(45) NOT NULL,
  `u_surname` varchar(45) NOT NULL,
  `u_phone` int NOT NULL,
  `u_email` varchar(45) NOT NULL,
  `u_password` varchar(45) NOT NULL,
  `u_role` enum('client','manager') DEFAULT 'client',
  PRIMARY KEY (`idUser`),
  UNIQUE KEY `u_email_UNIQUE` (`u_email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3

CREATE TABLE `address` (
  `idAddress` int NOT NULL,
  `a_street` varchar(45) NOT NULL,
  `a_house` varchar(45) NOT NULL,
  `a_flat` int DEFAULT '0',
  PRIMARY KEY (`idAddress`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `order` (
  `idOrder` int NOT NULL,
  `o_price` int DEFAULT '0',
  `Address_id` int NOT NULL,
  `User_id` int NOT NULL,
  PRIMARY KEY (`idOrder`),
  KEY `fk_Order_Address1_idx` (`Address_id`),
  KEY `fk_Order_User1_idx` (`User_id`),
  CONSTRAINT `fk_Order_Address1` FOREIGN KEY (`Address_id`) REFERENCES `address` (`idAddress`),
  CONSTRAINT `fk_Order_User1` FOREIGN KEY (`User_id`) REFERENCES `user` (`idUser`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `menu` (
  `idMenu` int NOT NULL,
  `m_name` varchar(45) DEFAULT NULL,
  `m_price` int DEFAULT '0',
  `m_availability` tinyint DEFAULT '0',
  `m_demand` tinyint DEFAULT '0',
  PRIMARY KEY (`idMenu`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `product` (
  `idProduct` int NOT NULL,
  `p_name` varchar(45) DEFAULT NULL,
  `p_price` int DEFAULT NULL,
  `p_weight` int DEFAULT NULL,
  PRIMARY KEY (`idProduct`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `ingredient` (###
  `idIngredient` int NOT NULL,
  `i_weight` int NOT NULL,
  `i_percent` int NOT NULL DEFAULT '20',
  `Menu_id` int NOT NULL,
  `Product_id` int NOT NULL,
  PRIMARY KEY (`idIngredient`),
  KEY `fk_Ingredient_Menu_idx` (`Menu_id`),
  KEY `fk_Ingredient_Product1_idx` (`Product_id`),
  CONSTRAINT `fk_Ingredient_Menu` FOREIGN KEY (`Menu_id`) REFERENCES `menu` (`idMenu`),
  CONSTRAINT `fk_Ingredient_Product1` FOREIGN KEY (`Product_id`) REFERENCES `product` (`idProduct`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `details` (
  `idDetails` int NOT NULL,
  `d_quantity` int DEFAULT '1',
  `Order_id` int NOT NULL,
  `Menu_id` int NOT NULL,
  PRIMARY KEY (`idDetails`),
  KEY `fk_Details_Order1_idx` (`Order_id`),
  KEY `fk_Details_Menu1_idx` (`Menu_id`),
  CONSTRAINT `fk_Details_Menu1` FOREIGN KEY (`Menu_id`) REFERENCES `menu` (`idMenu`),
  CONSTRAINT `fk_Details_Order1` FOREIGN KEY (`Order_id`) REFERENCES `order` (`idOrder`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
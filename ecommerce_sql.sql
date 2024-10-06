-- MySQL dump 10.13  Distrib 8.0.37, for Win64 (x86_64)
--
-- Host: localhost    Database: ecommerce
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cart`
--

DROP TABLE IF EXISTS `cart`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cart` (
  `cart_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `quantity` int DEFAULT '1',
  `added_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`cart_id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cart`
--

LOCK TABLES `cart` WRITE;
/*!40000 ALTER TABLE `cart` DISABLE KEYS */;
INSERT INTO `cart` VALUES (1,3,1,1,'2024-09-26 09:19:45'),(2,3,1,1,'2024-09-26 09:21:38'),(3,3,1,1,'2024-09-26 09:22:11');
/*!40000 ALTER TABLE `cart` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'watch','Watch Category'),(2,'shoes','Shoes Category'),(3,'clothes','Clothes Category');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `favourites`
--

DROP TABLE IF EXISTS `favourites`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `favourites` (
  `fav_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `pid` int DEFAULT NULL,
  `added_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`fav_id`),
  KEY `user_id` (`user_id`),
  KEY `pid` (`pid`),
  CONSTRAINT `favourites_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `favourites_ibfk_2` FOREIGN KEY (`pid`) REFERENCES `products` (`pid`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `favourites`
--

LOCK TABLES `favourites` WRITE;
/*!40000 ALTER TABLE `favourites` DISABLE KEYS */;
INSERT INTO `favourites` VALUES (4,3,1,'2024-09-26 09:19:41');
/*!40000 ALTER TABLE `favourites` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `order_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `total_amount` float(10,2) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `pid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text,
  `price` bigint NOT NULL,
  `stock_quantity` int NOT NULL,
  `category_id` int NOT NULL,
  `media` text,
  `date_added` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`pid`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (1,'Rolex','Vintage Rolex 1601 CUSTOM Olive Green Dial Men\'s Automatic Watch 1973',250000,25,1,'http://1.bp.blogspot.com/-9p0HfYYwaoo/TZSpWH8BdcI/AAAAAAAAC00/LPGaiWS2aP8/s1600/Rolex%2BWALLPAPER.jpg','2022-06-29 00:00:00'),(2,'Apple','Watch Series 9 GPS 41mm Aluminium Case with Midnight Sport Loop',675,30,1,'https://c4.wallpaperflare.com/wallpaper/298/13/143/watch-technology-apple-watch-wallpaper-preview.jpg','2022-06-29 00:00:00'),(3,'Noise','Noise ColorFit NAV Smart Watch with Built-in GPS and High Resolution Display (Stealth Black)',450,45,1,'https://images.hindustantimes.com/tech/img/2020/07/20/1600x900/Noise_smartwatch_1595249244671_1595249254804.png','2022-06-29 00:00:00'),(4,'Air Jordan 1 Mid','Step up your style with Air Jordan – combining iconic design with unmatched comfort for a bold, athletic look. Perfect for both the court and the street.',200,25,2,'https://static.nike.com/a/images/t_PDP_936_v1/f_auto,q_auto:eco,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/1b1785a7-b7b2-4b09-915f-257fd37b7653/AIR+JORDAN+1+MID.png','2022-06-29 00:00:00'),(5,'Nike Air Force 1 \'07','Classic style meets modern comfort with the Nike Air Force 1 \'07. Featuring premium materials and timeless design, it\'s a staple for everyday wear.',150,30,2,'https://static.nike.com/a/images/t_PDP_936_v1/f_auto,q_auto:eco/2032825b-7466-4b2b-9a80-4f36ca6e0092/WMNS+AIR+FORCE+1+%2707.png','2022-06-29 00:00:00'),(6,'Nike Waffle Nav','Experience vintage vibes with the Nike Waffle Nav, blending retro-inspired design with lightweight comfort. Perfect for casual wear with a timeless edge.',275,30,2,'https://static.nike.com/a/images/t_PDP_936_v1/f_auto,q_auto:eco/758293c6-ace1-4f1f-a8a9-639711885067/NIKE+WAFFLE+NAV.png','2022-06-29 00:00:00'),(7,'Lymio Men\'s Solid Regular Fit Shirt','Elevate your wardrobe with the Lymio Men\'s Solid Regular Fit Shirt, offering a sleek, versatile look. Perfect for both casual and formal occasions.',20,50,3,'https://m.media-amazon.com/images/I/61wyfIo5XvL._SY741_.jpg','2022-06-29 00:00:00'),(8,'Lymio Men\'s Solid Regular Fit Shirt(White)','Elevate your wardrobe with the Lymio Men\'s Solid Regular Fit Shirt, offering a sleek, versatile look. Perfect for both casual and formal occasions.',20,50,3,'https://m.media-amazon.com/images/I/61snvxo3CjL._SY550_.jpg','2022-06-29 00:00:00'),(9,'Lymio Men\'s Solid Regular Fit Shirt(Maroon)','Elevate your wardrobe with the Lymio Men\'s Solid Regular Fit Shirt, offering a sleek, versatile look. Perfect for both casual and formal occasions.',20,50,3,'https://m.media-amazon.com/images/I/61w5PO2JqxL._SY550_.jpg','2022-06-29 00:00:00'),(12,'Nike Lunar Roam','The Nike Lunar Roam shoe offers lightweight cushioning with a sleek, modern design, perfect for all-day comfort. Its durable sole and breathable upper make it ideal for both casual wear and light activity.',160,56,2,'https://static.nike.com/a/images/t_PDP_936_v1/f_auto,q_auto:eco/8a650128-e142-49db-9ce0-cdffa094ea3a/NIKE+LUNAR+ROAM.png','2024-09-21 09:34:10'),(13,'Lymio Men Regular Fit Casual Shirt','The Lymio Men\'s Regular Fit Casual Shirt combines style and comfort with its versatile design, suitable for everyday wear. Its soft fabric and relaxed fit offer a great blend of ease and fashion for any casual occasion.',10,50,3,'https://m.media-amazon.com/images/I/71kkSLQhcGL._SY741_.jpg','2024-09-21 09:43:19'),(14,'Jumpman MVP','Jumpman MVP Nike shoes blend iconic design elements from past Air Jordans to deliver a modern, stylish sneaker. With a lightweight, breathable upper and cushioned midsole for maximum comfort, these shoes are perfect for both casual wear and athletic performance. Step up your game with a sleek, sporty look that pays homage to the Jumpman legacy.',173,30,2,'https://static.nike.com/a/images/t_PDP_936_v1/f_auto,q_auto:eco,u_126ab356-44d8-4a06-89b4-fcdcc8df0245,c_scale,fl_relative,w_1.0,h_1.0,fl_layer_apply/8a9c6c3e-4bc5-4909-9709-3911bc78a347/JORDAN+MVP.png','2024-09-25 17:54:53');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `t_id` int NOT NULL AUTO_INCREMENT,
  `order_id` int DEFAULT NULL,
  `payment_method` varchar(255) DEFAULT NULL,
  `payment_status` varchar(255) DEFAULT NULL,
  `transaction_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `amount` float(10,2) DEFAULT NULL,
  PRIMARY KEY (`t_id`),
  KEY `order_id` (`order_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(255) DEFAULT NULL,
  `password` varchar(20) NOT NULL,
  `name` varchar(20) DEFAULT NULL,
  `mobile` bigint DEFAULT NULL,
  `joining_date` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'abc@gmail.com','123456','Abc',123456789,'2024-09-14 16:41:53'),(2,'xyz@gmail.com','789123','Xyz',456789123,'2024-09-14 16:42:47'),(3,'rahul.rs2863@gmail.com','123456','Rahul',7891234560,'2024-09-16 08:26:59'),(11,'rahulsangwan280603@gmail.com','smrs289867532','Rahul',9876543210,'2024-09-16 08:41:28'),(12,'admin@gmail.com','admin@123','Admin',9789765123,'2024-09-18 22:24:17');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-09-26 18:08:16

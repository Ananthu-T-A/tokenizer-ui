/*
SQLyog Community v13.1.6 (64 bit)
MySQL - 5.7.9 : Database - onlinebid
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`onlinebid` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `onlinebid`;

/*Table structure for table `auction` */

DROP TABLE IF EXISTS `auction`;

CREATE TABLE `auction` (
  `auction_id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` int(11) DEFAULT NULL,
  `start_time` varchar(20) DEFAULT NULL,
  `start_date` varchar(20) DEFAULT NULL,
  `start_amount` varchar(20) DEFAULT NULL,
  `auction_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`auction_id`)
) ENGINE=MyISAM AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `auction` */

insert  into `auction`(`auction_id`,`item_id`,`start_time`,`start_date`,`start_amount`,`auction_status`) values 
(7,1,'20:59','2023-01-09','1200','start'),
(8,2,'21:00','2023-01-09','1500','start');

/*Table structure for table `bid` */

DROP TABLE IF EXISTS `bid`;

CREATE TABLE `bid` (
  `bid_id` int(11) NOT NULL AUTO_INCREMENT,
  `auction_id` int(11) DEFAULT NULL,
  `bidder_id` int(11) DEFAULT NULL,
  `date_time` varchar(20) DEFAULT NULL,
  `bid_amount` varchar(20) DEFAULT NULL,
  `bid_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`bid_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;

/*Data for the table `bid` */

insert  into `bid`(`bid_id`,`auction_id`,`bidder_id`,`date_time`,`bid_amount`,`bid_status`) values 
(4,7,1,'12-12-2023','1250','bid'),
(3,7,2,'12-12-2023','1350','bid'),
(8,7,1,'2023-01-03 12:44:31','1500','winner'),
(7,7,1,'2023-01-03 12:44:23','1351','bid'),
(9,7,1,'2023-01-03 14:06:49','4000','bid');

/*Table structure for table `card` */

DROP TABLE IF EXISTS `card`;

CREATE TABLE `card` (
  `card_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `card_no` varchar(20) DEFAULT NULL,
  `card_name` varchar(20) DEFAULT NULL,
  `exp_date` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`card_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `card` */

insert  into `card`(`card_id`,`user_id`,`card_no`,`card_name`,`exp_date`) values 
(1,1,'576876467446768','amal','12/2023');

/*Table structure for table `category` */

DROP TABLE IF EXISTS `category`;

CREATE TABLE `category` (
  `cat_id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_name` varchar(20) DEFAULT NULL,
  `cat_desc` varchar(20) DEFAULT NULL,
  `cat_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`cat_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Data for the table `category` */

insert  into `category`(`cat_id`,`cat_name`,`cat_desc`,`cat_status`) values 
(10,'Happy','Hello','active'),
(5,'antique','before 90s','active'),
(6,'kkk','kkkk','active'),
(9,'sad','asd','active');

/*Table structure for table `courier` */

DROP TABLE IF EXISTS `courier`;

CREATE TABLE `courier` (
  `courier_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `cour_name` varchar(20) DEFAULT NULL,
  `cour_phone` varchar(20) DEFAULT NULL,
  `cour_address` varchar(20) DEFAULT NULL,
  `cour_district` varchar(20) DEFAULT NULL,
  `cour_state` varchar(20) DEFAULT NULL,
  `cour_pin` varchar(20) DEFAULT NULL,
  `cour_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`courier_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `courier` */

insert  into `courier`(`courier_id`,`username`,`cour_name`,`cour_phone`,`cour_address`,`cour_district`,`cour_state`,`cour_pin`,`cour_status`) values 
(2,'dtdc','dtdc','9874563210','dtdckochi','eranakulam','kerala','68754','active'),
(3,'mail','dafs','7895461230','sdfasf','sdafsdf','sdfaf','555555','active');

/*Table structure for table `delivery` */

DROP TABLE IF EXISTS `delivery`;

CREATE TABLE `delivery` (
  `delivery_id` int(11) NOT NULL AUTO_INCREMENT,
  `bid_id` int(11) DEFAULT NULL,
  `courier_id` int(11) DEFAULT NULL,
  `delivery_date` varchar(20) DEFAULT NULL,
  `delivery_time` varchar(20) DEFAULT NULL,
  `delivery_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`delivery_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `delivery` */

insert  into `delivery`(`delivery_id`,`bid_id`,`courier_id`,`delivery_date`,`delivery_time`,`delivery_status`) values 
(1,3,2,'2023-01-12','00:22','Delivered');

/*Table structure for table `item` */

DROP TABLE IF EXISTS `item`;

CREATE TABLE `item` (
  `item_id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_id` int(11) DEFAULT NULL,
  `subcat_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `item_name` varchar(20) DEFAULT NULL,
  `item_desc` varchar(20) DEFAULT NULL,
  `item_image` varchar(1000) DEFAULT NULL,
  `item_amount` varchar(20) DEFAULT NULL,
  `item_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`item_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `item` */

insert  into `item`(`item_id`,`cat_id`,`subcat_id`,`user_id`,`item_name`,`item_desc`,`item_image`,`item_amount`,`item_status`) values 
(1,5,1,1,'jsfdkuf','dsflskjdfb','static/0115eaf9-4f94-43e2-89d2-2e43facac59ed226e5099a6f2e10003580e38ca87c4e.jpg','1200','Added to auction'),
(2,10,1,2,'dfedfa','dasd','static/2c417e61-eb52-4a19-ad46-8be68590639fFeatured-Image-Best-4K-Wallpapers-Windows.jpg','1200','active');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) DEFAULT NULL,
  `user_type` varchar(20) DEFAULT NULL,
  `login_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`username`,`password`,`user_type`,`login_status`) values 
('admin','admin','admin','active'),
('dtdc','dtdc','courier','active'),
('mail','mail','courier','active'),
('user','user','user','active'),
('hari','hari','user','active');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `card_id` int(11) DEFAULT NULL,
  `bid_id` int(11) DEFAULT NULL,
  `payment_date` varchar(20) DEFAULT NULL,
  `payment_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `payment` */

insert  into `payment`(`payment_id`,`card_id`,`bid_id`,`payment_date`,`payment_status`) values 
(1,1,3,'42568464','paid');

/*Table structure for table `subcategory` */

DROP TABLE IF EXISTS `subcategory`;

CREATE TABLE `subcategory` (
  `subcat_id` int(11) NOT NULL AUTO_INCREMENT,
  `subcat_name` varchar(20) DEFAULT NULL,
  `subcat_desc` varchar(20) DEFAULT NULL,
  `subcat_status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`subcat_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `subcategory` */

insert  into `subcategory`(`subcat_id`,`subcat_name`,`subcat_desc`,`subcat_status`) values 
(1,'sa','aserw','active'),
(2,'scrap','dfsd','active');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(20) DEFAULT NULL,
  `u_fname` varchar(20) DEFAULT NULL,
  `u_lname` varchar(20) DEFAULT NULL,
  `u_gender` varchar(20) DEFAULT NULL,
  `u_dob` varchar(20) DEFAULT NULL,
  `u_phone` varchar(20) DEFAULT NULL,
  `u_houseno` varchar(20) DEFAULT NULL,
  `u_street` varchar(20) DEFAULT NULL,
  `u_district` varchar(20) DEFAULT NULL,
  `u_state` varchar(20) DEFAULT NULL,
  `u_pin` varchar(20) DEFAULT NULL,
  `u_date` varchar(20) DEFAULT NULL,
  `u_stastus` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`username`,`u_fname`,`u_lname`,`u_gender`,`u_dob`,`u_phone`,`u_houseno`,`u_street`,`u_district`,`u_state`,`u_pin`,`u_date`,`u_stastus`) values 
(1,'user','amal','amal','male','12/12/2001','7894561230','amalnivas','11th street','eranakulam','kerala','788455`','12/12/2022','active'),
(2,'hari','haari','krisnan','on','2023-01-31','9874563210','h34','32nd street','eranakulam','kerala','687546','2023-01-02','active');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

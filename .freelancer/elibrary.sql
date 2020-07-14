/*
SQLyog Community v12.4.3 (64 bit)
MySQL - 5.5.62-0ubuntu0.14.04.1 : Database - elibrary
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`elibrary` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `elibrary`;

/*Table structure for table `faculty` */

DROP TABLE IF EXISTS `faculty`;

CREATE TABLE `faculty` (
  `id` int(5) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) DEFAULT NULL,
  `userId` varchar(20) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `faculty` */

insert  into `faculty`(`id`,`name`,`userId`,`password`) values 
(1,'Amit','amit','amit');

/*Table structure for table `uploadVideos` */

DROP TABLE IF EXISTS `uploadVideos`;

CREATE TABLE `uploadVideos` (
  `id` int(7) NOT NULL AUTO_INCREMENT,
  `subjectId` int(2) DEFAULT NULL,
  `facultyId` int(5) DEFAULT NULL,
  `unit` int(1) DEFAULT NULL COMMENT 'fixed unit 1 to 4',
  `videoUrl` varchar(255) DEFAULT NULL,
  `status` int(1) DEFAULT '1' COMMENT '1->New Upload, 2->english conversion,3->approved,4->declain',
  `englishSubTitleUrl` varchar(255) DEFAULT NULL,
  `created` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

/*Data for the table `uploadVideos` */

insert  into `uploadVideos`(`id`,`subjectId`,`facultyId`,`unit`,`videoUrl`,`status`,`englishSubTitleUrl`,`created`) values 
(4,5,1,1,'/home/skd/Work/bot-python-transcribe/.freelancer/good.mp4',1,NULL,'2020-07-11 18:51:58');

/*Table structure for table `videoSubject` */

DROP TABLE IF EXISTS `videoSubject`;

CREATE TABLE `videoSubject` (
  `id` int(2) NOT NULL AUTO_INCREMENT,
  `name` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

/*Data for the table `videoSubject` */

insert  into `videoSubject`(`id`,`name`) values 
(1,'Principles & Practices of Management'),
(2,'Human Resource Management'),
(3,'Marketing Management'),
(4,'Financial Management'),
(5,'Computer Application & Management'),
(6,'Managerial Economics'),
(7,'Organizational Behaviour'),
(8,'Business Coomunciation'),
(9,'Operations Research'),
(10,'Business Environment'),
(11,'Legal Environmental & Business Law'),
(12,'Production & Operation Management'),
(13,'Suppply Chain Management'),
(14,'Management Information System');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

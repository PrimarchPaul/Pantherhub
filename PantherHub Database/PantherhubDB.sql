-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: pantherhub
-- ------------------------------------------------------
-- Server version	8.0.36

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `coach`
--

DROP TABLE IF EXISTS `coach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coach` (
  `coachID` int NOT NULL,
  `coachName` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `coachFName` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `coachLName` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `coachPassword` varchar(128) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `coachEmail` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `coachRate` int DEFAULT NULL,
  PRIMARY KEY (`coachID`),
  KEY `coachID` (`coachID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coach`
--

LOCK TABLES `coach` WRITE;
/*!40000 ALTER TABLE `coach` DISABLE KEYS */;
/*!40000 ALTER TABLE `coach` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coachroster`
--

DROP TABLE IF EXISTS `coachroster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coachroster` (
  `coachID` int DEFAULT NULL,
  `userName` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `startDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `endDate` timestamp NULL DEFAULT NULL,
  KEY `coachID` (`coachID`),
  CONSTRAINT `coachroster_ibfk_1` FOREIGN KEY (`coachID`) REFERENCES `coach` (`coachID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coachroster`
--

LOCK TABLES `coachroster` WRITE;
/*!40000 ALTER TABLE `coachroster` DISABLE KEYS */;
/*!40000 ALTER TABLE `coachroster` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `coachtransactions`
--

DROP TABLE IF EXISTS `coachtransactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `coachtransactions` (
  `coachID` int DEFAULT NULL,
  `userID` int DEFAULT NULL,
  `cardNumber` int DEFAULT NULL,
  `userTransaction` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `transactionAmount` int DEFAULT NULL,
  KEY `coachID` (`coachID`),
  KEY `userID` (`userID`),
  CONSTRAINT `coachtransactions_ibfk_1` FOREIGN KEY (`coachID`) REFERENCES `coach` (`coachID`),
  CONSTRAINT `coachtransactions_ibfk_2` FOREIGN KEY (`userID`) REFERENCES `useraccount` (`userID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `coachtransactions`
--

LOCK TABLES `coachtransactions` WRITE;
/*!40000 ALTER TABLE `coachtransactions` DISABLE KEYS */;
/*!40000 ALTER TABLE `coachtransactions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `useraccount`
--

DROP TABLE IF EXISTS `useraccount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `useraccount` (
  `userid` int NOT NULL AUTO_INCREMENT,
  `userName` varchar(32) COLLATE utf8mb4_general_ci NOT NULL,
  `userFName` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `userLName` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `userEmail` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `userPreference` varchar(40) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `userGender` varchar(40) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `userCoach` int DEFAULT NULL,
  `userPID` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `userPhoneNumber` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `userZip` int DEFAULT NULL,
  `userState` varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `userDOB` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `userBio` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`userEmail`,`userName`),
  UNIQUE KEY `idx_username` (`userName`),
  UNIQUE KEY `idx_useremail` (`userEmail`),
  KEY `userID` (`userid`),
  KEY `userEmail` (`userEmail`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `useraccount`
--

LOCK TABLES `useraccount` WRITE;
/*!40000 ALTER TABLE `useraccount` DISABLE KEYS */;
INSERT INTO `useraccount` VALUES (10,'melatoninsniffer','paul','reyes','paulreyes44@gmail.com','straight','male',NULL,'1234567','1234567890',33028,'FL','2000-10-13',NULL),(11,'codingsniffer','paul','john','reyespaul56@gmail.com','straight','male',NULL,'6220746','1234567890',12345,'AL','2000-10-13','Wassup !!'),(4,'creatinesniffer','paul','reyes','testing@test.com','straight','male',NULL,NULL,NULL,12345,'AL','2000-10-13',NULL),(8,'testing','p','j','testing@testing.com','straight','male',NULL,'6220746','1234567890',12345,'AL','2000-10-13',NULL),(9,'testingtest','paul','john','testingtest@testing.com','bisexual','Male',NULL,'1234567','1234567890',12345,'FL','2000-10-13','I am looking for sexy ass girls in my area');
/*!40000 ALTER TABLE `useraccount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usercardinfo`
--

DROP TABLE IF EXISTS `usercardinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usercardinfo` (
  `userID` int DEFAULT NULL,
  `cardName` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `cardNumber` int DEFAULT NULL,
  `cardCVV` int DEFAULT NULL,
  `cardPin` int DEFAULT NULL,
  `cardDate` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  KEY `userID` (`userID`),
  CONSTRAINT `usercardinfo_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `useraccount` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usercardinfo`
--

LOCK TABLES `usercardinfo` WRITE;
/*!40000 ALTER TABLE `usercardinfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `usercardinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userchatlogs`
--

DROP TABLE IF EXISTS `userchatlogs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userchatlogs` (
  `userID` int DEFAULT NULL,
  `userFriend` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `userMessageTo` varchar(500) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `messageSent` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  KEY `userID` (`userID`),
  CONSTRAINT `userchatlogs_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `useraccount` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userchatlogs`
--

LOCK TABLES `userchatlogs` WRITE;
/*!40000 ALTER TABLE `userchatlogs` DISABLE KEYS */;
/*!40000 ALTER TABLE `userchatlogs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userlogin`
--

DROP TABLE IF EXISTS `userlogin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userlogin` (
  `userID` int NOT NULL AUTO_INCREMENT,
  `userEmail` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `userPassword` varchar(256) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `userName` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`userID`),
  KEY `userEmail` (`userEmail`),
  CONSTRAINT `userlogin_ibfk_1` FOREIGN KEY (`userEmail`) REFERENCES `useraccount` (`userEmail`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userlogin`
--

LOCK TABLES `userlogin` WRITE;
/*!40000 ALTER TABLE `userlogin` DISABLE KEYS */;
INSERT INTO `userlogin` VALUES (3,'testing@test.com','Dd06220746!@','creatinesniffer'),(7,'testing@testing.com','scrypt:32768:8:1$wYXSuxKg08SFkVOU$adba727b11a667d7068e126a92f0fb757faabe706a6e9b61a9191aea539652cb16d438d5167c77063e82ac21455eef6c73fff4982d9ded45524493c1573d8ee6','testing'),(8,'testingtest@testing.com','scrypt:32768:8:1$1aDg3mckUoQRDGUy$df01ecb73562916434ea9114dce86a6ffc4f4983c0f8f0c8fb9b823b529da31f35c2f6d9aa2045c236b7fa26654eb03b0a888651bc2af819e1999e15217f51e0','testingtest'),(9,'paulreyes44@gmail.com','scrypt:32768:8:1$EjmznEpAPXXe7gIR$1faae92853ee96c45a260139f85ac18a0f1d88057c8566a763e55a42d06537de40b2e707ede0794a8ea2033fae7c8d49737d8b07759097aeb70a7d5c0da95e0a','melatoninsniffer'),(10,'reyespaul56@gmail.com','scrypt:32768:8:1$xgpQPSBXm1AvRUtX$f3fcaff171228a3435ea2eabbd37d46072d308dfe40fd7335dce0dacb52a8e83c556b145eeb0846cdb95406c13cfa92c205e0b05c69fd9b94a277741a0e92d9a','codingsniffer');
/*!40000 ALTER TABLE `userlogin` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usermatch`
--

DROP TABLE IF EXISTS `usermatch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usermatch` (
  `userName` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `user1Name` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `userinterest` tinyint(1) DEFAULT NULL,
  KEY `userName` (`userName`),
  KEY `user1Name` (`user1Name`),
  CONSTRAINT `usermatch_ibfk_1` FOREIGN KEY (`userName`) REFERENCES `useraccount` (`userName`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `usermatch_ibfk_2` FOREIGN KEY (`user1Name`) REFERENCES `useraccount` (`userName`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usermatch`
--

LOCK TABLES `usermatch` WRITE;
/*!40000 ALTER TABLE `usermatch` DISABLE KEYS */;
INSERT INTO `usermatch` VALUES ('codingsniffer','testing',1),('codingsniffer','testingtest',1),('codingsniffer','creatinesniffer',1),('codingsniffer','melatoninsniffer',1),('codingsniffer','melatoninsniffer',1),('codingsniffer','melatoninsniffer',1),('codingsniffer','melatoninsniffer',1),('codingsniffer','melatoninsniffer',1),('codingsniffer','testing',1),('codingsniffer','testing',1);
/*!40000 ALTER TABLE `usermatch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `userphoto`
--

DROP TABLE IF EXISTS `userphoto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `userphoto` (
  `userName` varchar(32) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `PhotoDirectory` varchar(1024) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `uploadDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `userphoto`
--

LOCK TABLES `userphoto` WRITE;
/*!40000 ALTER TABLE `userphoto` DISABLE KEYS */;
INSERT INTO `userphoto` VALUES ('codingsniffer','pantherPNG.png','2024-04-08 06:19:15'),('testingtest','pantherPNG.png','2024-04-08 06:20:19');
/*!40000 ALTER TABLE `userphoto` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-04-08 22:26:04

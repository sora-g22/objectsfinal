SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';
CREATE SCHEMA IF NOT EXISTS `piratenetDB` DEFAULT CHARACTER SET utf8 ;
USE `piratenetDB` ;
CREATE TABLE IF NOT EXISTS `piratenetDB`.`users` (
  `UUID` CHAR(36) BINARY NOT NULL,
  `username` VARCHAR(45) NOT NULL,
  `password` LONGTEXT NOT NULL,
  `salt` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`UUID`))
ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `piratenetDB`.`students` (
  `users_UUID` CHAR(36) BINARY NOT NULL,
  `firstName` VARCHAR(45) NOT NULL,
  `lastName` VARCHAR(45) NOT NULL,
  `enrollmentStatus` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`users_UUID`),
  INDEX `fk_students_users1_idx` (`users_UUID` ASC) VISIBLE,
  CONSTRAINT `fk_students_users1`
    FOREIGN KEY (`users_UUID`)
    REFERENCES `piratenetDB`.`users` (`UUID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `piratenetDB`.`admins` (
  `users_UUID` CHAR(36) BINARY NOT NULL,
  `firstName` VARCHAR(45) NOT NULL,
  `lastName` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`users_UUID`),
  INDEX `fk_admins_users1_idx` (`users_UUID` ASC) VISIBLE,
  CONSTRAINT `fk_admins_users1`
    FOREIGN KEY (`users_UUID`)
    REFERENCES `piratenetDB`.`users` (`UUID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `piratenetDB`.`professors` (
  `UUID` CHAR(36) BINARY NOT NULL,
  `firstName` VARCHAR(45) NOT NULL,
  `lastName` VARCHAR(45) NOT NULL,
  `contactInfo` VARCHAR(45) NULL,
  PRIMARY KEY (`UUID`),
  INDEX `fk_professors_users1_idx` (`UUID` ASC) VISIBLE,
  CONSTRAINT `fk_professors_users1`
    FOREIGN KEY (`UUID`)
    REFERENCES `piratenetDB`.`users` (`UUID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `piratenetDB`.`courses` (
  `courseID` VARCHAR(45) NOT NULL,
  `professors_users_UUID` CHAR(36) BINARY NOT NULL,
  `meetingTime` VARCHAR(45) NULL DEFAULT NULL,
  `meetingDays` VARCHAR(45) NULL DEFAULT NULL,
  PRIMARY KEY (`courseID`, `professors_users_UUID`),
  INDEX `fk_courses_professors1_idx` (`professors_users_UUID` ASC) VISIBLE,
  INDEX `fk_courses_professors1` (`professors_users_UUID` ASC) VISIBLE,
  CONSTRAINT `fk_courses_professors1`
    FOREIGN KEY (`professors_users_UUID`)
    REFERENCES `piratenetDB`.`professors` (`UUID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `piratenetDB`.`roles` (
  `roleID` VARCHAR(45) NOT NULL,
  `users_UUID` CHAR(36) BINARY NOT NULL,
  PRIMARY KEY (`roleID`),
  INDEX `fk_roles_users1_idx` (`users_UUID` ASC) VISIBLE,
  INDEX `fk_roles_users1` (`users_UUID` ASC) VISIBLE,
  CONSTRAINT `fk_roles_users1`
    FOREIGN KEY (`users_UUID`)
    REFERENCES `piratenetDB`.`users` (`UUID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `piratenetDB`.`permissions` (
  `permissionID` INT NOT NULL,
  `permissions` VARCHAR(45) NULL DEFAULT NULL,
  `roles_roleID` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`permissionID`, `roles_roleID`),
  INDEX `fk_permissions_roles1_idx` (`roles_roleID` ASC) VISIBLE,
  INDEX `fk_permissions_roles1` (`roles_roleID` ASC) VISIBLE,
  CONSTRAINT `fk_permissions_roles1`
    FOREIGN KEY (`roles_roleID`)
    REFERENCES `piratenetDB`.`roles` (`roleID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `piratenetDB`.`grades` (
  `courseID` VARCHAR(45) NOT NULL,
  `students_users_UUID` CHAR(36) BINARY NOT NULL,
  `professors_users_UUID` CHAR(36) BINARY NOT NULL,
  `percentageGrade` DOUBLE(5,2) NULL,
  PRIMARY KEY (`courseID`, `students_users_UUID`, `professors_users_UUID`),
  INDEX `fk_grades_courses1_idx` (`courseID` ASC, `professors_users_UUID` ASC) VISIBLE,
  CONSTRAINT `fk_grades_students1`
    FOREIGN KEY (`students_users_UUID`)
    REFERENCES `piratenetDB`.`students` (`users_UUID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_grades_courses1`
    FOREIGN KEY (`courseID` , `professors_users_UUID`)
    REFERENCES `piratenetDB`.`courses` (`courseID` , `professors_users_UUID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
CREATE TABLE IF NOT EXISTS `piratenetDB`.`courses_has_students` (
  `courseID` VARCHAR(45) NOT NULL,
  `professors_users_UUID` CHAR(36) BINARY NOT NULL,
  `students_users_UUID` CHAR(36) BINARY NOT NULL,
  PRIMARY KEY (`courseID`, `professors_users_UUID`, `students_users_UUID`),
  INDEX `fk_courses_has_students_students1_idx` (`students_users_UUID` ASC) VISIBLE,
  INDEX `fk_courses_has_students_courses1_idx` (`courseID` ASC, `professors_users_UUID` ASC) VISIBLE,
  CONSTRAINT `fk_courses_has_students_courses1`
    FOREIGN KEY (`courseID` , `professors_users_UUID`)
    REFERENCES `piratenetDB`.`courses` (`courseID` , `professors_users_UUID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_courses_has_students_students1`
    FOREIGN KEY (`students_users_UUID`)
    REFERENCES `piratenetDB`.`students` (`users_UUID`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

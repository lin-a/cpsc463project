-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`dealers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`dealers` (
  `dealer_id` INT NOT NULL AUTO_INCREMENT,
  `dealer_name` VARCHAR(45) NOT NULL,
  `dealer_space` INT NOT NULL,
  `dealer_password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`dealer_id`),
  UNIQUE INDEX `dealer_name_UNIQUE` (`dealer_name` ASC) VISIBLE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`cars`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`cars` (
  `cars_id` INT NOT NULL AUTO_INCREMENT,
  `car_model` VARCHAR(45) NOT NULL,
  `cars_variant` VARCHAR(45) NOT NULL,
  `dealer_dealer_id` INT NOT NULL,
  PRIMARY KEY (`cars_id`),
  INDEX `fk_cars_dealer_idx` (`dealer_dealer_id` ASC) VISIBLE,
  CONSTRAINT `fk_cars_dealer`
    FOREIGN KEY (`dealer_dealer_id`)
    REFERENCES `mydb`.`dealers` (`dealer_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`car`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`car` (
  `car_id` INT NOT NULL,
  `car_model` VARCHAR(45) NULL,
  `car_variant` VARCHAR(45) NULL,
  PRIMARY KEY (`car_id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

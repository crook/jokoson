-- MySQL Script generated by MySQL Workbench
-- Thu Oct 27 22:19:17 2016
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema jksndb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema jksndb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `jksndb` DEFAULT CHARACTER SET utf8 ;
USE `jksndb` ;

-- -----------------------------------------------------
-- Table `jksndb`.`company`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `jksndb`.`company` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `Address1` VARCHAR(45) NULL,
  `Address2` VARCHAR(45) NULL,
  `cell_phone` VARCHAR(45) NULL,
  `office_phone` VARCHAR(45) NULL,
  `City` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `jksndb`.`role`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `jksndb`.`role` (
  `id` INT NOT NULL,
  `role` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `jksndb`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `jksndb`.`user` (
  `username` (16) NOT NULL,
  `email` (255) NULL,
  `password` (32) NOT NULL,
  `create_time`  NULL DEFAULT CURRENT_TIMESTAMP,
  `id` INT NOT NULL,
  `wechat_id` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `id`
    FOREIGN KEY ()
    REFERENCES `jksndb`.`company` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id`
    FOREIGN KEY ()
    REFERENCES `jksndb`.`role` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);


-- -----------------------------------------------------
-- Table `jksndb`.`vendor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `jksndb`.`vendor` (
  `id` INT NOT NULL,
  `name` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `cell_phone` VARCHAR(45) NULL,
  `office_phone` VARCHAR(45) NULL,
  `address1` VARCHAR(45) NULL,
  `address2` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `jksndb`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `jksndb`.`category` (
  `id` INT NOT NULL,
  `discription` VARCHAR(45) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `jksndb`.`equip`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `jksndb`.`equip` (
  `id` INT NOT NULL,
  `model` VARCHAR(45) NULL,
  `sn` VARCHAR(45) NULL,
  `discription` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `id`
    FOREIGN KEY ()
    REFERENCES `jksndb`.`vendor` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id`
    FOREIGN KEY ()
    REFERENCES `jksndb`.`category` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `jksndb`.`order`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `jksndb`.`order` (
  `id` INT NOT NULL,
  `signtime` DATETIME NULL,
  `starttime` DATETIME NULL,
  `endtime` DATETIME NULL,
  `duration` INT NULL,
  `money` INT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `companyid`
    FOREIGN KEY ()
    REFERENCES `jksndb`.`user` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `equipid`
    FOREIGN KEY ()
    REFERENCES `jksndb`.`equip` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `jksndb`.`gpssensor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `jksndb`.`gpssensor` (
  `id` INT NOT NULL,
  `status` INT NULL,
  `batterypercent` INT NULL,
  `model` VARCHAR(45) NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `id`
    FOREIGN KEY ()
    REFERENCES `jksndb`.`equip` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id`
    FOREIGN KEY ()
    REFERENCES `jksndb`.`vendor` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id`
    FOREIGN KEY ()
    REFERENCES `jksndb`.`category` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `jksndb`.`gpsdata`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `jksndb`.`gpsdata` (
  `id` INT NOT NULL,
  `time` DATETIME NULL,
  `x` FLOAT NULL,
  `y` FLOAT NULL,
  `hight` FLOAT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `gpssensorid`
    FOREIGN KEY ()
    REFERENCES `jksndb`.`gpssensor` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `jksndb`.`admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `jksndb`.`admin` (
  `username` (16) NOT NULL,
  `email` (255) NULL,
  `password` (32) NOT NULL,
  `create_time`  NULL DEFAULT CURRENT_TIMESTAMP,
  `id` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`));


-- -----------------------------------------------------
-- Table `jksndb`.`order_hist`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `jksndb`.`order_hist` (
  `id` INT NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `id`
    FOREIGN KEY ()
    REFERENCES `jksndb`.`order` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `id`
    FOREIGN KEY ()
    REFERENCES `jksndb`.`equip` ()
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

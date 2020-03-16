
DROP TABLE IF EXISTS `general_logs`;
DROP TABLE IF EXISTS `request_log`;
DROP TABLE IF EXISTS `rubic_template`;
DROP TABLE IF EXISTS `rubic`;
DROP TABLE IF EXISTS `challenge_user`;
DROP TABLE IF EXISTS `challenge_template`;

DROP TABLE IF EXISTS `challenge`;
DROP TABLE IF EXISTS `deadline`;
DROP TABLE IF EXISTS `category`;

DROP TABLE IF EXISTS `classmate`;
DROP TABLE IF EXISTS `classroom`;
DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `country`;
DROP TABLE IF EXISTS `permission`;
DROP TABLE IF EXISTS `rol`;
DROP TABLE IF EXISTS `permission_type`;



CREATE TABLE `permission_type` (
  `permission` varchar(300) NOT NULL,
  PRIMARY KEY(permission)
)  ENGINE=InnoDB;

INSERT INTO `permission_type` (`permission`) VALUES ('Create_class');
INSERT INTO `permission_type` (`permission`) VALUES ('Read_class');
INSERT INTO `permission_type` (`permission`) VALUES ('Update_class');
INSERT INTO `permission_type` (`permission`) VALUES ('Delete_class');

INSERT INTO `permission_type` (`permission`) VALUES ('Create_rubic');
INSERT INTO `permission_type` (`permission`) VALUES ('Read_rubic');
INSERT INTO `permission_type` (`permission`) VALUES ('Update_rubic');
INSERT INTO `permission_type` (`permission`) VALUES ('Delete_rubic');

INSERT INTO `permission_type` (`permission`) VALUES ('Create_challenge');
INSERT INTO `permission_type` (`permission`) VALUES ('Read_challenge');
INSERT INTO `permission_type` (`permission`) VALUES ('Update_challenge');
INSERT INTO `permission_type` (`permission`) VALUES ('Delete_challenge');

CREATE TABLE `rol` (
  `rol_name` varchar(100) NOT NULL,
  `description_rol` varchar(1000) NOT NULL,
  PRIMARY KEY(rol_name)
)  ENGINE=InnoDB;

INSERT INTO `rol` (`rol_name`,`description_rol`) VALUES
('Student','Esto es una descripcion de estudiante');
INSERT INTO `rol` (`rol_name`,`description_rol`) VALUES
('Professor','Esto es una descripcion de un profesor');
INSERT INTO `rol` (`rol_name`,`description_rol`) VALUES
('anonym','Esto es una descripcion de un anonimo');
INSERT INTO `rol` (`rol_name`,`description_rol`) VALUES
('administrador','Esto es una descripcion de un administrador');

CREATE TABLE `permission` (
  `value` varchar(400) NOT NULL , 
  `FK_PERMISSION_TYPE_permission` varchar(300) NOT NULL ,
  `FK_ROL_rol_name` varchar(100) NOT NULL , 
  FOREIGN KEY (`FK_PERMISSION_TYPE_permission`) REFERENCES permission_type(permission),
  FOREIGN KEY (`FK_ROL_rol_name`) REFERENCES rol(rol_name)
)  ENGINE=InnoDB;

INSERT INTO `permission` (`FK_PERMISSION_TYPE_permission`,`FK_ROL_rol_name`,`value`) VALUES ('Create_class','Professor','True');
INSERT INTO `permission` (`FK_PERMISSION_TYPE_permission`,`FK_ROL_rol_name`,`value`) VALUES ('Create_challenge','Professor','True');
INSERT INTO `permission` (`FK_PERMISSION_TYPE_permission`,`FK_ROL_rol_name`,`value`) VALUES ('Create_rubic','Professor','True');


INSERT INTO `permission` (`FK_PERMISSION_TYPE_permission`,`FK_ROL_rol_name`,`value`) VALUES ('Read_class','Professor','True');
INSERT INTO `permission` (`FK_PERMISSION_TYPE_permission`,`FK_ROL_rol_name`,`value`) VALUES ('Read_challenge','Professor','True');
INSERT INTO `permission` (`FK_PERMISSION_TYPE_permission`,`FK_ROL_rol_name`,`value`) VALUES ('Read_rubic','Professor','True');

INSERT INTO `permission` (`FK_PERMISSION_TYPE_permission`,`FK_ROL_rol_name`,`value`) VALUES ('Update_class','Professor','True');
INSERT INTO `permission` (`FK_PERMISSION_TYPE_permission`,`FK_ROL_rol_name`,`value`) VALUES ('Update_challenge','Professor','True');
INSERT INTO `permission` (`FK_PERMISSION_TYPE_permission`,`FK_ROL_rol_name`,`value`) VALUES ('Update_rubic','Professor','True');



CREATE TABLE `country` (
  `country` varchar(300) NOT NULL,
  PRIMARY KEY(country)
)  ENGINE=InnoDB;

INSERT INTO `country` (`country`) VALUES
('Chile');


CREATE TABLE `users` (
  `email` varchar(255) NOT NULL,
  `nickname` varchar(255) NOT NULL,
  `firstname` varchar(255),
  `lastname` varchar(255),
  `passw` varchar(100) NOT NULL,
  `salt` varchar(100) NOT NULL,
  `birthday_datetime` DATETIME, 
  `FK_COUNTRY_country` varchar(300) NOT NULL,
  `FK_ROL_rol_name` varchar(100) NOT NULL,
  PRIMARY KEY(email),
  FOREIGN KEY (`FK_COUNTRY_country`) REFERENCES country(country),
  FOREIGN KEY (`FK_ROL_rol_name`) REFERENCES rol(rol_name),
  UNIQUE(nickname)
)  ENGINE=InnoDB;

INSERT INTO `users` (`nickname`, `passw`, `salt`, `email`, `firstname`, `FK_COUNTRY_country`, `FK_ROL_rol_name`) VALUES
('profesor1', '924c3e107882ec413a5d52c84d3763d828f58cf11359a596d6739567f9d4ba7c', '$2b$12$awABuYqShBoaOlOGfYofBe', 'profesor1@test.com','nombre usuario1','Chile','Professor');
INSERT INTO `users` (`nickname`, `passw`, `salt`, `email`, `firstname`, `FK_COUNTRY_country`, `FK_ROL_rol_name`) VALUES
('estudiante1', '924c3e107882ec413a5d52c84d3763d828f58cf11359a596d6739567f9d4ba7c', '$2b$12$awABuYqShBoaOlOGfYofBe', 'estudiante1@test.com','nombre usuario1','Chile','Student');


CREATE TABLE `classroom` (
  `id_number` INT NOT NULL AUTO_INCREMENT,
  `classroom_name` varchar(255) NOT NULL,
  `FK_USERS_email` varchar(255) NOT NULL,
  FOREIGN KEY (`FK_USERS_email`) REFERENCES users(email),
  PRIMARY KEY (`id_number`)
)  ENGINE=InnoDB;

CREATE TABLE `classmate` (
  `id_number` INT NOT NULL AUTO_INCREMENT,
  `FK_CLASSROOM_id_number` INT NOT NULL,
  `FK_USERS_email` varchar(255) NOT NULL,
  FOREIGN KEY (`FK_CLASSROOM_id_number`) REFERENCES classroom(id_number),
  FOREIGN KEY (`FK_USERS_email`) REFERENCES users(email),
  PRIMARY KEY (`id_number`)
)  ENGINE=InnoDB;


CREATE TABLE `category` (
  `category_name` varchar(300) NOT NULL,
  `description` TEXT NOT NULL,
  PRIMARY KEY (`category_name`)
)  ENGINE=InnoDB;

INSERT INTO `category` (`category_name`,`description`) VALUES ('general','cat de prueba 1');
INSERT INTO `category` (`category_name`,`description`) VALUES ('general2','cat de prueba 2');

CREATE TABLE `deadline` (
  `type` varchar(200) NOT NULL,
  PRIMARY KEY (`type`)
)  ENGINE=InnoDB;

INSERT INTO `deadline` (`type`) VALUES ('minutes');
INSERT INTO `deadline` (`type`) VALUES ('timestamp');

CREATE TABLE `challenge` (
  `id_number` INT NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `description` TEXT NOT NULL,
  `token` varchar(100) NOT NULL,
  `photo` MEDIUMTEXT NOT NULL,
  `aim` varchar(500) NOT NULL,
  `create_datetime` DATETIME NOT NULL,
  `last_modified_datetime` DATETIME ,
  `FK_DEADLINE_type` varchar(200) NOT NULL,
  `deadline_value` varchar(254) NOT NULL,
  `FK_CLASSROOM_id_number` INT NOT NULL,
  `FK_CATEGORY_category_name` varchar(300) NOT NULL,
  FOREIGN KEY (`FK_DEADLINE_type`) REFERENCES deadline(type),
  FOREIGN KEY (`FK_CLASSROOM_id_number`) REFERENCES classroom(id_number),
  FOREIGN KEY (`FK_CATEGORY_category_name`) REFERENCES category(category_name),
  PRIMARY KEY (`id_number`)
)  ENGINE=InnoDB;

CREATE TABLE `challenge_template` (
  `id_number` INT NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `description` TEXT NOT NULL,
  `photo` MEDIUMTEXT NOT NULL,
  `aim` varchar(500) NOT NULL,
  `added_datetime` DATETIME NOT NULL,
  `last_modified_datetime` DATETIME ,
  `status` DATETIME ,
  `FK_CATEGORY_category_name` varchar(300) NOT NULL,
  `FK_USERS_email` varchar(255) NOT NULL,
  FOREIGN KEY (`FK_USERS_email`) REFERENCES users(email),
  FOREIGN KEY (`FK_CATEGORY_category_name`) REFERENCES category(category_name),
  PRIMARY KEY (`id_number`)
)  ENGINE=InnoDB;


CREATE TABLE `challenge_user` (
  `id_number` INT NOT NULL AUTO_INCREMENT,
  `FK_CHALLENGE_id_number` INT NOT NULL,
  `FK_USERS_email` varchar(255) NOT NULL,
  FOREIGN KEY (`FK_CHALLENGE_id_number`) REFERENCES challenge(id_number),
  FOREIGN KEY (`FK_USERS_email`) REFERENCES users(email),
  PRIMARY KEY (`id_number`)
)  ENGINE=InnoDB;


CREATE TABLE `rubic` (
  `id_number` INT NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `description` MEDIUMTEXT NOT NULL,
  `create_datetime` DATETIME NOT NULL,
  `last_modified_datetime` DATETIME ,
  `datajson` MEDIUMTEXT NOT NULL,
  `FK_CHALLENGE_id_number` INT NOT NULL,
  FOREIGN KEY (`FK_CHALLENGE_id_number`) REFERENCES challenge(id_number),
  PRIMARY KEY (`id_number`)
)  ENGINE=InnoDB;

CREATE TABLE `rubic_template` (
  `id_number` INT NOT NULL AUTO_INCREMENT,
  `title` varchar(250) NOT NULL,
  `description` MEDIUMTEXT NOT NULL,
  `create_datetime` DATETIME NOT NULL,
  `last_modified_datetime` DATETIME ,
  `datajson` MEDIUMTEXT NOT NULL,
  `status` varchar(250) NOT NULL,
  `FK_USERS_email` varchar(255) NOT NULL,
  FOREIGN KEY (`FK_USERS_email`) REFERENCES users(email),
  PRIMARY KEY (`id_number`)
)  ENGINE=InnoDB;

CREATE TABLE `request_log` (
  `id_number` INT NOT NULL AUTO_INCREMENT,
  `endpoint` varchar(250) NOT NULL,
  `request_type` varchar(50) NOT NULL,
  `data` MEDIUMTEXT NOT NULL,
  `reqdatetime` DATETIME NOT NULL,
  `ip` varchar(50) NOT NULL,
  `FK_USERS_email` varchar(255) ,
  FOREIGN KEY (`FK_USERS_email`) REFERENCES users(email),
  PRIMARY KEY (`id_number`)
)  ENGINE=InnoDB;

CREATE TABLE `general_logs` (
  `id_number` INT NOT NULL AUTO_INCREMENT,
  `data` MEDIUMTEXT NOT NULL,
  `reqdatetime` DATETIME NOT NULL,
  `ip` varchar(50) NOT NULL,
  `FK_USERS_email` varchar(255) ,
  FOREIGN KEY (`FK_USERS_email`) REFERENCES users(email),
  PRIMARY KEY (`id_number`)
)  ENGINE=InnoDB;
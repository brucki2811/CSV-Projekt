-- Autor: Michael Bruckner
-- Date: 12-01-2016
-- Version: 1.4

CREATE DATABASE wahlen DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_general_ci;
USE wahlen;

CREATE TABLE wahlkreis(
	wnr INT PRIMARY KEY,
	wname VARCHAR(255)
) ENGINE = INNODB;

CREATE TABLE bezirk(
	bnr INT PRIMARY KEY,
	bname VARCHAR(255),
	wnr INT,
	FOREIGN KEY (wnr) REFERENCES wahlkreis(wnr) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE wahl(
	termin DATE PRIMARY KEY,
	mandate INT
) ENGINE = INNODB;

CREATE TABLE partei(
	abkuerzung VARCHAR(255) PRIMARY KEY,
	pname VARCHAR(255)
) ENGINE = INNODB;

CREATE TABLE kandidatur(
	abkuerzung VARCHAR(255),
	wnr INT,
	termin DATE,
	listenplatz INT,
	PRIMARY KEY (abkuerzung,wnr,termin),
	FOREIGN KEY (abkuerzung) REFERENCES partei(abkuerzung) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (wnr) REFERENCES wahlkreis(wnr) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (termin) REFERENCES wahl(termin) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE wahlsprengel(
	bnr INT,
	termin DATE,
	spnr INT,
	ungueltige INT,
	abgegeben INT,
	wahlberechtigte INT,
	PRIMARY KEY (bnr,termin,spnr),
	FOREIGN KEY (bnr) REFERENCES bezirk(bnr) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (termin) REFERENCES wahl(termin) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE sprengelstimmen(
	abkuerzung VARCHAR(255),
	bnr INT,
	termin DATE,
	spnr INT,
	gueltige INT,
	PRIMARY KEY (abkuerzung,bnr,termin,spnr),
	FOREIGN KEY (abkuerzung) REFERENCES partei(abkuerzung) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (bnr,termin,spnr) REFERENCES wahlsprengel(bnr,termin,spnr) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE wahlstimmen(
	termin DATE,
	abkuerzung VARCHAR(255),
	gesamte INT,
	PRIMARY KEY(termin,abkuerzung),
	FOREIGN KEY(termin) REFERENCES wahl(termin) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(abkuerzung) REFERENCES partei(abkuerzung) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE hochrechnung(
	termin DATE,
	zeitpunkt TIME,
	PRIMARY KEY(termin,zeitpunkt),
	FOREIGN KEY(termin) REFERENCES wahl(termin) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = INNODB;

CREATE TABLE hochrechnungsdaten(
	termin DATE,
	zeitpunkt TIME,
	abkuerzung VARCHAR(255),
	prozent FLOAT,
	PRIMARY KEY(termin,zeitpunkt,abkuerzung),
	FOREIGN KEY(termin,zeitpunkt) REFERENCES hochrechnung(termin,zeitpunkt) ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY(abkuerzung) REFERENCES partei(abkuerzung) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE = INNODB;


USE wahlen;
DELIMITER //

DROP PROCEDURE IF EXISTS erstelleHochrechnung//

CREATE PROCEDURE erstelleHochrechnung(IN termin DATE, IN zeitpunkt TIME) BEGIN

  INSERT INTO hochrechnung VALUES (termin, zeitpunkt);

  INSERT INTO hochrechnungsdaten SELECT sprengelstimmen.termin, zeitpunkt, sprengelstimmen.abkuerzung, 
  SUM(sprengelstimmen.gueltige) / (SELECT SUM(sprengelstimmen.gueltige) FROM sprengelstimmen) * 100 
  FROM sprengelstimmen where sprengelstimmen.termin = termin GROUP BY abkuerzung;

END//

DELIMITER ;

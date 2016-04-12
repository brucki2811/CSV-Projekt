DELIMITER //

DROP PROCEDURE IF EXISTS erstelleHochrechnung//

CREATE PROCEDURE erstelleHochrechnung(IN termin DATE, IN zeitpunkt TIME) BEGIN

  INSERT INTO hochrechnung VALUES (termin, zeitpunkt);

  INSERT INTO hochrechnungsdaten SELECT
                           sprengelstimmen.termin,
                           zeitpunkt,
                           sprengelstimmen.abkuerzung,
                           sprengelstimmen.gueltige / (SELECT SUM(gueltige) FROM sprengelstimmen WHERE sprengelstimmen.termin = termin) * 100
                           FROM sprengelstimmen WHERE sprengelstimmen.termin = termin GROUP BY abkuerzung;

END//

DELIMITER ;

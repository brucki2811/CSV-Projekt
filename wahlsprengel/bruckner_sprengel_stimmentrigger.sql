USE wahlen;
DELIMITER //

DROP TRIGGER IF EXISTS gesamtStimmen//

CREATE TRIGGER gesamtStimmen
AFTER INSERT ON wahlstimmen FOR EACH ROW
  BEGIN
    INSERT INTO wahlstimmen VALUES (new.abkuerzung, new.termin, new.gesamte)
    ON DUPLICATE KEY UPDATE gesamtanzahl = gesamtanzahl + new.gesamte;
  END//

DELIMITER ;
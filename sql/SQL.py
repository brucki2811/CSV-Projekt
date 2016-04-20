__author__ = "Michael Bruckner"
__version__ = 1.0
__date__ = 20160409

from datetime import datetime
from orderedset.OrderedSet import OrderedSet
from sql.Connector import MySQLConnector


class SQL:
    def __init__(self, username, password, database, wahltermin):
        self.conn = MySQLConnector(username, password, database)
        self.wahltermin = wahltermin

    def writeList(self, datalist):
        """
        Die Funktion liest die Daten aus der Tabelle in die Datenbank ein.
        :param datalist: Ueber die datalist werden die einzelnen Informationen der Tabelle uebergeben
        :return:
        """
        ses = self.conn.getSession()

        ses.execute("DELETE FROM sprengelstimmen")
        ses.execute("DELETE FROM wahlsprengel")
        ses.execute("DELETE FROM wahl")

        Wahl = self.conn.getClass("wahl")
        wahl = Wahl(termin=self.wahltermin, mandate=100)
        ses.add(wahl)

        Wahlsprengel = self.conn.getClass("wahlsprengel")
        Sprengelstimmen = self.conn.getClass("sprengelstimmen")

        parteien = []
        for key in datalist[0].keys():
            # "T", "WV", "WK",
            if key not in ["T", "WV","WK","SPR", "BZ", "WBER", "ABG", "UNG", "\n","\r","\n\r","\r\n"]:
                parteien.append(key)

        for row in datalist:
            sprengel = Wahlsprengel(spnr=int(row["SPR"]), bnr=int(row["BZ"]), termin=wahl.termin, wahlberechtigte=int(row["WBER"]), abgegeben=int(row["ABG"]), ungueltige=int(row["UNG"]))
            ses.add(sprengel)
            for partei in parteien:
                stimmabgabe = Sprengelstimmen(spnr=int(row["SPR"]), bnr=int(row["BZ"]), termin=wahl.termin, abkuerzung=partei, gueltige=int(row[partei]))
                ses.add(stimmabgabe)

        ses.commit()

    def loadList(self):
        """
        Liest die Daten aus der Datenbank in die Tabelle hinein
        :return:
        """
        ses = self.conn.getSession()

        query = "SELECT  sprengelstimmen.abkuerzung, wahlkreis.wnr, bezirk.bnr, wahlsprengel.spnr, wahlsprengel.wahlberechtigte, " \
                "wahlsprengel.abgegeben, wahlsprengel.ungueltige, sprengelstimmen.gueltige " \
                "FROM wahlkreis " \
                "INNER JOIN bezirk ON wahlkreis.wnr = bezirk.wnr " \
                "INNER JOIN wahlsprengel ON bezirk.bnr = wahlsprengel.bnr " \
                "AND wahlsprengel.termin = '" + self.wahltermin + "' " \
                "INNER JOIN sprengelstimmen ON sprengelstimmen.termin = '" + self.wahltermin + "' " \
                "AND sprengelstimmen.bnr = bezirk.bnr " \
                "AND sprengelstimmen.spnr = wahlsprengel.spnr;"

        result = ses.execute(query).fetchall()

        header = OrderedSet(["WK", "BZ", "SPR", "WBER", "ABG", "UNG"])
        datalist = []
        row = {}
        partei = None
        for i in range(0, len(result)):
            abk = result[i]["abkuerzung"]
            if partei is None or abk == partei:
                if row:
                    datalist.append(row)
                row = {}
                partei = abk
                row["WK"] = result[i]["wnr"]
                row["BZ"] = result[i]["bnr"]
                row["SPR"] = result[i]["spnr"]
                row["WBER"] = result[i]["wahlberechtigte"]
                row["ABG"] = result[i]["abgegeben"]
                row["UNG"] = result[i]["ungueltige"]
            row[abk] = result[i]["gueltige"]
            header.add(abk)

        return datalist, list(header)

    def results(self):
        """
        Ruft die Procedure erstelleHochrechnung auf und generiert eine Hochrechnung.
        :return:
        """
        termin = self.wahltermin
        zeitpunkt = datetime.now().time().strftime("%H:%M:%S")

        conn = self.conn.getConnection()
        cursor = conn.cursor()

        args = (termin, zeitpunkt)
        cursor.callproc("erstelleHochrechnung", args)

        cursor.close()
        conn.commit()

        ses = self.conn.getSession()
        ses.commit()

        query = "SELECT abkuerzung, prozent FROM hochrechnungsdaten WHERE termin = '" + termin + "' AND zeitpunkt = '" + zeitpunkt + "';"
        result = ses.execute(query).fetchall()

        column = {}
        header = []
        datalist = []
        for i in range(0, len(result)):
            column[result[i]["abkuerzung"]] = result[i]["prozent"]
            header.append(result[i]["abkuerzung"])
        datalist.append(column)

        return datalist, header

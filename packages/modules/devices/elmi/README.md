# ELMI Power Hub 400

Implementiert nach ModbusTCP Protocol Hub 400 V2.2, 22.01.2026.
Standard: TCP 502, Unit-ID 1; alle Werte Big-Endian, High-Word zuerst.
Lesen mit FC03, Schreiben mit FC16.

| Komponente | Register | Typ | Faktor |
|---|---|---|---|
| Speicher-SOC | 1004 | U32 | 0,01 % |
| Speicher-AC-Leistung | 1024 | S32 | 0,1 W |
| Batteriezustand | 1046 | U32 | 1=laden, 2=entladen |
| Lade-/Entladesperre | 1054/1056 | U32 | Bool |
| Verfügbare Lade-/Entladeleistung | 1074/1076 | U32 | 0,1 W |
| Zähler-Ströme | 1030/1032/1034 | U32 | 0,01 A |
| Zähler-Spannungen | 1036/1038/1040 | U32 | 0,01 V |
| Frequenz | 1042 | U32 | 0,001 Hz |
| PV-Leistung | 1068 | U32 | 0,1 W |
| Netzbezug | 1070 | U32 | 0,1 W |
| Netzeinspeisung, negativ | 1072 | S32 | 0,1 W |
| Heartbeat-Rückmeldung | 1052 | U32 | 1 |
| Grid-Sollleistung | 1200 | S32 | 0,1 W |
| Heartbeat schreiben | 1204 | U32 | 1 |

Zählerleistung = Register 1070 + Register 1072. PV-Erzeugung ist in openWB
negativ. Die Richtung der Speicherleistung wird über den Batteriezustand
normalisiert, da die Dokumentation das Vorzeichen von 1024 nicht definiert.
Energiezähler werden mit dem vorhandenen SimCounter aus Leistung integriert.
Es gibt keine echten Energiezähler und keine phasenweisen Wirkleistungen.
Die Stromrichtung pro Phase wird aus der Gesamtleistung abgeleitet; gegenläufige
Phasenflüsse lassen sich damit nicht erkennen. Den Hub-Zähler nur dann als EVU
verwenden, wenn sein Messpunkt tatsächlich den Netzanschlusspunkt erfasst.

## Steuerung

Bei openWB-Vorzeichen (Laden positiv, Entladen negativ):

    Grid-Soll = EVU-Ist - Speicher-Ist + Speicher-Soll

Das gilt auch für Speicher-Soll = 0: Grid-Soll = 0 würde stattdessen
Eigenverbrauchsausgleich anfordern. EVU-Ist wird vom Regler übergeben.
Der Speicher-Istwert wird vor jeder Sollwertberechnung frisch gelesen.
Register 1200 wird frühestens nach 11 Sekunden erneut geschrieben. Es wird
jeweils der neueste Sollwert verwendet. Der Heartbeat wird bei jedem gültigen
Steueraufruf vor dem Sollwert geschrieben, auch innerhalb der 11 Sekunden.
Der aktuelle Heartbeat wird gelesen und modulo 2^32 erhöht, auch nach Neustarts.
Der openWB-Regelzyklus muss zuverlässig kürzer als 30 Sekunden sein.

Bei `power_limit=None` oder fehlendem EVU-Wert wird kein Heartbeat geschrieben.
ELMI besitzt laut Dokumentation kein Register zur sofortigen Rückgabe an die
Eigenregelung. Nach 30 Sekunden ohne Heartbeat beginnt die konfigurierte
Offline-Strategie. Standardmäßig bleibt der letzte Modbus-Sollwert zunächst
bis zu fünf Minuten bestehen. Das muss beim Einsatz berücksichtigt werden.

ELMI nennt +5 kW als kleinsten positiven und -10 kW als kleinsten negativen
Grid-Sollwert sowie eine Genauigkeit von etwa ±500 W. Kleinere Werte werden
bewusst nicht auf höhere Leistungen angehoben; ihr Verhalten und insbesondere
eine gewünschte Speicher-Nullleistung müssen am Gerät geprüft werden.
Die Register 1074/1076 beschreiben verfügbare Lade-/Entladeleistung, werden hier
aber nicht als Grid-Sollwertgrenzen interpretiert: Grid- und Speicherleistung
sind wegen anderer Verbraucher/Erzeuger nicht gleich.
Sie werden als maximale Lade-/Entladeleistung an den openWB-Regler gemeldet,
bei gesetzter Lade-/Entladesperre (1054/1056) jeweils als 0 W.

Der interne EMS-Plan bleibt aktiv. Laut Hersteller für externe Regelung
ForceSOC_StartChg=0 und End SOC=100 einstellen; Entladesperre, Discharge Ratio
und AC Grid Charge Limitation im ELMI-Backend beachten.

Das Beispiel auf Seite 7 enthält widersprüchliche Vorzeichen, eine falsche
Leistungsangabe und FC03 als Schreibcode. Implementiert sind die Registertabelle
und die korrigierte Funktionscodeliste: -10 kW => -100000 als S32, FC16.

## Projektbeschreibung


Die Anwendung ist eine Gruppen-Filmempfehlungs-App wie „Tinder für Filme“. Nutzer können gemeinsam mit Freunden oder Familie einer Lobby beitreten. Anschließend werden allen Teilnehmern Filme aus einer Datenbank vorgeschlagen. Jeder Nutzer kann einen Film liken, disliken oder als „schon gesehen“ markieren. Sobald alle Teilnehmer denselben Film geliked haben, wird dieser als gemeinsames Ergebnis angezeigt. Filme, die von einem Nutzer als „schon gesehen“ markiert wurden, werden aus der Auswahl ausgeschlossen. Falls nach 50 Swipes kein perfekter Treffer gefunden wurde, wird der Film mit der besten Bewertung angezeigt. Zusätzlich gibt es „Honorable Mentions“, bei denen die Plätze 2 bis 5 angezeigt werden. Nutzer können Filme außerdem zu einer „Später ansehen“-Liste hinzufügen und im Hauptmenü ihre gesehenen sowie gespeicherten Filme ansehen.

Must have:
- Unsere Datenbank mit der externen API verbinden um Daten zu holen.
- SQL Injektion verhindern
- Datenbank soll das Ergebnis des am besten gewählten Film ausgeben

Nice to have:
- Filme sollten gefiltert werden nach Genre, Erscheinungsjahr usw.


## ERM

![ER-Diagramm](<ERM.png>)
## 1NF
![alt text](image-1.png)

Passt perfekt musste man nichts ändern.

## 2NF
![alt text](image-1.png)

muss man wieder nichts ändern 

## 3NF
![alt text](image-3.png)

hab bei Movie_details die PK zu movie_id fk gemacht






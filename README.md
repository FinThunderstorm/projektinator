# Projektinator

Kurssisuoritus Helsingin yliopiston [tietokantasovelluskurssin](https://hy-tsoha.github.io/materiaali/index) kevään 2021 toteutukseen.
Sovellus pyörii osoitteessa [projektinator.herokuapp.com](https://projektinator.herokuapp.com).

## Idea

Tarkoitus on toteuttaa projektin hallintaan käytettävä sovellus, jolla voidaan seurata projektin edistymistä, ajankäyttöä ja hallita niitä.

## Tech stack

Python & Flask
PostgreSQL
Suoritetaan kehityksen aikaisesti Docker-kontitettuna, tuotantoversio Herokussa normaalina sovelluksena

## Todo

| Ominaisuus | Valmis? |
| ---------- | ------- |
| Pääsivu    | ❌      |

## Projektin aikana tapahtunutta

### Ongelma #1:

Mac ei halunnut antaa suorittaa Pythonin virtualenviä ilman sudoja. *Ratkaisu:* rakennetaan kehitysympäristö VSCoden devcontainereiden avustuksella.

### Ongelma #2: 

VSCoden devcontainer.json ei tue settings osioon tietojen hakemista .env tiedostosta, liittyy [GitHub Issue #2809 @ microsoft/vscode](https://github.com/microsoft/vscode/issues/2809) - asiaa ei ole neljän vuoden aikana saatettu korjatuksi. *Ratkaisu:* tehdään geneeriset tunnukset kehityksen ajaksi ja asetetaan tuotantoon erikseen vastaavat ympäristömuuttujat vahvennetuilla tunnuksilla. 

# Projektinator

Kurssisuoritus Helsingin yliopiston [tietokantasovelluskurssin](https://hy-tsoha.github.io/materiaali/index) kevään 2021 toteutukseen.
Sovellus pyörii osoitteessa [projektinator.herokuapp.com](https://projektinator.herokuapp.com).

## Idea

Tarkoitus on toteuttaa projektinhallintatyökalu, jolla voidaan seurata projektin edistymistä ja ajankäyttöä, sekä hallita niitä.

## Tech stack

- Python & Flask
- PostgreSQL
- Suoritetaan kehityksen aikaisesti Docker-kontitettuna, tuotantoversio Herokussa normaalina sovelluksena

## Kehitettäessä sovellusta

- Flask hot reload: ensin anna komento **export FLASK_ENV=development** ja tämän jälkeen suorita normaalisti **flask run**
- Postgresin dev-konttiin pääsee seuraavalla komennolla **docker exec -it projektinator_devcontainer_db_1 psql -U example -d projektinator**

## Todo

| Ominaisuus                                        | Valmis? |
| ------------------------------------------------- | ------- |
| Kehitysympäristö ja automatisoitu Herokuun vienti | ✅      |
| Tietokannan suunnittelu / 1. versio               | ✅      |
| Kirjautuminen                                     | ❌      |
| Dashboard                                         | ❌      |

## Projektin aikana tapahtunutta tulevaisuuden varalle muistiin

### Ongelma #1

Mac ei halunnut antaa suorittaa pip3-paketinhallinnan asennuksia ilman sudoja. Oletettavasti aiemmin käytetty virheellisesti sudo-oikeuksia käytettäessä pip3:a. _Ratkaisu:_ rakennetaan kehitysympäristö VSCoden devcontainereiden avustuksella.

### Ongelma #2

VSCoden devcontainer.json ei tue **settings** osioon tietojen hakemista .env tiedostosta, liittyy [GitHub Issue #2809 @ microsoft/vscode](https://github.com/microsoft/vscode/issues/2809) - asiaa ei ole neljän vuoden aikana saatettu korjatuksi. _Ratkaisu:_ tehdään geneeriset tunnukset kehityksen ajaksi ja välitetään ne käyttäen .env-tiedostoa ja asetetaan tuotantoon erikseen vastaavat ympäristömuuttujat vahvennetuilla tunnuksilla.

### Ongelma #3

PostgreSQL:n Docker image ei ottanut oikeita käyttäjätietoja sisälle, tietokantaan ei päässyt käsiksi millään käyttäjällä. _Ratkaisu:_ poista käytössä oleva Docker-kontti ja tämän jälkeen poista kaikki käyttämättä olevat volumet **docker volume prune** komennolla. Lähde [https://github.com/docker-library/postgres/issues/453#issuecomment-393939412](https://github.com/docker-library/postgres/issues/453#issuecomment-393939412)

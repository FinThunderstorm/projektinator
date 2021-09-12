# Projektinator

Kurssisuoritus Helsingin yliopiston [tietokantasovelluskurssin](https://hy-tsoha.github.io/materiaali/index) kevään 2021 toteutukseen.
Sovellus pyörii osoitteessa [projektinator.herokuapp.com](https://projektinator.herokuapp.com).

## Idea

Tarkoitus on toteuttaa projektinhallintatyökalu, jolla voidaan seurata projektin edistymistä ja ajankäyttöä, sekä hallita niitä.

Käyttäjätasoja on kolme:

- admin = käyttöoikeus kaikkeen
- leader = peruskäyttäjä, joka pystyy hallinnoimaan projektien asetuksia
- user = peruskäyttäjä

Sovelluksella voi luoda projekteja. Projekti voi sisältää useita erilaisia ominaisuuksia. Ominaisuudet voi sisältää erilaisia tehtäviä. Tehtäville voidaan antaa kuvaus, mitä pitää tehdä ja merkitä kauan siihen on käytetty aikaa. Tehtäville, ominaisuuksille ja projekteille voi antaa erilaisia lippuja kuvaamaan niiden luonnetta ja tehtäviä sekä ominaisuuksia voi kommentoida = kerätä tietoa edistymisestä. Tehtäville ja ominaisuuksille voi antaa kiireellisyysluokituksen. Ominaisuuksia ja tehtäviä voidaan seurata ns. **dashboardin** avulla projektikohtaisesti.

Sivurakenne:

- Dashboard
- Login/register-form
- Projektilistaus
- Projektin sivu
- Tehtävän sivu


- Pääsivu / henkilökohtainen työpöytä
- Kirjautumissivu + rekisteröitymislomake, jolla pääkäyttäjä voi luoda uusia käyttäjiä
- Listaus projekteista
- Projektin sivu, joka listaa ominaisuudet ja tehtävät
- Ominaisuuden sivu, joka listaa tehtävät
- Tehtävän sivu, josta saa tehtävän lisätiedot auki, ja pystyy tarvittaessa muuttamaan sen tietoja.
- Tiimien hallinta
- Hallintasivu, josta voi hallita asennuksen oikeuksia ja käyttäjien asetuksia.

Testaustunnukset:
Pääkäyttäjä: admin/admin

## Tech stack

- Python & Flask
- PostgreSQL
- Suoritetaan kehityksen aikaisesti Docker-kontitettuna, tuotantoversio Herokussa normaalina sovelluksena.

## Kehitettäessä sovellusta muistettavia käytännöllisiä komentoja

- Flask hot reload: ensin anna komento **export FLASK_ENV=development** ja tämän jälkeen suorita normaalisti **flask run**
- Postgresin dev-konttiin pääsee seuraavalla komennolla **docker exec -it projektinator_devcontainer_db_1 psql -U example -d projektinator**

## Todo

Tilojen kuvaus: ✅ = valmis, 🏃 = työn alla, ❌ = aloittamatta



## Tyylittely

- Logo: öljylamppu: <https://publicdomainvectors.org/en/free-clipart/Oil-lamp-image/71630.html>, fontti: <https://ianbarnard.co/products/montebello-cursive-script-typeface>
- Taustakuva-kirjautuminen: <https://www.pexels.com/fi-fi/kuva/ihmiset-kuppi-muki-toissa-3183150>, Kuvaaja fauxels palvelusta Pexels
- Taustaväri-tumma: #780252, korostusväri-kirkas: #FF0064
- Käytetty kirjasto: Bulma & scss-installaatio

## Projektin aikana tapahtunutta tulevaisuuden varalle muistiin

### Ongelma #1

Mac ei halunnut antaa suorittaa pip3-paketinhallinnan asennuksia ilman sudoja. Oletettavasti aiemmin käytetty virheellisesti sudo-oikeuksia käytettäessä pip3:a. _Ratkaisu:_ rakennetaan kehitysympäristö VSCoden devcontainereiden avustuksella.

### Ongelma #2

VSCoden devcontainer.json ei tue **settings** osioon tietojen hakemista .env tiedostosta, liittyy [GitHub Issue #2809 @ microsoft/vscode](https://github.com/microsoft/vscode/issues/2809) - asiaa ei ole neljän vuoden aikana saatettu korjatuksi. _Ratkaisu:_ tehdään geneeriset tunnukset kehityksen ajaksi ja välitetään ne käyttäen .env-tiedostoa ja asetetaan tuotantoon erikseen vastaavat ympäristömuuttujat vahvennetuilla tunnuksilla.

### Ongelma #3

PostgreSQL:n Docker image ei ottanut oikeita käyttäjätietoja sisälle, tietokantaan ei päässyt käsiksi millään käyttäjällä. _Ratkaisu:_ poista käytössä oleva Docker-kontti ja tämän jälkeen poista kaikki käyttämättä olevat volumet **docker volume prune** komennolla. Lähde: [https://github.com/docker-library/postgres/issues/453#issuecomment-393939412](https://github.com/docker-library/postgres/issues/453#issuecomment-393939412)

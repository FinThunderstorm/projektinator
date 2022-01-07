# Projektinator - Your project's best friend

Kurssisuoritus Helsingin yliopiston [tietokantasovelluskurssille](https://hy-tsoha.github.io/materiaali/index).
Sovellus pyörii osoitteessa [projektinator.herokuapp.com](https://projektinator.herokuapp.com).

## Idea

Projektinator on ketterän kehityksen projektinhallintatyökalu, jolla voidaan tehdä projektien tilaseurantaa sekä seurata käytettyjä työtunteja.

### Projekti

Sovelluksen toiminnan perusykskkö on projekti. Projekti koostuu useita toiminnallisuuksista. Projektilla on projektin omistaja, kuka vastaa projektista.

#### Oikeudet

- katsella: kaikki käyttäjät
- luoda: kaikki käyttäjät, peruskäyttäjä ei voi lisätä projektiomistajaksi kuin itsensä tai tiiminsä jäsenen.
- muokata: vain projektin omistaja tai pääkäyttäjäoikeudellinen
- poistaa: vain projektin omistaja tai pääkäyttäjäoikeudellinen

### Ominaisuus

Projekti koostuu ominaisuuksista. Ominaisuus kuvaa jotain projektin toteutettavaa osa-aluetta. Ominaisuuteen voi liittyä tehtäviä sekä työ-aikaa seuraavia kommentteja.

#### Oikeudet

- katsella: kaikki käyttäjät
- luoda: kaikki käyttäjät, peruskäyttäjä ei voi lisätä ominaisuuden omistajaksi kuin itsensä tai tiiminsä jäsenen.
- muokata: vain ominaisuuden omistaja tai tiiminvetäjäoikeudellinen
- poistaa: vain ominaisuuden omistaja tai tiiminvetäjäoikeudellinen

### Tehtävä

Ominaisuus koostuu tehtävistä. Tehtävä kuvaa jotain projektin toteutettavaa ominaisuutta. Tehtävään voi liittyä tehtäviä työ-aikaa seuraavia kommentteja.

#### Oikeudet

- katsella: kaikki käyttäjät
- luoda: kaikki käyttäjät, peruskäyttäjä ei voi lisätä tehtävän hoitajaksi kuin itsensä tai tiiminsä jäsenen.
- muokata: vain tehtävän hoitaja tai tiiminvetäjäoikeudellinen
- poistaa: vain tehtävän hoitaja tai tiiminvetäjäoikeudellinen

### Kommentti

Ominaisuus tai tehtävä voi koostua kommenteista. Kommentti kertoo niihin liittyvä havaintoja sekä niihin käytettyä työaikaa.

#### Oikeudet

- katsella: kaikki käyttäjät
- luoda: kaikki käyttäjät
- muokata: vain kommentin luoja tai tiiminvetäjäoikeudellinen
- poistaa: vain kommentin luoja tai tiiminvetäjäoikeudellinen

### Tiimi

Käyttäjä voi kuulua tiimiin, ja tiimi määrittelee peruskäyttäjän näkemät henkilöt niitä valittaessa

#### Oikeudet

- katsella: kaikki käyttäjät
- luoda: tiiminvetäjäoikeudelliset
- muokata: vain tiimin vetäjä tai pääkäyttäjäoikeudellinen
- poistaa: vain tiimin vetäjä tai pääkäyttäjäoikeudellinen

### Käyttäjätasoja on kolme:

Vain pääkäyttäjäoikeudellinen voi korottaa eri käyttäjien oikeustasoja. Käyttäjä ei voi itse muuttaa oikeustasoaan, vaikka olisi pääkäyttäjä.

- admin = pääkäyttäjäoikeus
- leader = käyttäjä, jolla on tiimin hallintaoikeudet
- user = peruskäyttäjä

## Testaustunnukset:

- Pääkäyttäjä: `admin / admin`
- Tiimin vetäjä: `leader / leader`
- Peruskäyttäjä: `project / project`

## Tech stack

- Python 3.10
- Flask
- Material Design Lite -käyttöliittymäkirjasto
- PostgreSQL
- Docker

## Huomioitavaa kehitettäessä

- Kehitysaikaisen sovellusympäristön saa käyntiin komennolla `docker-compose up -d`
- Sovelluksen logeja voi katsoa komennolla `docker-compose logs -f app`
- Tuotantoympäristöä vastaavan sovellusympäristön saa käyntiin komennolla `docker-compose -f docker-compose.prod.yml up -d`
- Postgresin dev-konttiin pääsee seuraavalla komennolla `docker exec -it projektinator-db psql -U example -d projektinator`

Sovelluskehitysympärstö tarvitsee `.env`-tiedoston, jonka sisältö on seuraava. Postgresin hostnamen täytyy vastata docker-composesta sille tulevaa. Oletuksena `projektinator-db`.

```
POSTGRES_USER=example
POSTGRES_DB=projektinator
POSTGRES_PASSWORD=example
POSTGRES_HOSTNAME=projektinator-db
POSTGRES_PORT=5432

SECRET=example
DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOSTNAME}:${POSTGRES_PORT}/${POSTGRES_DB}
```

## Tyylittely

- Logo: öljylamppu: <https://publicdomainvectors.org/en/free-clipart/Oil-lamp-image/71630.html>, fontti: <https://ianbarnard.co/products/montebello-cursive-script-typeface>
- Taustakuva-kirjautuminen: <https://www.pexels.com/fi-fi/kuva/ihmiset-kuppi-muki-toissa-3183150>, Kuvaaja fauxels palvelusta Pexels

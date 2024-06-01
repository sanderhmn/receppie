# Recəppie
by Sander Heimans

#### Overview

Deze app wordt gemaakt voor mensen die niet weten wat ze moeten koken. Voor als je ergens zin in hebt maar niet weet waarin, 
en als je dan googlet krijg je allemaal exotische recepten waar je geen zin in hebt. In deze app kan iedereen zijn favoriete 
recepten van verschillende bronnen op een centrale plek bijhouden. Je kan nieuwe recepten automatisch toevoegen via de URL
en om suggesties te krijgen kan je zoeken op ingrediënten die je nog in huis hebt of op type gerecht. Vervolgens kun je de zoekresultaten filteren op bijvoorbeeld vegetarisch, budget, gezond etc. Op de homepagina staan ook wat willekeurige recepten als inspiratie.

De app wordt ontwikkeld voor een kleine set gebruikers: voornamelijk mezelf en vrienden die het ook willen gebruiken. Deze 
gebruikers zullen een account hebben en de app regelmatig gebruiken. Waarschijnlijk wordt de app voornamelijk op mobiele
apparaten gebruikt.

#### Core features:

- Homepagina met willekeurige recepten te inspiratie
 
<img src="readme/main.png" width="533px" height="300px">

- Recepten toevoegen via URL

<img src="readme/toevoegen.png" width="533px" height="300px">

- Google Chrome extensie om recepten direct vanuit de bron toe te voegen

<img src="readme/extension.png" width="533px" height="300px">

- Zoeken op ingredienten 

<img src="readme/zoekpagina.png" width="533px" height="300px">

#### Possible additional features:

- Vragenlijst waar je zin in hebt (keuken/bereidingstijd/etc.) -> suggestie
- Google Chrome extensie om op een recept-pagina dat recept direct toe te voegen
- Kookboeken kunnen fotograferen (image to text)
- Notificeren welk gerecht ingrediënten heeft die in de aanbieding zijn / totale prijs voor ingrediënten weergeven (voor 1 supermarkt zodat het meer een indicatie is van de prijs)
- Aantal gerechten rangschikken en op basis daarvan suggestie 
- Recepten van vrienden kunnen bekijken, laatst bekeken recept als suggestie voor vrienden
- Alle ingredienten meteen bestellen via picnic

#### Requirements 

Componenten:
- Flask, SQLAlchemy, postgresql (database and functionality)
- BeautifulSoup4 (scraping)
- Bootstrap 5 

Bronnen:
- Allerhande, Hello Fresh

#### Learning goals

- Implement Flask to produce usable application
- Learn Bootstrap 5, HTML and CSS to produce nice looking UI

#### Usage for host

Link Flask to postgresql
- export DATABASE_URL = "postgresql://username:password@postgresql/receppie
Host application
- flask --debug run

#### Screencast
https://www.youtube.com/watch?v=KLOrAFZvqc4

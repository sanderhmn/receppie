# review door Hidde
1. search functie in app.py wordt opgenomen in de results route. Misschien overzichterlijker om bij de daadwerkelijke search route te implementeren
2. Je hebt nog een test functie geimplementeerd die nog niks toevoegd. 
3. Misschien zou je in de toekomst nog kunnen implementeren dat je bij het toevoegen van recepten met snel, gemiddeld of lange bereidingstijd dat als filter toevoegen bij je opgeslagen recepten. 
4. Heel nice dat je automatisch filters meegeeft als je opzoekt in je recepten. Misschien in de toekomst kan je implementeren dat je meerdere filters kan selecteren. 
5. Ik denk dat je zelf het ook al wilde implementeren maar dat je een home pagina hebt met al je opgeslagen recepten. 

# Wat is het tegengekomen probleem?
1. Search functie staat in de results route.
2. Loze testfunctie geimplementeerd
3. Bereidingstijd is (nog) niet bruikbaar als filter bij zoekpagina
4. Er was nog geen functionaliteit om meerdere filters aan te zetten
5. Er mist een pagina met alle toegevoegde recepten

# Hoe zou je dit beter kunnen maken?
1. Hele zoekfunctie naar de search-route verplaatsen
2. Verwijderen
3. Dropdown menu bij de zoekfunctie om eventueel te filteren op bereidingstijd
4. Heb ik gedaan: meer filters meegeven via de fetch request en sql query aanpassen zodat alle filters worden toegepast
5. Pagina toevoegen met alle recepten

# Wat voor afweging maak je? Vaak is een keuze voor iets ook een keuze tegen iets anders.
1. Keuze was eigenlijk alleen zodat er geen "/search?search={{query}}" in de URL zou staan maar "/results?search={{query}}" zodat de link duidelijk is in het geval van delen.
2. Hij is nu verwijderd.
3. Ik wil de UI simpel houden. Daarnaast was dit een tijdelijke oplossing omdat ik wel automatisch de bereidingstijd wil importeren via de scrape functie.
4. Ik had het nog niet af maar het is nu geïmplementeerd.
5. Het is nu nog geen functionaliteit die ik vereis van de app: het gaat vooral om het zoeken.
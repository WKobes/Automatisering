# Automatisering documentatie

In deze repository worden scripts bijgehouden om het publicatie- en controleproces van documenten te automatiseren.

## Automatische tests

### Publicatie
In de repository van iedere [ReSpec](https://respec.org/)-publicatie is een [script](scripts/build.yml) te vinden dat de volgende handelingen uitvoert:
* Genereer statische HTML-pagina
* Controleer op WCAG-criteria
* Genereer PDF-bestand


### Gebroken links
Iedere maandagochtend draait een controle op gebroken links in documenten gepubliceerd op https://publicatie.centrumvoorstandaarden.nl/.

De resultaten worden gepresenteerd in [links.md](links.md).

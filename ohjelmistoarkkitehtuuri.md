# Ohjelmistoarkkitehtuuri

## Sisällys

1. [Mitä arkkitehtuuri on?](#mitä-arkkitehtuuri-on)
2. [Miksi arkkitehtuuri on tärkeää?](#miksi-arkkitehtuuri-on-tärkeää)
3. [Ohjelmistokehityksen arkkitehtuurihistoria](#ohjelmistokehityksen-arkkitehtuurihistoria)
4. [Arkkitehtuuritasot](#arkkitehtuuritasot)
5. [Esimerkkinä: MyLeague](#esimerkkinä-myleague)
6. [Lyhenteet](#lyhenteet)

---

## Mitä arkkitehtuuri on?

> **Arkkitehtuuri on niiden päätösten joukko, jotka ovat kalliita muuttaa myöhemmin.**

Ajattele taloa. Tapetin voi vaihtaa viikonlopussa. Kantavan seinän siirto vaatii luvan, telineet ja uudet tukirakenteet. Ohjelmistossa jako on sama: jotkin päätökset ovat pintaa, toiset ovat kantavia rakenteita.

| Halpa muuttaa myöhemmin | Kallis muuttaa myöhemmin |
|-------------------------|--------------------------|
| Nappulan väri | Missä asuu sääntö *tulos kirjataan vain kerran* |
| Virheilmoituksen teksti | Onko sääntö yhdessä paikassa vai kopioitu kolmeen paikkaan |
| Yhden sivun asettelu | Tallennetaanko tulos tietokantaan vai tiedostoon |
| Napin fontti | Mikä osa saa kutsua mitäkin osaa |

![Rakennus ja ohjelmisto rinnakkain: tapetti on helppo muuttaa, kantava seinä kallis — sama jako ohjelmistossa](images/oa-01-building-vs-software.svg)

**IEEE** (Institute of Electrical and Electronics Engineers, kansainvälinen tekniikan standardijärjestö) määrittelee arkkitehtuurin näin: järjestelmän perusrakenne — **osat**, niiden **suhteet** ja **periaatteet**, joiden mukaan järjestelmää rakennetaan ja kehitetään.

Kolme kysymystä riittää alkuun:

| Kysymys | Mitä se tarkoittaa | Pieni esimerkki |
|---------|--------------------|------------------|
| **Mihin osiin jaetaan?** | Rakenne | Selain, API ja tietokanta — tai controller, service ja repository |
| **Kuka saa kutsua ketä?** | Suhteet | Service kutsuu repositorya. Repository ei kutsu controlleria. |
| **Millä säännöllä päätetään?** | Periaatteet | Sääntö asuu yhdessä paikassa. Salaisuuksia ei laiteta Gitiin. |

**API** (Application Programming Interface) on tyypillisesti HTTP-rajapinta: selain tai Swagger kutsuu osoitteita kuten `POST /api/matches`. **HTTP** (Hypertext Transfer Protocol) on se protokolla, jolla selain ja palvelin keskustelevat.

Toimiva koodi ja hyvä koodi eivät ole sama asia. Alla oleva metodi *toimii*: tulos tallentuu. Se on silti huono, jos sama `if`-tarkistus pitää kopioida jokaiseen paikkaan, joka koskee tulosta.

```csharp
// Toimii — mutta sääntö, tallennus ja HTTP-vastaus ovat samassa kasassa
[HttpPost("{id}/result")]
public IActionResult RecordResult(int id, int home, int away)
{
    var match = _matches.First(m => m.Id == id);
    if (match.HomeGoals is not null)
        return BadRequest("Tulos on jo kirjattu.");
    match.HomeGoals = home;
    match.AwayGoals = away;
    return Ok(match);
}
```

Hyvä rakenne ei näy ensimmäisessä demossa. Se näkyy siinä, että *seuraava* muutos sattuu yhteen paikkaan eikä viiteen.

Arkkitehtuuri ei ole kaunis kaavio seinällä. Se on vastaus kysymykseen: *missä tämä kuuluu asumaan, ja kuka saa tietää kenestä?*

---

## Miksi arkkitehtuuri on tärkeää?

Yhden illan koulutyössä arkkitehtuurilla ei ole väliä — mikä tahansa toimii. Ero näkyy vasta, kun ohjelmisto elää: kun siihen tulee lisää ominaisuuksia, lisää käyttäjiä, lisää tekijöitä.

**1. Muutoksen hinta kasvaa ajan myötä — jos rakenne ei tue sitä.** Ilman rakennetta jokainen uusi ominaisuus on hitaampi lisätä kuin edellinen, koska koodi on sotkeutunut itseensä. Hyvässä rakenteessa käyrä pysyy tasaisena: sadas ominaisuus on yhtä helppo lisätä kuin kymmenes.

![Kaksi käyrää: ilman rakennetta muutoksen hinta nousee jyrkästi, hyvässä rakenteessa se pysyy tasaisena](images/oa-02-change-cost.svg)

**2. Useampi ihminen työskentelee samassa koodissa.** Kun sääntö *tulos kirjataan vain kerran* asuu yhdessä paikassa, kaksi kehittäjää voi työskennellä eri osissa törmäämättä toisiinsa. Spagetissa kaikki koskee kaikkea.

**3. Virheet maksavat enemmän myöhemmin löydettynä.** Väärä tietokantavalinta tai puuttuva kerrosjako huomataan usein vasta, kun järjestelmä on jo tuotannossa ja täynnä dataa — silloin korjaus on moninkertaisesti kalliimpi kuin suunnitteluvaiheessa.

**4. Uusi tekijä pääsee sisään nopeammin.** Selkeä rakenne on kartta: uusi kehittäjä osaa arvata, mistä jokin asia löytyy, ilman että kukaan selittää sitä ääneen.

**5. Tekoäly tarvitsee rakennetta yhtä lailla kuin ihminen.** Tekoälyavusteinen koodaus on yleistynyt, ja agentti ei lue ajatuksia — se näkee kansiot, nimet ja rajapinnat. Spagetissa se arvaa. Kerroksissa se osaa seurata kaavaa ja tuottaa koodia, joka sopii muuhun järjestelmään.

**6. Järjestelmän on kestettävä kasvua.** Kymmenen käyttäjän sovellus ja kymmenentuhannen käyttäjän sovellus eivät tarvitse samaa arkkitehtuuria — mutta huono arkkitehtuuri tekee kasvamisesta mahdotonta ilman uudelleenkirjoitusta.

Tyypillinen virhe on ajatella, että arkkitehtuuri on ylimääräistä työtä, joka hidastaa. Todellisuudessa huono arkkitehtuuri vain siirtää hitauden myöhemmäksi — ja korkeampaan hintaan.

### Miksi arkkitehtuuri auttaa tekoälyä ja AI-agentteja

Tekoälyavusteinen koodaus ei poista arkkitehtuurin tarvetta — se korostaa sitä. Agentti ei lue ajatuksia eikä muista aiempia keskusteluja seuraavalla kerralla: se päättelee kontekstin siitä, mitä se näkee juuri nyt — kansiorakenteesta, tiedostonimistä, rajapinnoista ja olemassa olevasta koodista. Selkeässä kerrosrakenteessa agentti löytää oikean paikan uudelle säännölle (esim. "lisää sama tarkistus kuin `RecordResult`-metodissa tekee") ja tuottaa koodia, joka noudattaa muun järjestelmän kaavaa. Spagettikoodissa agentti joutuu arvaamaan, mikä johtaa toistuvaan logiikkaan, vääriin riippuvuuksiin ja koodiin, jota kukaan — ei ihminen eikä agentti — pysty enää selittämään jälkikäteen. Sama pätee katselmointiin ja testaukseen: kun sääntö asuu yhdessä paikassa, sekä ihminen että agentti voivat tarkistaa sen yhdellä katseella, eikä kukaan joudu jäljittämään samaa logiikkaa viidestä eri tiedostosta.

---

## Ohjelmistokehityksen arkkitehtuurihistoria

Ohjelmistoarkkitehtuuri ei syntynyt yhdellä kertaa. Se kertyi sitä mukaa, kun ohjelmat kasvoivat ja alkoivat elää vuosia. Alla sama polku pienin esimerkein.

![Aikajana 1950–2020: kaikki yhdessä, funktiot, kerrokset, yhteinen kieli, säännöt keskelle, pilvi ja putket](images/oa-03-history-timeline.svg)

### 1. Kaikki yhdessä (1950–60)

Ohjelmat olivat pieniä. Yksi ihminen piti kokonaisuuden päässään. Erillistä rakennetta ei tarvittu.

```csharp
// Kaikki samassa paikassa: tarkistus, tallennus, tiedosto, sähköposti
if (kotiId == vierasId)
    return "Sama joukkue kahdesti";

ottelut.Add(uusiOttelu);
File.WriteAllText("ottelut.txt", ...);
LähetäSähköposti("Uusi ottelu luotu");
```

Tämä riittää kymmeneen riviin. Sadassa rivissä et enää tiedä, *missä* sääntö asuu.

### 2. Jaa funktioihin (1970)

Edsger Dijkstra ja **strukturoitu ohjelmointi**: jaa työ funktioihin, vältä `GOTO`-hyppyjä (komento, joka hyppää koodissa mielivaltaiseen kohtaan). Ensimmäinen opetus, joka pätee yhä — *jaa, älä kasaa*.

```csharp
void LuoOttelu(int kotiId, int vierasId)
{
    TarkistaEriJoukkueet(kotiId, vierasId);
    TallennaOttelu(kotiId, vierasId);
}

void TarkistaEriJoukkueet(int kotiId, int vierasId)
{
    if (kotiId == vierasId)
        throw new Exception("Koti ja vieras eivät saa olla sama joukkue.");
}
```

Funktio on pieni palikka. Se ei vielä kerro, *mihin kerrokseen* palikka kuuluu.

### 3. Kerrokset (1980)

**Kerrosarkkitehtuuri** jakaa ohjelman vaakasuoriin kaistoihin. Jokaisella kaistalla on yksi vastuu. Ylempi kerros saa käyttää alempaa. Alempi ei tiedä ylemmästä.

```
Selain / Swagger     ← esitys: HTTP sisään ja ulos
        ↓
Service              ← säännöt: saako tuloksen kirjata?
        ↓
Repository           ← data: hae ja tallenna
```

Sama ajatus näkyy **TCP/IP**-pinossa (verkko jaetaan kerroksiin: sovellus, kuljetus, verkko, siirto) ja vanhoissa tietokantasovelluksissa.

```csharp
// Controller ei päätä sääntöä — se vain vastaanottaa pyynnön
public IActionResult RecordResult(int id, int home, int away)
{
    _matchService.RecordResult(id, home, away);
    return NoContent();
}

// Service päättää: tulos vain kerran
public void RecordResult(int id, int home, int away)
{
    var match = _matches.GetById(id);
    if (match.HomeGoals is not null)
        throw new BusinessRuleException("Tulos on jo kirjattu.");
    _matches.Update(match);
}
```

Kolme kerrosta ja yksi suunta riittää jo pitkälle: se on edelleen yleisin lähtökohta uudelle projektille.

### 4. Yhteinen kieli (1990)

Olio-ohjelmointi yleistyi. Vuonna 1994 *Design Patterns* -kirja antoi nimetyt ratkaisut toistuviin ongelmiin (Singleton, Factory, Observer). Mallit eivät ole arkkitehtuuri itse. Ne tekevät rakenteesta *keskusteltavaa*: "laita se repositoryyn" tarkoittaa tiimissä samaa asiaa kaikille.

### 5. Säännöt keskelle (2000–2010)

Kun ohjelma kasvoi, kerroksetkaan eivät riittäneet, jos sääntö valui silti joka paikkaan. **DDD** (Domain-Driven Design, Eric Evans 2003) kysyi: *mitä liiketoiminta oikeasti kieltää?* **Clean Architecture** (Robert C. Martin, 2010-luku) laittoi säännöt keskelle ja tekniikan (tietokanta, HTTP, sähköposti) ulkokehälle.

```csharp
// Sääntö asuu ottelussa, ei controllerissa eikä SQL-lauseessa
match.RecordResult(homeGoals: 2, awayGoals: 1);
```

Samaan aikaan isot firmat jakoivat järjestelmän **mikropalveluiksi**: monta pientä ohjelmaa, jotka puhuvat verkon yli. Netflixille se oli järkevää. Pienelle tiimille se on usein liian aikaisin.

**CQRS** (Command Query Responsibility Segregation) tarkoittaa: kirjoitus ja luku eri polkua. Esimerkiksi *kirjaa tulos* on komento, *hae sarjataulukko* on kysely — ne voivat käyttää eri malleja ja jopa eri tietolähteitä.

### 6. Järjestelmä on muutakin kuin luokkia (2010–2020)

Pilvi, julkaisuputket ja valvonta tulivat osaksi arkkitehtuuria. "Toimii minun koneella" ei ole enää riittävä totuus. Koodin jako on yksi taso. Missä koodi *ajetaan*, miten se *julkaistaan* ja kuka *saa tehdä mitä* ovat omia tasojaan — näihin siirrytään seuraavaksi.

**Mitä historia opettaa:** seuraava malli syntyi yleensä edellisen kivusta. Kerrokset syntyivät, koska funktiot eivät riittäneet. Clean Architecture syntyi, koska kerroksetkaan eivät estäneet sääntöjen leviämistä. Ei kannata hypätä keskelle ilman että ymmärtää, mitä ongelmaa kukin vaihe ratkaisi.

---

## Arkkitehtuuritasot

Sana *arkkitehtuuri* tarkoittaa eri ihmisille eri asiaa. Backend-kehittäjä ajattelee kerroksia. Joku toinen ajattelee pilvipalveluita. Joku kolmas ajattelee, kuka saa julkaista tuotantoon. **Kaikki ovat oikeita.** Ne vastaavat eri kysymykseen.

Kutsumme näitä **tarkastelutasoiksi**. Sama järjestelmä, eri kysymys.

![Viisi tarkastelutasoa päällekkäin: sovellus, versionhallinta, infra, toimitus ja tuotanto](images/oa-04-architecture-levels.svg)

### 1. Sovellus — miten koodi on jaettu

**Kysymys:** miten yksi ohjelma on sisältä jaettu, ja missä säännöt asuvat?

Tällä tasolla puhutaan siitä, miten yhden ohjelman sisäinen koodi on organisoitu kerroksiin tai projekteihin: mikä osa tietää säännöt, mikä osa puhuu tietokannalle, mikä osa vastaa HTTP-pyyntöön. Tyypillinen ratkaisu on Clean Architecture: keskellä säännöt, ulkona tietokanta ja HTTP.

Ilman tätä tasoa seuraava muutos sattuu jokaiseen tiedostoon. Tietokannan voi vaihtaa vain, jos koodi riippuu *sopimuksesta* (esim. `IMatchRepository`), ei konkreettisesta listasta tai SQL-lauseesta.

### 2. Versionhallinta ja kehitysprosessi — miten koodi muuttuu turvallisesti

**Kysymys:** miten monta kehittäjää voi muokata samaa koodia rikkomatta toistensa työtä, ja miten yksi muutos etenee ideasta hyväksyttyyn koodiin?

**Versionhallinta** (yleisimmin **Git**) tallentaa jokaisen muutoksen historian ja mahdollistaa rinnakkaisen työskentelyn ilman että kukaan ylikirjoittaa toisen työtä. Tähän tasoon kuuluu myös **haarautumisstrategia** (branching strategy): missä järjestyksessä haarat (branches) yhdistetään toisiinsa, ja mikä haara vastaa mitäkin ympäristöä. Yleisiä malleja ovat esim. trunk-based development (kaikki lähellä yhtä päähaaraa) ja GitFlow-tyyliset mallit, joissa on erilliset kehitys- ja julkaisuhaarat.

**Monorepo vs. polyrepo** on rakenteellinen valinta: onko backend, frontend ja infra samassa repositoriossa (monorepo) vai omissa repoissaan (polyrepo)? Monorepo helpottaa muutosten koordinointia usean osan välillä samalla kertaa; polyrepo eristää tiimit ja julkaisusyklit toisistaan paremmin.

**Pull request (PR) -käytäntö** on sääntö siitä, kuka saa yhdistää muutoksen mihinkin haaraan: pakolliset katselmoijat, pakolliset automaattitestit ennen yhdistämistä, ja usein sääntö ettei kukaan — ei edes ylläpitäjä — voi pushata suoraan tuotantohaaraan ilman katselmointia.

Ilman tätä tasoa ainoa suoja virheellistä muutosta vastaan on ihmisen muisti. Haarasuojaus ja PR-pakko tekevät virheestä vaikean, ei vain epätoivottavan.

### 3. Infra ja ympäristöt — missä ohjelma elää

**Kysymys:** millä koneilla kehitys ja tuotanto toistuvat?

**Infra** = infrastruktuuri: koneet, kontit, tietokantapalvelimet. **Docker** paketoi ohjelman ja sen riippuvuudet niin, että sama pino käynnistyy jokaisella koneella. "Toimii minun koneella" ei riitä tiimille.

**Pilvi** tarkoittaa, että ostetaan valmista kapasiteettia (esim. Azure, AWS, Google Cloud) sen sijaan että ylläpidettäisiin omaa palvelinhuonetta. Tyypillisesti tarvitaan kapasiteettia ainakin näihin:

| Mitä tarvitaan | Mitä yleensä ostetaan | Miksi ei koodata itse |
|----------------|------------------------|------------------------|
| HTTP-API | sovelluspalvelu | Oma palvelin ei päivity eikä skaalaudu |
| Selain | staattisen sivun palvelu | Staattinen sivu ilman palvelinviritystä |
| Data | hallittu tietokanta | Varmuuskopio ja palomuuri valmiina |
| Telemetria | valvontapalvelu | Tuotantovirhe ei näy paikallisessa lokissa |

**Ympäristö** on paikka, jossa sama koodi juoksee eri asetuksilla:

| Ympäristö | Missä | Kenelle |
|-----------|-------|---------|
| Local | oma kone | kehittäjä |
| Staging | pilvi, testikäyttö | "toimiiko tämä oikeassa pilvessä?" |
| Prod (production, tuotanto) | pilvi, oikeat käyttäjät | ei kokeiluja ilman lupaa |

Pilveen voi julkaista myös spagetin. Ostettu palvelu ei korvaa kerroksia — se tekee sotkusta kalliimman.

### 4. Toimitus — miten muutos pääsee käyttäjille

**Kysymys:** miten ympäristö luodaan uudelleen, ja miten koodi pääsee laptopilta tuotantoon ilman toivoa?

**IaC** (Infrastructure as Code) tarkoittaa, että pilven asetukset ovat tiedostoja, ei klikkailua portaalissa. Sama ympäristö voidaan tuottaa uudelleen samoista tiedostoista.

**CI/CD** (Continuous Integration / Continuous Delivery):

- **CI** = jokainen muutos käännetään ja testataan automaattisesti
- **CD** = hyväksytty muutos voidaan julkaista automaattisesti tai napista

Tyypillisesti tämä toteutetaan työkaluputkina (esim. GitHub Actions): testit jokaisesta **PR**:stä (pull request, ehdotus yhdistää haara), staging automaattisesti, tuotanto vain kun ihminen hyväksyy. **OIDC** (OpenID Connect) on tapa kirjautua pilveen ilman että salainen avain makaa repossa.

Ilman putkea ainoa totuus on laptop. Rikkinäinen tuotanto jää huomaamatta. Sääntö *kuka saa julkaista* on arkkitehtuuria yhtä lailla kuin kerrosjako.

### 5. Tuotanto — näkyvyys ja luottamus

**Kysymys:** mistä tiedät että järjestelmä on rikki, ja kuka saa tehdä mitä?

**Havainnointi** (observability): logit ja hälytykset. Et voi korjata sitä mitä et näe.

**Turvallisuus:** kuka saa kirjata tuloksen? Missä salaisuudet asuvat? Tyypillinen ratkaisu on sähköpostikoodi ja **JWT** (JSON Web Token, allekirjoitettu "lupalappu" jonka API tarkistaa). Salaisuus repossa on arkkitehtuurivirhe, ei unohdus.

---

## Esimerkkinä: MyLeague

[MyLeague](https://github.com/xamkfi/myleague-app) on Xamkin julkinen, oikeasti tuotannossa toimiva sovellus, joka hallinnoi harrastesarjoja. Se hallinnoi kolmea lajia — salibandylla ja jalkapallolla on täysi julkinen käyttöliittymä, jääkiekolla on koko backend ja testidata mutta ei vielä julkista näkymää. Sovellus kattaa seurat, joukkueet, ottelut, live-tulokset, tilastot, uutiset ja kirjautumisen ilman salasanaa (koodi sähköpostiin).

![MyLeague tuotannossa: ottelunäkymä Pöyryn Pantterit–Joukkue, tulos 3–2](images/oa-05-myleague-ui.png)

Katsotaan, miten samat asiat — mitä arkkitehtuuri on, miksi se on tärkeää, mistä ratkaisut ovat peräisin historiallisesti, ja miten tarkastelutasot näkyvät — konkretisoituvat yhdessä oikeassa tuotteessa.

### Arkkitehtuuri MyLeaguessa: rakenne

MyLeaguen palvelinpuoli on jaettu neljään Clean Architecture -projektiin:

- **Domain** — entiteetit, arvo-oliot, repository-sopimukset. Ei riipu mistään muusta kerroksesta.
- **Application** — CQRS-komennot ja -kyselyt MediatR-kirjastolla, jaettuna laji­kohtaisiin "feature slice" -kansioihin: Auth, Common, Floorball, Football, Hockey.
- **Infrastructure** — EF Core, autentikointi, kuvat, SignalR.
- **WebAPI** — controllerit, middleware, OpenAPI.

Riippuvuudet osoittavat sisäänpäin: Domain ei tiedä mistään ulkopuolisesta.

![MyLeaguen neljä kerrosta: Presentation, Application, Infrastructure ja Domain, riippuvuudet alaspäin](images/oa-06-myleague-layers.svg)

Selain on React + TypeScript (Vite). Data on **PostgreSQL**-tietokanta. Kausien ja turnausten yhteinen `*Competition`-kantaluokka ja EF Core:n Table-Per-Hierarchy-mallinnus pitävät saman `competitionId`:n sekä sarjakausille että turnauksille — konkreettinen esimerkki siitä, miten rakenteellinen päätös (yksi yhteinen kantaluokka) tekee myöhemmästä laajennuksesta halvempaa.

### Miksi se on tärkeää MyLeaguelle

MyLeague on oikeassa käytössä useamman lajin ja tuhansien käyttäjien kanssa, joten arkkitehtuurin hyödyt eivät ole teoreettisia:

- **Feature slice -rakenne** (Floorball, Football, Hockey omina kansioinaan) tarkoittaa, että jääkiekon lisääminen ei sotkenut salibandyn koodia — uusi laji lisättiin omaan siiloonsa samaa kaavaa noudattaen.
- **Automaattiset smoke-testit** jokaisen julkaisun jälkeen (ks. Toimitus alla) tarkoittavat, että rikkinäinen julkaisu huomataan minuuteissa, ei siinä vaiheessa kun käyttäjä valittaa.
- **Hälytykset** (ks. Tuotanto alla) tarkoittavat, että kehittäjätiimi tietää palvelimen kaatumisesta ennen käyttäjiä.
- **Yksi App Service -instanssi tarkoituksella:** SignalR käyttää muistinvaraista tilaa, joten arkkitehtuuripäätös (ei skaalata vielä useammalle instanssille) on tietoinen valinta, joka vältti tarpeettoman monimutkaisuuden (Redis-taustan) ennen kuin sille oli oikeasti tarvetta.

### Mistä ratkaisut ovat peräisin: historia näkyy koodissa

MyLeaguen arkkitehtuuri ei ole yhden vaiheen ratkaisu, vaan yhdistelmä useasta historiallisesta kerroksesta:

- **Kerrokset (1980-luku):** Presentation → Application → Infrastructure → Domain on suoraan sama nelivaiheinen kerrosajattelu.
- **Yhteinen kieli (1990-luku):** komennot, kyselyt, handlerit ja DTO:t ovat nimettyjä, tunnistettavia malleja — ei omia keksittyjä ratkaisuja.
- **Säännöt keskelle (2000–2010):** Clean Architecture -projektijako ja Domain-kerroksen entiteetit (esim. `Competition`-kantaluokka) noudattavat DDD-henkistä ajattelua — sääntö asuu oliossa, ei controllerissa.
- **CQRS:** MediatR erottaa kirjoitus- ja lukupolut jo rakenteen tasolla — komennot ja kyselyt eivät jaa samaa koodipolkua.
- **Pilvi ja putket (2010–2020):** Docker paikalliskehitykseen, Azure tuotantoon, GitHub Actions -putki julkaisuun — järjestelmä on muutakin kuin luokkia.

### Tasot käytännössä

**Sovellus.** Katettu edellä: Domain / Application / Infrastructure / WebAPI, CQRS + MediatR, PostgreSQL.

![Kerrosjako rinnastettuna tarkastelutasoihin: Clean Architecture on Sovellus-tason toteutus](images/oa-07-layers-vs-levels.svg)

**Versionhallinta ja kehitysprosessi.** MyLeague on **monorepo**: backend, frontend, testit ja infra-tiedostot ovat kaikki samassa repositoriossa (`src/backend`, `src/frontend`, `tests/backend`, `infra/`) — muutos, joka koskee sekä API:a että käyttöliittymää, voidaan tehdä ja katselmoida yhtenä kokonaisuutena.

Julkaisupolku on kaksivaiheinen: ominaisuushaara → PR `development`-haaraan → PR `development`-haarasta `master`-haaraan. Tätä valvotaan koodilla, ei vain sopimuksella:

- `protect-master.yml`-työnkulku hylkää PR:n `master`iin automaattisesti, ellei se tule `development`-haarasta.
- Haarasuojaussäännöt `master`-haaralle: pakotusten esto (force push), poiston esto, rajattu suoran pushin oikeus (vain organisaation ylläpitäjät tai ei kukaan), pakollinen PR ennen yhdistämistä, ja pakolliset tilatarkistukset (`PR must come from development`, Backend/Frontend CI:n `Build and Test`).
- Halutessaan sääntö voidaan asettaa koskemaan myös ylläpitäjiä — ei "admin bypass" -oikeutta edes heille.

Tämä on konkreettinen esimerkki siitä, että sääntö *kuka saa muuttaa mitäkin ja missä järjestyksessä* on yhtä lailla arkkitehtuuria kuin kerrosjako — se on vain kirjoitettu Git-työkalujen sääntöinä koodin sisältä sen sijaan että se elää dokumentissa.

**Infra ja ympäristöt.** MyLeague nousee paikallisesti komennolla `docker compose up` — Postgres, Seq (lokien katselu), API ja frontend samassa pinossa, maksaa 0 €. Tietoisesti **ei ole** erillistä pilvi-dev-ympäristöä: paikallinen Docker riittää siihen tarkoitukseen.

Pilvenä käytetään Azurea, kaksi ympäristöä kumpikin omassa resurssiryhmässään:

| Mitä tarvitaan | Mitä ostetaan | Miksi ei koodata itse |
|----------------|---------------|------------------------|
| HTTP-API | App Service (Basic B1, Linux) | Oma palvelin ei päivity eikä skaalaudu |
| Selain | Static Web App (ilmainen taso) | Staattinen sivu ilman palvelinviritystä |
| Data | PostgreSQL Flexible Server (Burstable B1ms) | Varmuuskopio ja palomuuri valmiina |
| Kuvat | Storage Account | Ei tarvitse rakentaa omaa tiedostopalvelinta |
| Sähköposti | Azure Communication Services | Kirjautumiskoodi ulos ilman omaa SMTP:tä |
| Telemetria | Application Insights + Log Analytics | Tuotantovirhe ei näy paikallisessa lokissa |

| Ympäristö | Missä | Kenelle | Kuukausihinta |
|-----------|-------|---------|----------------|
| Local | oma kone (`docker compose up`) | kehittäjä | 0 € |
| Staging | Azure, `myleague-staging-rg`, auto-deploy `development`-haarasta | "toimiiko tämä oikeassa pilvessä?" | ~26 $ |
| Prod (production, tuotanto) | Azure, `myleague-prod-rg`, manuaalinen julkaisu | ei kokeiluja ilman lupaa | ~27 $ |

Budjettihälytys laukeaa 80 %:ssa 35 $:n kuukausikatosta per resurssiryhmä.

![Kolme ympäristöä: Local 0 €, Staging ~26 $, Prod ~27 $, julkaisuvirta vasemmalta oikealle](images/oa-08-environments.svg)

**Toimitus.** Pilven asetukset on kirjoitettu Biceppinä (IaC-kieli): erilliset moduulit App Service Plan-, App Service-, PostgreSQL-, Static Web App-, Storage- ja monitorointiresursseille. Kaksi ympäristöä syntyvät samoista Bicep-tiedostoista eri parametritiedostoilla.

CI/CD on toteutettu GitHub Actions -työtiedostoina:

| Workflow | Mitä tekee |
|----------|------------|
| `backend-ci.yaml` / `frontend-ci.yaml` | Build, testit, lint jokaisesta PR:stä `master`- ja `development`-haaroihin |
| `protect-master.yml` | Estää suoran PR:n `master`iin, ellei se tule `development`-haarasta |
| `infra-deploy.yml` | Bicep-provisiointi OIDC:llä — staging automaattisesti, prod vain manuaalisesti hyväksyjien kautta |
| `deploy-backend.yml` / `deploy-frontend.yml` | Sovelluksen julkaisu + smoke-testit |

Jokaisen backend-julkaisun jälkeen smoke-testi kutsuu oikeaa ympäristöä: terveystarkastus, muutama julkinen luku-endpoint, tarkistus että suojattu endpoint palauttaa 401 ilman tokenia, ja tuntematon reitti palauttaa 404. Jos jokin epäonnistuu, koko julkaisu merkitään epäonnistuneeksi heti.

OIDC (federoidut tunnistetiedot Entra ID:hen) hoitaa kirjautumisen Azureen ilman että pitkäikäinen salaisuus makaa repossa tai GitHub-secretissä. Vain `prod`-ympäristöllä on pakolliset hyväksyjät GitHubissa — `staging` julkaisee ilman ihmisen väliintuloa.

![CI/CD-putki: push, CI, staging, hyväksyntä ja tuotanto](images/oa-09-cicd-pipeline.svg)

**Tuotanto.** Kirjautuminen on sähköpostikoodi ja JWT (15 min access token, 7 vrk refresh token tuotannossa; refresh-tokenin uudelleenkäyttö perumisen jälkeen perii kaikki kyseisen käyttäjän tokenit).

Havainnointi hoidetaan Application Insightsilla ja Log Analyticsilla (30 vrk säilytys, 1 Gt/vrk katto). Hälytyksiä on useita tasoja vakavuuden mukaan, esimerkiksi:

| Hälytys | Kynnys | Vakavuus |
|---------|--------|----------|
| Terveystarkastus epäonnistuu | alle 100, 5 min | 1 (kriittinen) |
| Sivusto ei vastaa (vain prod) | 2+ sijaintia epäonnistuu | 1 (kriittinen) |
| Tietokannan levytila täyttymässä | yli 80 % | 1 (kriittinen) |
| HTTP 5xx -piikki | yli 10 / 5 min | 2 |
| Hidas vasteaika | keskiarvo yli 5 s / 15 min | 3 |

Kaikki hälytykset menevät sähköpostiin jaetun toimintaryhmän kautta. Tämä on se taso, joka erottaa "toimii kehittäjän koneella" -kokeilun tuotantovalmiista järjestelmästä.

---

## Yhteenveto

Viisi tarkastelutasoa — Sovellus, Versionhallinta ja kehitysprosessi, Infra ja ympäristöt, Toimitus, Tuotanto — vastaavat viiteen eri kysymykseen samasta järjestelmästä. MyLeague näyttää, että kaikki viisi tasoa ovat todellisia päätöksiä, ei teoriaa: feature-slice-rakenne, koodilla valvottu haarasuojaus, kaksi Azure-ympäristöä tunnetulla kuukausihinnalla, automaattinen julkaisuputki smoke-testeineen, ja hälytykset jotka herättävät ihmisen ennen käyttäjää. Sama historia — kerroksista sääntöihin keskelle ja pilveen — näkyy jokaisessa niistä.

---

## Lyhenteet

| Lyhenne | Auki | Selitys |
|---------|------|---------|
| IEEE | Institute of Electrical and Electronics Engineers | Kansainvälinen tekniikan standardijärjestö, määritteli arkkitehtuurin käsitteen |
| API | Application Programming Interface | HTTP-rajapinta, esim. Swagger |
| HTTP | Hypertext Transfer Protocol | Selain ↔ palvelin -protokolla |
| DDD | Domain-Driven Design | Säännöt keskelle, tekniikka ulkokehälle |
| CQRS | Command Query Responsibility Segregation | Kirjoitus ja luku eri polkua |
| DTO | Data Transfer Object | Kapea tietue, jonka API lähettää ulos |
| CI/CD | Continuous Integration / Continuous Delivery | Automaattinen testaus ja julkaisu |
| IaC | Infrastructure as Code | Pilven asetukset tiedostoina |
| JWT | JSON Web Token | Allekirjoitettu "lupalappu", jonka API tarkistaa |
| PR | Pull Request | GitHub: ehdotus yhdistää haara |
| SQL | Structured Query Language | Tietokannan kyselykieli |
| OIDC | OpenID Connect | Tapa kirjautua pilveen ilman pitkäikäistä salaisuutta |

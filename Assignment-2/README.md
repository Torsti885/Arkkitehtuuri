# Assignment 2: Refaktoroi spagetti kerroksiin

Tämä on **kerran 1 toinen harjoitus**. [Assignment 1](../Assignment-1/README.md) ohjasi LeagueHubin kerroksiin askel askeleelta. Nyt sama liike **ilman valmista reittiä**: spagetti on valmiina, sinä siirrät koodin oikeisiin kerroksiin.

> Tätä tehtävää **ei palauteta**.

---

## Tavoite

Harjoitella, *mihin mikäkin koodi kuuluu*. Etsi säännöt, HTTP-vastaukset ja data, ja sijoita ne kerroksiin kuten tehtävässä 1.

---

## Mitä tämä ohjelma tekee?

**Lainaamo** on kampuksen välinehuoneen API. Henkilökunta lainaa välineitä opiskelijoille ja merkitsee palautuksen.

| Reitti | Mitä tapahtuu |
|--------|----------------|
| `GET /api/items` | lista välineistä |
| `POST /api/items` | uusi väline (nimi pakollinen) |
| `GET /api/loans` | lista lainoista |
| `POST /api/loans` | lainaa (`itemId`, `borrowerName`) |
| `POST /api/loans/{id}/return` | palauta |

| Sääntö | Spagetissa nyt |
|--------|----------------|
| Välineen nimi ei tyhjä | `CreateItem` |
| Välinettä ei voi lainata, jos sillä on avoin laina (`ReturnedAt == null`) | `Borrow` |
| Palautus vain avoimelle lainalle | `ReturnLoan` |
| Välineen pitää olla olemassa | `Borrow` |

---

## Lähtö

Koodi on tässä paketissa valmiina:

`starter/Lainaamo/`

```bash
cd starter/Lainaamo
dotnet run
```

Swaggerissa kokeile:

- `GET /api/items` — kolme välinettä
- `GET /api/loans` — yksi avoin laina, yksi palautettu
- lainaa projektoria uudestaan → 400
- palauta avoin laina → 200
- palauta sama laina uudestaan → 400

Refaktoroi tätä projektia. Jos haluat pitää alkuperäisen spagetin vertailua varten, kopioi kansio ensin.

---

## Tehtävä

Muuta Lainaamo kerrosarkkitehtuuriin. Käyttäjän näkemä API ei saa muuttua: samat reitit, samat statuskoodit 200 / 400 / 404.

Tee ainakin nämä:

1. Kansiot `Models`, `Repositories` ja `Services` (ja poikkeukset, jos käytät niitä kuten tehtävässä 1).
2. Controller hoitaa vain HTTP:n: statuskoodit ja bodyn. Siinä ei ole sääntöjä, kuten `if (loan.ReturnedAt is not null)`.
3. Säännöt asuvat Servicessä.
4. Välineet ja lainat asuvat Repositoryssa, ei controllerissa. Service riippuu **rajapinnasta** (`ILoanRepository`), ei valmiista `InMemory…`-luokasta.
5. Rekisteröi riippuvuudet `Program.cs`:ssä. In-memory-repositoryt **Singleton** (data säilyy pyyntöjen yli), servicet **Scoped**.

Valinnaisena yksi yksikkötesti: avointa välinettä ei voi lainata kahdesti. Testaa Serviceä fake-repositorylla, ilman HTTP-pyyntöä.

---

## Valmis, kun

- Swaggerilla sama polku kuin spagetissa toimii.
- `LainaamoController` on poissa tai tyhjä — työ on jaettu kerroksiin.
- Osaat näyttää, *miksi tämä rivi oli sääntö eikä jäänyt controlleriin*.

---

<details>
<summary>Vinkit (avaa jos jumitat)</summary>

**Mihin mikäkin rivi.** Käy `LainaamoController` rivi riviltä. `return BadRequest(...)` jää controlleriin, koska se on HTTP-vastaus. `if (string.IsNullOrWhiteSpace(item.Name))` on sääntö → Service. `_loans.FirstOrDefault(...)` on haku → Repository.

**Älä laita repositoryyn** metodia `IsItemAlreadyBorrowed`. Repository palauttaa lainat; Service katsoo, onko avointa lainaa (`ReturnedAt is null`). Sama ajatus kuin `IMatchRepository` ilman metodia `IsResultAlreadyRecorded`.

**Kaksi serviceä on ok.** `ItemService` (nimi pakollinen) ja `LoanService` (lainaa / palauta). `LoanService` tarvitsee sekä `IItemRepositoryn` että `ILoanRepositoryn`, jotta se tietää että väline on olemassa.

**Poikkeukset.** Tehtävässä 1 Service heitti `BusinessRuleException`in tai `NotFoundException`in, ja controller muutti ne vastauksiksi `400` / `404`. Sama malli toimii tässä. Service ei palauta `IActionResult`ia — se ei tiedä HTTP:stä.

**DI.** `AddSingleton` repositoryille: data on muistissa, olion pitää elää pyyntöjen yli. `AddScoped` serviceille. Jos repository on Scoped, seuraava GET ei näe äsken tehtyä lainaa.

**Testi.** `new LoanService(fakeItems, fakeLoans)`. Lisää väline ja avoin laina fakeen. Toinen `Borrow` samalle `itemId`:lle → `BusinessRuleException`. Älä käynnistä koko web-sovellusta testissä.

**Piirrä ensin.** Kolme kerrosta, nuolet alaspäin. Sijoita `POST /api/loans` ja `POST /api/loans/1/return` ennen kuin siirrät koodia.

</details>

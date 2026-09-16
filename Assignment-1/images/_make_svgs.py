"""Tehtävä 1 -diagrammit (LeagueHub). Aja kerran; SVG:t commitoitaan."""
from pathlib import Path

OUT = Path(__file__).parent
FONT = "Segoe UI, Calibri, sans-serif"

HEAD = """<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
  <rect width="{w}" height="{h}" fill="#f7f5f2"/>
  <text x="24" y="36" font-family="FONT" font-size="20" font-weight="700" fill="#1d3557">{title}</text>
""".replace("FONT", FONT)
FOOT = "</svg>\n"
DEFS = """
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#1d3557"/>
    </marker>
  </defs>
"""


def txt(x, y, s, size=13, fill="#1d3557", weight=None):
    w = f' font-weight="{weight}"' if weight else ""
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{fill}"{w}>{s}</text>'


def box(x, y, w, h, fill, stroke, title, lines, title_fill="#ffffff"):
    parts = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="2"/>',
        txt(x + 16, y + 28, title, 16, title_fill, 700),
    ]
    for i, line in enumerate(lines):
        parts.append(txt(x + 16, y + 52 + i * 20, line, 13, title_fill))
    return "\n  ".join(parts)


def write(name, w, h, title, body):
    (OUT / name).write_text(HEAD.format(w=w, h=h, title=title) + DEFS + body + FOOT, encoding="utf-8")
    print("wrote", name)


write("01-eventhub-overview.svg", 960, 400, "Mitä rakennamme: LeagueHub", f"""
  {box(40, 70, 280, 200, "#1d3557", "#1d3557", "Joukkueet", ["Nimi, kaupunki, maxRoster", "GET/POST /api/teams"])}
  {box(340, 70, 280, 200, "#457b9d", "#457b9d", "Ottelut", ["Koti, vieras, ajankohta", "Tulos kerran", "POST .../result"])}
  {box(640, 70, 280, 200, "#e07a5f", "#9b2226", "Säännöt", ["Kaksi eri joukkuetta", "Tulos vain jos ohi", "Ei toista tulosta"], "#1d3557")}
  {txt(40, 310, "Sama tuote koko kurssin: ensin API, myöhemmin Clean Architecture, CQRS ja selain.", 15)}
  {txt(40, 340, "Sarjataulukko lasketaan otteluista — siksi säännöt eivät saa hajota controllereihin.", 14, "#457b9d")}
""")

write("02-spaghetti.svg", 960, 400, "Spagetti: kaikki yhdessä controllerissa", f"""
  {box(200, 70, 560, 240, "#fff1ee", "#c1121f", "LeagueController.cs", [
      "HTTP-statuskoodit",
      "Validointi (nimi, maxRoster)",
      "Säännöt (eri joukkue, tulos kerran)",
      "Data: static List Team ja Match",
  ], "#1d3557")}
  {txt(40, 350, "Toimii Swaggerissa — mutta yksi tiedosto tekee viittä työtä (SRP rikki).", 15, "#c1121f")}
""")

write("03-spaghetti-pain.svg", 960, 400, "Sama sääntö kolmessa paikassa", f"""
  {box(40, 80, 280, 200, "#fff1ee", "#c1121f", "RecordResult()", ["hae ottelu", "onko tulos jo?", "onko ajankohta ohi?"], "#1d3557")}
  {box(340, 80, 280, 200, "#fff1ee", "#c1121f", "GetStandings()", ["hae ottelut", "laske pisteet", "ohita perutut?"], "#1d3557")}
  {box(640, 80, 280, 200, "#fff1ee", "#c1121f", "CancelMatch()", ["hae ottelu", "onko alkanut?", "onko tulos?"], "#1d3557")}
  {txt(40, 330, "Asiakas: perua saa vain ennen alkua. Kolme korjauspaikkaa.", 16, "#c1121f")}
""")

write("04-layers.svg", 960, 500, "Kerrosarkkitehtuuri: yksi vastuu per kerros", f"""
  {box(80, 70, 800, 100, "#1d3557", "#1d3557", "PRESENTATION  —  Controllers/", ["HTTP sisään, statuskoodit ulos. Ei sääntöjä."])}
  <line x1="480" y1="170" x2="480" y2="196" stroke="#1d3557" stroke-width="2" marker-end="url(#arrow)"/>
  {box(80, 200, 800, 100, "#457b9d", "#457b9d", "BUSINESS  —  Services/", ["Säännöt ja sarjataulukon laskenta. Ei HTTP:tä, ei listoja."])}
  <line x1="480" y1="300" x2="480" y2="326" stroke="#1d3557" stroke-width="2" marker-end="url(#arrow)"/>
  {box(80, 330, 800, 100, "#2a9d8f", "#1d3557", "DATA  —  Repositories/", ["Haku ja tallennus. Nyt lista, kerralla 2 tietokanta."])}
  {txt(80, 460, "Riippuvuudet vain alaspäin. Kytkentä rajapinnoilla (IMatchRepository).", 14)}
""")

write("05-request-flow.svg", 960, 380, "POST /api/matches/1/result", f"""
  {box(30, 80, 200, 160, "#e9edc9", "#606c38", "1. HTTP", ["Swagger", "homeGoals, awayGoals"], "#1d3557")}
  {box(250, 80, 200, 160, "#1d3557", "#1d3557", "2. Controller", ["Ottaa pyynnön", "Kutsuu Serviceä", "400 / 404 / 200"])}
  {box(470, 80, 220, 160, "#457b9d", "#457b9d", "3. Service", ["Tulos jo?", "Ajankohta ohi?", "Kaksi eri joukkuetta"])}
  {box(710, 80, 220, 160, "#2a9d8f", "#1d3557", "4. Repository", ["GetById", "Update", "Ei sääntöjä"])}
  {txt(30, 290, "Count kuuluu repositoryyn. ”tulos jo kirjattu” kuuluu Serviceen.", 14, "#457b9d")}
""")

write("06-code-mapping.svg", 960, 360, "Mihin mikäkin koodi muuttaa", f"""
  {txt(80, 80, "Spagetissa", 14, "#c1121f", 700)}
  {txt(520, 80, "Kerroksissa", 14, "#2a9d8f", 700)}
  {txt(56, 130, "_matches.FirstOrDefault(...)", 13)}
  {txt(536, 130, "Repository", 15)}
  {txt(56, 180, "homeTeamId == awayTeamId", 13)}
  {txt(536, 180, "Service", 15)}
  {txt(56, 230, "return BadRequest(...)", 13)}
  {txt(536, 230, "Controller", 15)}
  {txt(56, 280, "static List&lt;Match&gt;", 13)}
  {txt(536, 280, "Repositoryn sisään", 15)}
""")

write("07-di-lifetimes.svg", 960, 400, "DI-elinkaaret LeagueHubissa", f"""
  {box(40, 70, 430, 180, "#1d3557", "#1d3557", "Singleton — repositoryt", ["Yksi olio koko ajan.", "Data elää muistissa."])}
  {box(490, 70, 430, 180, "#457b9d", "#457b9d", "Scoped — servicet", ["Uusi olio per HTTP-pyyntö.", "Kerralla 2 DbContext on Scoped."])}
  {txt(40, 290, "Kokeile: vaihda repositoryt AddScoped ja kirjaa tulos. Seuraava GET on tyhjä — uusi lista.", 14)}
""")

write("08-tests-without-http.svg", 960, 400, "Sääntötesti ilman HTTP:tä", f"""
  {box(40, 70, 400, 250, "#fff1ee", "#c1121f", "Spagetti — ei onnistu", ["Sääntö on IActionResultissa", "Data private static -listassa", "Testi vaatisi HTTP:n", "Testit sotkevat toistensa datan"], "#1d3557")}
  {box(520, 70, 400, 250, "#e9f5f3", "#2a9d8f", "Kerrokset — onnistuu", ["MatchService on tavallinen luokka", "Fake toteuttaa IMatchRepositoryn", "new MatchService(fakes)", "dotnet test, ei porttia"], "#1d3557")}
""")

write("09-folder-structure.svg", 960, 400, "Rakenne refaktoroinnin jälkeen", f"""
  {box(40, 70, 280, 280, "#1d3557", "#1d3557", "Controllers/", ["TeamsController", "MatchesController", "HTTP ↔ status"])}
  {box(340, 70, 280, 280, "#457b9d", "#457b9d", "Services/", ["TeamService", "MatchService", "Säännöt + standings"])}
  {box(640, 70, 280, 280, "#2a9d8f", "#1d3557", "Repositories/", ["InMemory…", "Listat täällä"])}
""")

print("done")

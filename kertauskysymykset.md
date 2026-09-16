# Kertauskysymykset — Kerrosarkkitehtuuri

Näitä **ei palauteta**. Käy läpi sen jälkeen kun ohjattu osio on tehty.

---

## Kerrosarkkitehtuuri

1. Nimeä kolme kerrosta ja kunkin vastuu.

2. Mihin suuntaan riippuvuudet kulkevat? Saako Repository kutsua Serviceä?

3. Käy läpi, mitä tapahtuu kun `POST /api/matches/1/result` kutsu saapuu.

4. Mihin kerrokseen kuuluvat: (a) `return NotFound(...)` (b) `if (match.HomeGoals is not null)` (c) `_matches.FirstOrDefault(...)`?

5. Miksi `IMatchRepositoryssa` ei ole metodia `IsResultAlreadyRecorded`?

## SOLID ja DI

6. Mitä **SRP** tarkoittaa? Miten `LeagueController` rikkoi sitä?

7. Mitä **DIP** tarkoittaa? Kaksi hyötyä siitä, että `MatchService` riippuu `IMatchRepositorysta`.

8. Mitä konstruktori-injektio tarkoittaa?

9. Miksi in-memory-repositoryt rekisteröidään **Singletonina**? Mitä tapahtuu, jos ne ovat **Scoped**?

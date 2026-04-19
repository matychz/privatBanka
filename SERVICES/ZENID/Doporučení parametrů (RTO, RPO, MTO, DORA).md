### Doporučení optimálních parametrů (RTO, RPO, MTO, DORA) – ZenID (Trask)

Tento dokument shrnuje doporučení pro technické a regulatorní parametry smlouvy k řešení ZenID, které je pro banku **kritickou ICT službou** (umožňuje onboarding klientů).

---

#### 1. RTO (Recovery Time Objective) – Cíl doby obnovy
*   **Návrh Trasku:** 12 hodin.
*   **DOPORUČENÍ:** **2 až 4 hodiny.**
*   **Odůvodnění:** 12 hodin je pro moderní SaaS (Software as a Service) postavený v cloudovém HA (High Availability) režimu nepřiměřeně mnoho. U kritického procesu onboardingu výpadek delší než 4 hodiny (půlka pracovního dne) znamená hmatatelnou ztrátu obchodních příležitostí a poškození reputace „digitální banky“.

#### 2. RPO (Recovery Point Objective) – Cíl bodu obnovy
*   **Návrh Trasku:** 6 hodin.
*   **DOPORUČENÍ:** **Maximálně 1 hodina.**
*   **Odůvodnění:** Ztráta dat z registrací rozpracovaných za posledních 6 hodin je pro banku vysoce riziková. Pokud by se jednalo pouze o technické logy, které banka stahuje v reálném čase, může být parametr volnější, ale u byznys dat (doklady, biometrie, formuláře) je 6 hodin neakceptovatelných. Optimální by byla replikace v reálném čase (RPO blížící se nule).

#### 3. MTO (Maximum Tolerable Downtime) – Max. doba výpadku
*   **Stav:** Trask odmítá definovat.
*   **DOPORUČENÍ:** **8 až 12 hodin.**
*   **Odůvodnění:** Banka musí mít jasný strop, přes který „nejede vlak“ (deadline pro aktivaci alternativního procesu nebo krizového scénáře). DORA vyžaduje, aby u kritických služeb byla stanovena hranice, po jejímž překročení je ohrožena kontinuita podnikání banky.

#### 4. DORA Compliance (Klíčové požadavky)
Pro splnění regulatorních požadavků DORA u kritického dodavatele doporučujeme trvat na:

*   **Auditní práva:** Smlouva nesmí omezovat audit na fixní počet dní (např. 1 MD zdarma). Banka a regulátor (ČNB/NBS) musí mít právo na audit v plném rozsahu, pokud je to nutné.
*   **Exit Plán:** Musí existovat konkrétní scénář pro přechod k jinému dodavateli (včetně exportu dat v otevřených formátech). Argument Trasku, že „data jsou v PB“, je nedostatečný – exit plán musí řešit i to, jak rychle banka dokáže integrovat jiné řešení (pokud Trask zkrachuje nebo službu vypne).
*   **Subdodavatelský řetězec:** Banka musí mít právo veta u změn subdodavatelů, kteří se podílejí na kritických funkcích služby.
*   **Testování kontinuity:** Minimálně jednou ročně musí proběhnout společný test obnovy po havárii (DR Test), nikoliv jen prohlášení dodavatele.

#### 5. Podpora (SLA)
*   **Stav:** Navrženo 5x8 (09:00–17:00).
*   **DOPORUČENÍ:** Pro **Prioritu A** (totální výpadek onboardingu) trvat na režimu **24/7 (nebo aspoň 12/7)**.
*   **Odůvodnění:** Klienti si chtějí účty zakládat i večer a o víkendech. Pokud systém v sobotu ráno spadne a support začne řešit až v pondělí v 9:00, bude banka celý víkend mimo provoz, což je pro moderní retailový produkt neakceptovatelné.

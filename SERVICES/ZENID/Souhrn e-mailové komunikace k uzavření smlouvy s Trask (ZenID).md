### Souhrn e-mailové komunikace k uzavření smlouvy s Trask (ZenID)

Na základě analýzy e-mailového vlákna v souboru `SERVICES/ZENID/smlouva Trusk.md` (datovaného od 31. března do 16. dubna 2026) uvádím souhrn klíčových bodů a aktuálního stavu vyjednávání:

#### 1. Právní a obchodní podmínky
*   **Smluvní strana:** Trask akceptoval, že smlouva bude uzavřena s **Privatbankou SK**. Do budoucna se zvažuje přistoupení české entity ke smlouvě.
*   **Délka smlouvy a cena:** Trask souhlasí s **tříletou fixací ceny**, ale požaduje, aby v takovém případě **nebyla možnost předčasného ukončení** smlouvy výpovědí z jedné či druhé strany.
*   **Odpovědnost za škodu:** Trask trvá na limitu **12 měsíčních plateb** (cca 1 mil. CZK). Navýšení limitu by podle nich znamenalo nutnost rekalkulace (zvýšení) ceny.

#### 2. IT Security a DORA (Regulace)
*   **Audit:** Trask omezuje rozsah součinnosti při auditu (nad 1 MD si účtuje náklady). Banka (IT SEC) má pochybnost, zda je to plnohodnotný DORA režim.
*   **Exit plán:** Trask jej nepovažuje za nutný, protože data persistují v systémech banky. Banka (Tomáš Hanuš) na exit plánu trvá kvůli kritičnosti služby pro onboarding a regulatorním požadavkům.
*   **Subdodavatelé:** Trask revidoval DORA dodatek a věří, že požadavky na transparentnost a kontrolu subdodavatelského řetězce jsou splněny v kombinaci s hlavní smlouvou.

#### 3. Technické parametry (SLA a Disaster Recovery)
Zde probíhá intenzivní interní diskuse v bance (Tomáš Hanuš, Marie Koflák):
*   **Support 5x8 (09:00–17:00):** Trask nabízí tento režim i pro Prioritu A. Tomáš Hanuš to považuje za akceptovatelné jen v případě, že tomu odpovídá i interní provozní režim banky (aby se neplatilo za SLA, které banka nevyužije).
*   **RTO/RPO:** Trask navrhl **RTO 12h** a **RPO 6h**.
    *   **RTO 12h:** Tomáš Hanuš považuje za příliš dlouhé na to, že jde o cloudové SaaS řešení, které mělo být by-design odolné a automatizované.
    *   **RPO 6h:** Je třeba ujasnit, o jaká konkrétní data by banka přišla (pravděpodobně logy a auditní záznamy).
*   **MTO (Max. Tolerable Downtime):** Trask odmítá definovat. Banka na definici trvá kvůli splnění požadavků DORA pro kritické ICT služby (regulátor očekává strop pro výpadek).
*   **Zálohy:** Banka požaduje jasné smluvní ošetření dělby odpovědnosti (co zálohuje Trask a co banka) a testování obnovy.

#### Aktuální stav k 16. 4. 2026
Smlouva je v pokročilé fázi, ale zbývá dořešit technické a regulatorní body (SLA, RTO/RPO, MTO, zálohy). Marie Koflák naplánovala na **16. dubna ve 14:30** interní call se specialisty (Hanuš, Matych), aby sjednotili stanovisko banky pro finální vyjednávání s Traskem.

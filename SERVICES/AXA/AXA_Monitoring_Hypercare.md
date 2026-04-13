# AXA Monitoring & Hypercare Strategie

Tento dokument detailně rozvádí monitorovací postupy pro systém **AXA Core Banking** během "Hypercare" fáze (prvních 30 dní po nasazení do produkce). Cílem je zajistit 100% shodu mezi objednávkami v mobilní aplikaci a reálným zúčtováním v bance.

## 1. Monitorované integrační body

Během Hypercare sledujeme tři hlavní toky, kde AXA figuruje:

| Tok | Typ | Kritický bod | Monitoring tool |
| :--- | :--- | :--- | :--- |
| **Onboarding (MQ)** | Asynchronní | Založení účtu -> Event v MQ -> Zpracování v OL | Elastic (Logy) + MQ Dashboard |
| **Rezervace (Sync)** | Synchronní | `VerifyBalance` + `ReserveFunds` (Blokace) | Elastic (Logy - latency & success rate) |
| **Vypořádání (Settlement)** | Asynchronní | `CommitPayment` (Uvolnění blokace + odpis) | SQL Report (OL vs. AXA) |

## 2. Klíčové metriky pro Hypercare (KPIs)

1.  **Orphaned Blockages (Osiřelé blokace):**
    *   **Definice:** Počet blokací v AXA, ke kterým nebyla do 24 hodin odeslána instrukce `CommitPayment` nebo `CancelReservation`.
    *   **Cíl:** 0 (každá blokace musí být buď zúčtována, nebo zrušena).
2.  **MQ Processing Lag:**
    *   **Definice:** Čas od odeslání události `AccountCreated` z AXA do jejího zpracování v OfficeLine.
    *   **Cíl:** < 5 sekund.
3.  **Settlement Error Rate:**
    *   **Definice:** Procento neúspěšných volání `CommitPayment` (např. z důvodu timeoutu nebo chyby API).
    *   **Cíl:** < 0.1%.

## 3. Proces denního odsouhlasení (Reconciliation)

Každé ráno během Hypercare probíhá manuální/automatizovaná kontrola (T+1):

1.  **Export z OfficeLine:** Seznam všech objednávek ve stavu `EXECUTED` (Centris potvrdil obchod).
2.  **Export z AXA:** Seznam všech pohybů (transactions) s příslušným `Correlation ID` nebo `Blockage ID`.
3.  **Validace:**
    *   Suma transakcí v AXA = Suma objednávek v OL.
    *   Identifikace "PENDING" objednávek v OL, které nemají blokaci v AXA.
    *   Identifikace blokací v AXA, které nemají odpovídající objednávku v OL/Centrisu.

## 4. Elastic / Kibana Dashboarding

Pro Hypercare tým jsou připraveny specifické vizualizace:

*   **AXA Response Time:** Sledování latence API volání (AXA bývá pod zátěží pomalejší, což může vést k timeoutům v mobilní appce).
*   **Correlation ID Tracker:** Možnost vyhledat celou cestu peněz: `MA Request` -> `OL Reserve` -> `Centris Confirm` -> `OL Commit`.
*   **Error Codes Heatmap:** Přehled chybových kódů z AXA (např. `AXA-045: Account Blocked`, `AXA-012: Insufficient Funds`).

## 5. Eskalační matice pro Hypercare

| Typ problému | Priorita | Akce |
| :--- | :--- | :--- |
| **Chyba u `CommitPayment`** | P1 (Kritická) | Okamžitý manuální zásah Back Office, hrozí nesoulad v účetnictví. |
| **Vysoká latence AXA (> 3s)** | P2 (Vysoká) | Eskalace na tým infrastruktury AXA, hrozí "zamrznutí" mobilní appky. |
| **Chybějící MQ eventy** | P3 (Střední) | Restart MQ listeneru v OfficeLine, ruční synchronizace portfolia klienta. |

---
*Související dokumenty:*
- [AXA_Summary.md](AXA_Summary.md)
- [Koncepce_logovani_PrivatBanka.md](../../Koncepce_logovani_PrivatBanka.md)

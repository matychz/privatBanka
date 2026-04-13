# Koncepce logování v PrivatBance

Tento dokument definuje strategický a technický rámec pro sběr, zpracování a analýzu logů v rámci digitálního bankovnictví a onboardingových procesů. Cílem je zajistit plnou observabilitu systému, soulad s bezpečnostními standardy a podporu pro provozní i business rozhodování.

---

## 1. Cíle logování

Koncepce logování v PrivatBance sleduje tři hlavní pilíře, které musí být v souladu s regulatorními požadavky (NBS, EBA) a vnitřními předpisy banky:

1.  **Provozní stabilita (Operations):**
    *   **Rychlá diagnostika:** Detekce chyb (5xx, 4xx) v reálném čase, analýza stack trace a latence (p95, p99).
    *   **Dostupnost (SLA):** Sledování dostupnosti kritických cest (např. login, podpis smlouvy) s cílem minimalizovat MTTR (Mean Time To Recovery).
    *   **Kapacitní plánování:** Analýza vytížení infrastruktury (CPU, RAM, DB connection pools) pro včasné škálování.

2.  **Business Intelligence (BI):**
    *   **Onboarding Funnel:** Sledování průchodu klienta procesem (začátek, nahrání dokladu, biometrie, podpis).
    *   **Drop-off Analysis:** Identifikace kroků, kde klienti proces opouštějí (např. příliš složitá biometrie v ZenID).
    *   **Marketingová úspěšnost:** Sledování konverzí z různých kanálů (web, mobilní aplikace).

3.  **Bezpečnost, Audit a Compliance (Security):**
    *   **Auditní stopa:** Záznam o tom, KDO (uživatel/systém), KDY (timestamp) a CO (akce/objekt) udělal. Toto je klíčové pro vyšetřování podvodů (Fraud Detection) a požadavky NBS.
    *   **Incident Response:** Detekce anomálií (např. 1000 neúspěšných přihlášení z jedné IP za minutu - Brute Force).
    *   **GDPR:** Zajištění anonymizace osobních údajů při zachování korelability pro řešení reklamací.

---

## 2. Přehled provozovaných systémů

| Systém | Technologie | Role v logování | Klíčové logované události |
| :--- | :--- | :--- | :--- |
| **Mobilní API Gateway** | .NET (IIS) | Vstupní bod, Auth, Proxy. | HTTP requesty, Response codes, Security headers, Device fingerprinty. |
| **OfficeLine (OL)** | .NET (IIS) | Business logika, integrace. | Volání externích služeb (E-mail, SMS), změny stavu procesu, integrační chyby. |
| **Centris / STORM** | Core System | Finální zápis, Core bankovní operace. | Založení klienta/účtu, finanční transakce, auditní záznamy o změnách v DB. |
| **AXA Core** | Core System | Správa účtů, clearing, karetní operace. | Zúčtování transakcí, blokace prostředků, změny zůstatků, MQ eventy (založení produktu). |
| **LegacyAuthGateway (LAG)** | .NET (IIS) | SSO, Token management. | Vystavení/validace tokenů, přesměrování mezi NIB a OIB, Auditní záznamy o přístupech. |
| **Trask ZenID** | SaaS (Azure) | Identita, OCR, Biometrie. | Výsledek ověření (Confidence Score), chyby nahrávání, metadata o dokladech (bez scanů). |

---

## 3. Technický standard (JSON Schéma)

Pro zajištění korelace napříč distribuovaným prostředím a splnění auditních požadavků je závazné používat toto JSON schéma:

*   **`timestamp`**: Čas události v UTC (ISO8601).
*   **`system`**: Identifikátor komponenty (např. `ibconsole`, `office-line`).
*   **`operation`**: Název business nebo technické operace (např. `VerifyIdentity`, `ResendOtp`).
*   **`correlationId`**: Unikátní GUID pro celé E2E flow (předává se v HTTP hlavičkách `X-Correlation-ID`).
*   **`processId`**: Business ID onboardingového procesu (např. `ONB-2026-000123`).
*   **`user.id`**: Identifikátor přihlášeného uživatele (pokud je znám, anonymizovaný hash).
*   **`user.ip`**: Zdrojová IP adresa klienta (pro auditní a security účely).
*   **`action.type`**: Typ akce (např. `Read`, `Write`, `Delete`, `Auth`, `LoginSuccess`, `LoginFail`).
*   **`result`**: Výsledek (OK, Error, Started).
*   **`message`**: Lidsky čitelný popis.
*   **`level`**: Log level (Info, Warn, Error, Critical, Audit).

---

## 4. Auditní logování

Auditní logování je v rámci banky odděleno od běžného provozního logování svou kritikou a archivačními pravidly.

### Rozdíl oproti provozním logům
| Vlastnost | Provozní logy | Auditní logy |
| :--- | :--- | :--- |
| **Cíl** | Debugging, monitoring. | Právní průkaznost, bezpečnost. |
| **Retence** | 3 - 6 měsíců. | 5 - 10 let (dle typu dat). |
| **Úroveň detailu** | Technické (stack trace, SQL). | Byznysové (Kdo, Kdy, Co změnil). |
| **Integrita** | Běžné zabezpečení. | Zákaz smazání/úpravy, digitální podpis (WORM storage). |

### Povinně auditované události
Všechny systémy musí pro pole `level: Audit` logovat:
1.  **Správa přístupu:** Úspěšná přihlášení, neúspěšné pokusy, změny oprávnění (RBAC), odhlášení.
2.  **Finanční operace:** Zahájení transakce, potvrzení platby, změna limitů.
3.  **Práce s daty (GDPR):** Export citlivých dat, nahlížení do klientské složky, smazání klienta.
4.  **Onboarding:** Výsledek liveness testu (ZenID), výsledek AML kontroly v Centrisu, výsledek založení produktů v AXA Core, podpis smlouvy.

### Auditní artefakty (Non-textual logs)
Mimo JSON logy banka archivuje tyto binární auditní artefakty:
*   **ZenID PDF reporty:** Souhrnný PDF report z vytěžování dokladu (uloženo v archivu dokumentů).
*   **Podepsané dokumenty:** Elektronicky podepsané smlouvy s časovým razítkem.
*   **Database Audit Trail:** Transakční logy core systémů (Centris/STORM, AXA).

---

## 5. Best Practices a Bezpečnost

### OWASP A09:2021 (Security Logging and Monitoring Failures)
*   Logujeme každé neúspěšné přihlášení (401/403) a pokus o přístup k neautorizovaným zdrojům.
*   Logy jsou ukládány mimo lokální file systém do centrálního Elasticu s nastavenou retencí.
*   **Log Integrity:** Logovací pipeline musí být zajištěna proti manipulaci. Každý pokus o smazání logů je monitorován.
*   Nad logy jsou nastaveny alerty na kritické chyby a anomálie (např. spike v počtu 500 chyb).

### GDPR a Anonymizace OÚ
*   **E-maily:** Jsou v poli `message` automaticky nahrazeny MD5 hashem ve formátu `#EMAIL#<hash>#EMAIL#`.
*   **Citlivá data:** Logy nesmí obsahovat hesla (včetně logování request body!), čísla karet (PAN), ani plná jména bez maskování.
*   **Korelace:** Anonymizace je reverzibilní pouze pro účely dohledání nahlášené chyby v autorizovaném režimu (např. Security Officer), nikoliv hromadně.

---

## 6. Monitoring a Alerting

### Provozní pohled (Dashboardy)
*   **Availability:** Procento úspěšných requestů (2xx vs 5xx).
*   **Performance:** P95 latence klíčových API endpointů.
*   **Error Rate:** Počet chyb rozdělený podle systémů a typů operací.

### Business pohled (Funnel Analysis)
*   **Conversion Rate:** Kolik % klientů, kteří začali onboarding, jej úspěšně dokončilo.
*   **Drop-off Points:** Ve kterém kroku (nahrání dokladu, podpis smlouvy) klienti proces nejčastěji opouštějí.
*   **Service Load:** Vytížení systému ZenID, Centris a AXA Core v reálném čase.

---

## 7. Implementační kroky

1.  **Instalace Elastic Agentů** na všechny IIS servery (Mobile API, OL, LAG).
2.  **Konfigurace Ingest Pipelines** pro normalizaci logů do JSON schématu.
3.  **Nastavení Correlation ID** v HTTP middlewarech napříč systémy.
4.  **Vytvoření Kibana Dashboardů** pro Operations a Business týmy.

# OfficeLine Mobile API – Přehled endpointů

Tento dokument shrnuje klíčové REST endpointy poskytované systémem **OfficeLine** (přes API Gateway) pro mobilní aplikaci v rámci modulu pro obchodování a onboardingu.

## 1. Modul: Obchodování (Securities & Trading)

| Endpoint | Metoda | Popis |
|---|---|---|
| `/v1/securities` | GET | Seznam aktuálně nabízených cenných papírů (dluhopisů). |
| `/v1/securities/{id}` | GET | Detail vybraného cenného papíru. |
| `/v1/account/{id}/balance` | GET | Ověření disponibilního zůstatku na účtu pro nákup. |
| `/v1/orders` | POST | Odeslání žádosti o nákup (vytvoření pokynu). |
| `/v1/orders/{id}` | GET | Aktuální stav a detail pokynu (Proveden, Odmítnut atd.). |
| `/v1/orders/{id}/approve` | POST | Autorizace pokynu klientem (po kontrole). |

## 2. Modul: MiFID Dotazníky (Investment Exams)

| Endpoint | Metoda | Popis |
|---|---|---|
| `/v1/mifid/status` | GET | Kontrola platnosti MiFID testu pro daného klienta. |
| `/v1/mifid/{id}` | GET | Vygenerování a stažení dotazníku (otázek) k vyplnění. |
| `/v1/mifid/{id}` | POST | Odeslání odpovědí a získání výsledku (PASS/FAIL). |
| `/v1/mifid/{id}/challenge` | POST | Inicializace autorizačního toku (výzva k biometrice/PIN). |
| `/v1/mifid/{id}/authorize` | POST | Finální odeslání autorizačního kódu a uzavření testu. |

## 3. Modul: Investiční smlouvy (Contracts)

| Endpoint | Metoda | Popis |
|---|---|---|
| `/v1/investment-contract` | GET | Kontrola existence platné investiční smlouvy. |
| `/v1/investment-contract` | POST | Zahájení procesu vytvoření nové investiční smlouvy. |
| `/v1/investment-contract/document/{id}` | GET | Stažení vygenerovaného PDF dokumentu smlouvy k přečtení. |
| `/v1/investment-contract/{id}/authorize` | POST | Digitální podpis (autorizace) investiční smlouvy. |

## 4. Technické standardy a bezpečnost

*   **Formát dat:** JSON (UTF-8).
*   **Autentizace:** Požadavky vyžadují platný JWT token (získaný po přihlášení v eCobra).
*   **Autorizace operací:** Kritické operace (např. odeslání pokynu, podpis smlouvy) vyžadují dvoufázovou autorizaci (`challenge` -> `authorize`).
*   **Ošetření chyb:** Standardní HTTP status kódy (400 Bad Request, 401 Unauthorized, 403 Forbidden, 500 Internal Server Error).

---
*Zdroj: DigitalnyOnBoarding Wiki (TR-OL-CP-Celkova-architektura.md, TR01-OL-CP-zobrazeni-nabidky-CP.md)*

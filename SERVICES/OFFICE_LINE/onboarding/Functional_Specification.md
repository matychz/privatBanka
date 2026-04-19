# Functional Specification - OfficeLine (E-Banking)

Toto je dokumentace funkcionalit systému OfficeLine (**OL**), neboli e-bankingu Privatbanky, v kontextu digitálního onboardingu.

**OL**, ve zkratce, implementuje:
- Internet Banking (front-end).
- Byznysovou logiku (middleware-like funkcionality): 
  - Persistování dat transakcí, klientů, disponentů, účtů, karet aj.
  - Napojení na core banking systém **Axa** pro provádění transakcí (clearing).
  - Udržování zůstatků na účtech apod.
  - Silná autentizace.
  - Správa disponentského modelu.
- **REST API pro mobilní bankovní aplikaci**.
- **REST API pro onboarding.**

Kromě vlastního OfficeLine je v rámci řešení E-BANKINGu použit také **eCobra Server** - autentizační server implementující silnou autentizaci.

## Klíčové procesy (MVP Onboarding)

Během procesu digitálního onboardingu plní OL tyto úkoly:
*   Vytvoření onboardingové session.
*   Správa a validace kontaktních údajů (SMS/E-mail přes eKobra).
*   Integrace se ZenID pro biometrickou identifikaci.
*   AML kontroly (volání API Centris).
*   Generování smluvní dokumentace.
*   Zajištění podpisu pomocí SMS OTP.
*   Založení klienta v core systému Centris/AXA.

## Onboarding REST API

API spravuje celý životní cyklus onboarding procesu (`/v1/onboarding/...`). 

### Hlavní endpointy (předpokládané):
- `POST /v1/onboarding/session` - Iniciace nové session
- `POST /v1/onboarding/contact/sms` - Ověření telefonního čísla
- `POST /v1/onboarding/contact/email` - Ověření e-mailu
- `POST /v1/onboarding/identity` - Uložení dat z OCR a biometriky
- `GET /v1/onboarding/aml` - Spuštění AML kontroly
- `GET /v1/onboarding/contracts` - Získání smluv k podpisu
- `POST /v1/onboarding/sign` - Podpis smluv

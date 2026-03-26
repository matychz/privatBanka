# Souhrnná analýza DigitalnyOnBoarding Wiki - PrivatBanka

Tento dokument obsahuje souhrn klíčových oblastí popsaných v Azure Wiki projektu DigitalnyOnBoarding.

## 1. Onboarding proces (Digitální onboarding)
Hlavním cílem projektu je umožnit novým klientům založit si účet v bance plně digitálně (mobile-first).

### Klíčové kroky procesu:
1.  **Identifikace klienta (KYC):** Probíhá pomocí řešení **Trask ZenID**. Zahrnuje nahrání dokladů totožnosti a ověření liveness (živosti) klienta.
2.  **AML a sankční kontroly:** Kontrola klienta proti sankčním seznamům a interním blacklistům (integrováno v systému CENTRIS).
3.  **Výběr produktu:** Klient si volí typ účtu a doplňkové služby.
4.  **Smluvní dokumentace:** Generování smluv a jejich potvrzení klientem.
5.  **Elektronický podpis:** Podepisování dokumentů pomocí jednorázového kódu (OTP).
6.  **Založení v core systému:** Automatizované založení klienta a účtu v systému Centris/STORM.
7.  **Aktivace účtu:** Prvotní vklad nebo jiný aktivační mechanismus.

## 2. Architektura a komponenty
Systém se skládá z několika klíčových komponent:

*   **Mobile API Backend:** Poskytuje REST rozhraní pro mobilní aplikaci a nové internetové bankovnictví (NIB).
*   **OfficeLine (OL) / ALSoft:** Zajišťuje byznysovou logiku, integrační vrstvu a autentizační služby. Běží v režimu 24/7.
*   **Centris / STORM:** Core bankovní systém, "zdroj pravdy" o klientech a smlouvách.
*   **LegacyAuthGateway (LAG):** Zajišťuje propojení mezi starým a novým autentizačním světem.
*   **ZenID (Trask):** Externí služba pro digitální identitu a KYC.

## 3. Integrace a API
Wiki podrobně popisuje několik API rozhraní:

### ONB REST API (Onboarding API)
*   Verze: 10.0.2
*   Spravuje celý životní cyklus onboarding procesu (`/v1/onboarding/...`).
*   Zahrnuje endpointy pro ověření telefonu/emailu, nahrávání dokladů, výběr produktů a aktivaci tokenu.

### LAG API (Legacy Auth Gateway)
*   Řeší přihlašování a správu tokenů.
*   Umožňuje **Single Sign-On (SSO)** ze starého internetového bankovnictví do nového a naopak.
*   Endpoint `/v1/token` pro získání access tokenu.
*   Endpoint `/v1/url` pro získání adresného redirectu do starého IB pro funkce, které v novém ještě nejsou (např. detaily investic).

## 4. Mobilní Onboarding
*   Důraz na "Mobile-first" přístup.
*   Využití push notifikací pro informování klienta o stavu procesu.
*   Aktivace **eCobra Tokenu (ECT)** jako hlavního bezpečnostního prvku pro budoucí přihlašování.

## 5. Deployment a prostředí
*   **DEV prostředí:**
    *   Mobilní API: `https://ma-dev.privatbanka.sk/api`
    *   Nové IB: `https://ibankdev.privatbanka.sk/PentaIB/`
    *   ZenID: `https://privatbanka.frauds.zenid.cz/`
*   Popisuje CI/CD procesy a způsob nasazení front-endu do bankovní infrastruktury.

---
*Zpracováno na základě stažených dat z Azure Wiki ke dni 18. 03. 2026.*

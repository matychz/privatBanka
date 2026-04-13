# OfficeLine (OL) – Technický přehled a role v systému

Tento dokument poskytuje základní přehled o systému **OfficeLine (OL)**, který slouží jako hlavní backend (middleware) pro digitální kanály Privatbanky.

## 1. Hlavní role a funkcionality

Systém **OfficeLine** (neboli e-banking backend) implementuje klíčovou byznysovou logiku a slouží jako integrační uzel mezi různými externími a interními systémy:

*   **Internet Banking Frontend:** Poskytuje UI a logiku pro webové bankovnictví.
*   **Business Logic (Middleware):**
    *   Persistování dat transakcí, klientů, disponentů, účtů a karet v dedikované databázi (**DB OL**).
    *   Udržování disponibilních zůstatků na účtech.
    *   Správa disponentského modelu (oprávnění a vztahy).
*   **Integrační uzel:**
    *   **Core Banking (Axa):** Napojení pro provádění transakcí a clearingu (viz [dokumentace integrace AXA](../AXA/AXA_Summary.md)).
    *   **Centris (TradingService):** Integrace pro investiční služby a onboarding (viz [dokumentace integrace CENTRIS](../CENTRIS/CENTRIS_Summary.md)).
    *   **ZenID:** Získávání vytěžených dat z dokladů totožnosti.
*   **REST API pro mobilní aplikaci:**
    *   Poskytuje endpointy pro kompletní proces digitálního onboardingu.
    *   Obsluhuje požadavky mobilního bankovnictví (přehledy, transakce, obchodování).
*   **Bezpečnost a autentizace:**
    *   Spolupracuje s **eCobra Serverem** pro silnou autentizaci (SCA).
    *   Implementuje správu session a autorizační toky.

## 2. Architektonické komponenty

1.  **OL Backend:** Jádro systému napsané v .NET/Java (dle specifikace), obsluhující byznysovou logiku.
2.  **OL API Gateway:** Vstupní bod pro mobilní aplikaci, zajišťující routování, transformaci dat a bezpečnost.
3.  **DB OL:** Relační databáze pro ukládání stavových informací, které nejsou v reálném čase dostupné v core bankingu.
4.  **eCobra Server:** Autentizační server pro správu uživatelských identit a certifikátů.

## 3. Klíčové procesy (MVP Onboarding)

Během procesu digitálního onboardingu plní OL tyto úkoly:
*   Vytvoření onboardingové session.
*   Komunikace se ZenID pro validaci dokladů.
*   Sběr doplňujících informací od klienta (AML dotazník, souhlasy).
*   Generování smluvní dokumentace (PDF).
*   Založení klienta v systému Centris a následně v Core Bankingu.

---
*Zdroj: DigitalnyOnBoarding Wiki (Funkční specifikace OfficeLine (E-Banking).md)*

# Onboarding Documentation

Tato složka obsahuje technickou a funkční dokumentaci k procesu digitálního onboardingu v Privatbance. Dokumentace byla migrována z Azure Wiki.

## Obsah složky

1.  **[Architecture Blueprint](./Architecture_Blueprint.md)**
    *   Celkový přehled komponent (OfficeLine, Centris, ZenID, SmartBanka).
    *   Diagramy architektury a popis komunikačních toků.
    *   Rozpad procesu podle obrazovek (Figma).

2.  **[ZenID Integration](./ZenID_Integration.md)**
    *   Detailní popis integrace biometrického ověření identity.
    *   Vazby na SDK, proxy operace a asynchronní zpracování vzorků.
    *   Odkazy na sandbox a manuály dodavatele.

3.  **[Functional Specification](./Functional_Specification.md)**
    *   Specifikace role OfficeLine v rámci onboardingu.
    *   Přehled byznysových procesů (session management, AML, podpisy).

4.  **[API Mapping Steps](./API_Mapping_Steps.md)**
    *   Detailní mapování vizuálních kroků z Figmy na konkrétní API operace a endpointy.

5.  **[API Parameters Detailed](./API_Parameters_Detailed.md)**
    *   Detailní přehled všech parametrů pro každou API operaci, včetně datových typů a číselníků (Enums).

6.  **[Onboarding Swagger (OpenAPI)](./onboarding_swagger.yaml)**
    *   Kompletní OpenAPI 3.0 specifikace REST API rozhraní (verze 12.0.0).

7.  **[Attachments](./attachments/)**
    *   Přílohy, diagramy a XLSX soubory použité v dokumentaci.

## Rychlé odkazy
- **Figma Onboarding:** [Odkaz](https://www.figma.com/design/GBRsstOiURYZ6Z6uHHOsfQ/Onboarding)
- **ZenID Swagger:** [https://privatbanka.frauds.zenid.cz/swagger/index.html](https://privatbanka.frauds.zenid.cz/swagger/index.html)
- **DEV Backend:** `https://ma-dev.privatbanka.sk/api`

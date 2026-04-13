# Integrace CENTRIS – Technický přehled

Tento dokument popisuje technickou integraci mezi **OfficeLine BE** a **Centris (TradingService)** pro operace `CreateEdcContract` a související investiční služby.

## 1. Rozhraní a odpovědnosti

### OfficeLine BE
OfficeLine:
*   Agreguje data získaná během onboardingu (ZenID, vstupy od klienta).
*   Generuje `ClientNumber` ve formátu **Z + 7 náhodných číslic**.
*   Sestavuje payload `CreateEdcContract` dle mapovací specifikace.
*   Volá službu Centris (TradingService).

### Centris (TradingService)
Centris:
*   Přijímá payload `CreateEdcContract`.
*   Provádí validaci vstupu.
*   Vrací technickou odpověď (úspěch / validační chyba).
*   Interní zpracování v Centris (např. synchronizace do systému IBIS) je mimo rozsah této dokumentace.

## 2. Mapování dat a původ

Data odesílaná do Centris mohou pocházet z:
*   **ZenID (MinedData):** Vytěžená data z dokladů totožnosti.
*   **Vstupy z onboardingu:** Data zadaná klientem v mobilní aplikaci.
*   **Hodnoty generované v OfficeLine:** Např. `ClientNumber`.
*   **Odvozené nebo konstantní hodnoty:** Např. `BirthCountryCode` (pokud chybí, plní se konstantou).

## 3. Technický model komunikace

*   OfficeLine volá operaci `CreateEdcContract` synchronně.
*   Komunikace je typu **Request–Response**.
*   Centris vrací technickou odpověď (úspěch / validační chyba).

### Sekvenční diagram integrace

```mermaid
sequenceDiagram
  autonumber
  actor Mobile as Mobile App
  participant OL as OfficeLine BE
  participant Zen as ZenID BE
  participant Cen as Centris (TradingService)

  Note over Mobile,OL: Onboarding = sequence of API calls initiated by Mobile App

  Mobile->>OL: Onboarding steps (AML, consents, contact details, etc.)
  OL->>Zen: Upload/Investigate session
  Zen-->>OL: MinedData (identity extraction)
  Mobile->>OL: Confirm mined data + provide missing inputs

  Note over OL: Finalization / Summary step
  OL->>OL: Aggregate onboarding data + Generate ClientNumber (Z1234567) + Prepare CreateEdcContract payload

  OL->>Cen: CreateEdcContract (mapped payload)
  Cen-->>OL: (OK/Accepted) or validation error

  Note over Cen: Centris internal follow-up processing is out of scope (black box)
```

## 4. Otevřené technické body

*   **Formát času podpisu:** Používá se `dateTime` s časovou zónou (zvalidováno s BU).
*   **BirthCountryCode:** Pokud není k dispozici ze ZenID, plní se konstantou (řeší se s BU).
*   **CorrespondenceAddress:** Korespondenční adresa se aktuálně neposílá, Centris využívá trvalou adresu ze ZenID.
*   **DeviceInfo:** Plánované rozšíření o metadata zařízení v budoucích verzích.
*   **Ošetření chyb:** Asynchronní proces na úrovni založení produktu pro zajištění plynulosti onboardingu (řešení welcome mailu a nočních uživatelů).

---
*Zdroj: DigitalnyOnBoarding Wiki (Funkční specifikace OfficeLine / Architektura OL / Volaná rozhraní / CENTRIS.md)*

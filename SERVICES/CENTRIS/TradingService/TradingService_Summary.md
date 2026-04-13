# TradingService (Centris) – Souhrnné informace

Tento dokument shrnuje technickou specifikaci služby **TradingService** (Centris). Pro obecné informace o integraci systému Centris a rozdělení odpovědností navštivte:

*   [**Obecný technický přehled integrace CENTRIS**](../CENTRIS_Summary.md)

## 1. Účel a role v architektuře
Služba **TradingService** v systému Centris slouží k finálnímu zpracování onboardingu klienta, správě investičních nástrojů, pokynů, smluv a MiFID testů.

*   **OfficeLine BE:** Agreguje data z onboardingu (ZenID, vstupy od klienta), generuje `ClientNumber` (formát Z + 7 číslic) a sestavuje SOAP payload pro volání služby.
*   **Centris (TradingService):** Primární systém pro správu obchodování, provádí validace (včetně kontrol na sankční seznamy a AML blacklisty) a synchronizuje data se systémem IBIS (Storm).

## 2. Technická specifikace
*   **Protokol:** SOAP 1.2
*   **Endpoint:** `https://172.16.100.39/OnlineTrading/TradingService.svc`
*   **Zabezpečení:** HTTPS, WS-Addressing (vyžadováno), WS-Security (`UsernameToken` s `SecureConversation`, `IncludeTimestamp`).
*   **Jmenné prostory:**
    *   `tem`: `http://tempuri.org/` (operace)
    *   `mod`: `http://schemas.datacontract.org/2004/07/Models` (datové typy)

## 3. Přehled operací
Služba obsahuje operace pro správu nástrojů, klientů, pokynů, smluv a MiFID testů. Detailní seznam operací naleznete v samostatném dokumentu:

*   [**Detailní přehled operací TradingService**](TradingService_Operations.md)

### Klíčové operace pro Onboarding:
*   `CreateEdcContract`: Vytvoření EDC smlouvy a založení klienta.
*   `CreateInvestmentContract`: Vytvoření investiční smlouvy.
*   `GenerateClientExam`: Vygenerování MiFID testu.
*   `PerformClientExam`: Vyhodnocení testu.

## 4. Datová struktura `CreateEdcContract`
Klíčový objekt `edcContract` obsahuje:
*   **Základní údaje:** `ContractNumber` (např. `028-E-2025-XXXXX`), `FileContent` (PDF smlouvy), `DateOfSignature`.
*   **Klient (`EdcClient`):** `ClientNumber`, `FirstName`, `LastName`, `BirthDate`, `Sex` (0=Žena, 1=Muž).
*   **Adresy:** `MainAddress` (Trvalý pobyt) a `CorrespondenceAddress`.
*   **IdentityList:** Seznam dokladů (Typy: RC, OP, CP, ICO).
*   **Příznaky:** `IsPoliticallyExposedPerson` (PEP), `IsPersonWithRelationship`.

## 5. Integrační pravidla a otevřené body
*   **Sankční seznamy:** Centris aktualizuje seznamy denně (cca 5:55). Klient není založen při shodě na AML blacklistu.
*   **Zdroj dat:** Primárně ZenID (vytěžená data) doplněná o vstupy z mobilní aplikace.
*   **Otevřené body:**
    *   `BirthCountryCode`: Pokud chybí v ZenID, plní se konstantou (řeší se s BU).
    *   `CorrespondenceAddress`: Pokud se neplní, v Centris se využívá trvalá adresa.
    *   `DeviceInfo`: Plánované rozšíření o metadata zařízení (correlationId) pro lepší observability.
    *   `Timezone`: Ověření formátu `dateTime` pro datum podpisu smlouvy.

---
*Zdroj: DigitalnyOnBoarding Wiki (CENTRIS.md, CENTRIS-INV-SOAP.md, Trading-Service.md)*

# Přehled operací TradingService (Centris)

Tato dokumentace poskytuje detailní přehled všech dostupných operací služby `TradingService` (Centris).

**Endpoint:** `https://172.16.100.39/OnlineTrading/TradingService.svc`  
**Protokol:** SOAP / HTTPS, autentizace WS-Security (UsernameToken + SecureConversation).

---

## 1. Nástroje (Instruments)

| Operace | Popis | Výstup |
|---|---|---|
| `GetInstruments` | Seznam dostupných nástrojů (dluhopisů). | `ArrayOfInstrument` |
| `GetInstrumentsForClient` | Nástroje dostupné pro konkrétního klienta. | `ArrayOfInstrument` |
| `GetInstrument` | Detail nástroje podle ID. | `Instrument` |
| `CreateInstrument` | Vytvoření nového nástroje. | void |
| `UpdateInstrument` | Aktualizace existujícího nástroje. | void |
| `DeleteInstrument` | Smazání nástroje. | void |

---

## 2. Klient (Client)

| Operace | Popis | Výstup |
|---|---|---|
| `GetClient` | Data klienta podle `abo` (např. `123456789`). | `Client` |
| `GetClientAddress` | Adresa klienta. | `Address` |
| `GetClientContacts` | Kontaktní údaje klienta. | `ActionResult<ArrayOfClientContact>` |
| `GetClientRepresentativePersons` | Zmocněné osoby a disponenti. | `ActionResult<ArrayOfPerson>` |
| `GetClientInvestmentStrategies` | Investiční strategie klienta. | `ArrayOfClientInvestmentStrategy` |

---

## 3. MiFID dotazník (Client Exam)

| Operace | Popis | Výstup |
|---|---|---|
| `GenerateClientExam` | Vygeneruje MiFID dotazník pro klienta. | `GenerateClientExamResult` |
| `GenerateClientExamForInvestmentContract` | Dotazník pro investiční smlouvu. | `GenerateClientExamResult` |
| `PerformClientExam` | Odeslání vyplněného dotazníku (včetně vyhodnocení). | `PerformClientExamResult` |
| `GetExamDefinitionsForClient` | Dostupné definice dotazníků. | `GetExamDefinitionsForClientResult` |
| `GetClientExamsView` | Historie dotazníků klienta. | `GetClientExamsViewResult` |
| `GetActiveClientExamForInvestmentContract` | Aktuálně platný dotazník. | `ActiveClientExamForInvestmentContract` |
| `GetAllowedStrategyTypeList` | Povolené investiční strategie na základě výsledků testu. | `ActionResult<ArrayOfInvestmentStrategyType>` |

### Technické požadavky na MiFID testy:
*   **`AdditionalInfo`**: Nová struktura pro otázky (obsahuje `Title`, `Subtitle`, `Text`, `LinkText`). Slouží pro zobrazení doplňujících informací v mobilní aplikaci.
*   **`IsOverrideOption`**: Příznak u odpovědi, který zneplatňuje ostatní volby (např. "Nemám žádné zkušenosti").
*   **Vyhodnocení (`PerformClientExam`)**: Backend musí vracet `IsPassed`, `InvestmentHorizon`, `RiskAttitudeAssessment` a `LossImpactAssessment`.
*   **`ScorePercentage`**: Výsledné procentuální hodnocení testu zaokrouhlené na celé číslo.

---

## 4. Smlouvy (Contracts)

| Operace | Popis | Výstup |
|---|---|---|
| `CreateEdcContract` | Vytvoření EDC smlouvy a založení klienta (klíčové pro ONB). | `ActionResult<EdcContract>` |
| `CreateInvestmentContract` | Vytvoření investiční smlouvy. | `CreateInvestmentContractResult` |
| `CreateAccountContract` | Vytvoření účetní smlouvy. | `ActionResult<AccountContract>` |
| `CreateTVContract` | Vytvoření smlouvy o termínovaném vkladu. | `ActionResult<TVContract>` |
| `GetActiveInvestmentContract` | Aktivní investiční smlouva. | `ActiveInvestmentContract` |

---

## 5. Objednávky a šablony (Orders & Templates)

| Operace | Popis | Výstup |
|---|---|---|
| `CreateOrder` | Vytvoření pokynu k nákupu/prodeji. | `CreateOrderResult` |
| `ConfirmOrder` | Potvrzení objednávky po autorizaci klientem. | `boolean` |
| `GetFee` | Výpočet poplatku před potvrzením. | `decimal` |
| `GetIbisOrders` | Objednávky ze systému IBIS. | `ArrayOfIbisOrder` |
| `CreateOrderTemplate` | Správa šablon pokynů. | void |

---

## 6. Prohlášení a výpisy (Declarations & Statements)

| Operace | Popis | Výstup |
|---|---|---|
| `SetTaxDomicileDeclaration` | Uložení prohlášení o daňové rezidenci. | `ActionResult<TaxDomicileDeclaration>` |
| `SetAMLDeclaration` | Uložení AML prohlášení. | `ActionResult<AMLDeclaration>` |
| `SaveStatementGFI` | Uložení výpisu GFI. | `ActionResult<StatementGFI>` |
| `SaveStatementKUV` | Uložení výpisu KUV (Konečný uživatel výhod). | `ActionResult<StatementKUV>` |

---

## 7. Synchronizace (Sync)

| Operace | Popis |
|---|---|
| `SyncClientToIbis` | Synchronizace dat klienta do systému IBIS. |
| `SyncFailedContracts` | Opakování synchronizace neúspěšných smluv. |
| `SyncFailedAmlDeclarations` | Opakování syncu AML prohlášení. |
| `SyncFailedEdcContracts` | Opakování syncu EDC smluv. |

## 8. Mapování operací na procesy (Bond Project)

| Operace | Kód kroku | Význam v procesu |
|---|---|---|
| `GetInstrumentsForClient` | TR01 | Zobrazení dostupných dluhopisů v mobilní aplikaci. |
| `GetInstrument` | TR01 | Detail dluhopisu před nákupem. |
| `GetFee` | TR01 | Zobrazení poplatku klientovi před potvrzením. |
| `GetClientExamsView` | TR02, TR03 | Ověření platnosti MiFID dotazníku. |
| `GenerateClientExamForInvestmentContract` | TR03 | Vygenerování dotazníku pro zobrazení v aplikaci. |
| `PerformClientExam` | TR03 | Odeslání vyplněného dotazníku, získání PASS/FAIL. |
| `GetActiveInvestmentContract` | TR04 | Ověření existence a platnosti investiční smlouvy. |
| `CreateInvestmentContract` | TR05 | Vytvoření smlouvy po úspěšné autorizaci. |
| `CreateOrder` | TR07 | Vytvoření pokynu k nákupu. |
| `ConfirmOrder` | TR09a | Potvrzení pokynu po autorizaci v mobilní aplikaci. |

---
*Zdroj: DigitalnyOnBoarding Wiki (CENTRIS-INV-SOAP - tabulka operací.md, CENTRIS-INV-SOAP-requirements.md)*

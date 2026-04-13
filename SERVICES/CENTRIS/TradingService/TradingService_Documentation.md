# Dokumentace k TradingService (WSDL)

Tento dokument poskytuje přehled a popis webové služby `TradingService`, definované v souboru `TradingService 2.wsdl`. Služba slouží k řízení investičních nástrojů, klientů, obchodních pokynů a souvisejících procesů (MiFID testy, smlouvy, synchronizace s IBIS).

## 1. Základní informace

- **Název služby:** TradingService
- **Rozhraní (PortType):** `ITradingService`
- **Cílový jmenný prostor:** `http://tempuri.org/`
- **Endpoint:** `https://localhost/OnlineTrading/TradingService.svc` (podle `TradingService 2.wsdl`)
- **Protokol:** SOAP 1.2
- **Zabezpečení:** 
    - Komunikace přes HTTPS.
    - WS-Security: `UsernameToken` s `SecureConversation`.
    - Vyžaduje zasílání časového razítka (`IncludeTimestamp`).
    - WS-Addressing je vyžadováno.

## 2. Přehled operací

Operace lze rozdělit do několika logických skupin:

### 2.1 Správa investičních nástrojů (Instruments)
- `GetInstruments`: Získání seznamu dostupných investičních nástrojů s možností filtrace.
- `GetInstrumentsForClient`: Získání nástrojů dostupných pro konkrétního klienta.
- `GetInstrument`: Detail konkrétního nástroje podle ID.
- `CreateInstrument`, `UpdateInstrument`, `DeleteInstrument`: CRUD operace pro správu nástrojů.

### 2.2 Správa klientů (Clients)
- `GetClient`: Získání informací o klientovi podle jeho ABO čísla.
- `GetClientAddress`: Získání adresy klienta.
- `GetClientContacts`: Získání kontaktních údajů klienta.
- `SetDisponentContactDetails`, `SetDisponentAccountDetails`, `SetDisponentPaymentDetails`: Nastavení údajů pro disponenta.
- `SetTaxDomicileDeclaration`, `SetAMLDeclaration`: Evidence prohlášení o daňovém domicilu a AML.

### 2.3 Obchodní pokyny (Orders)
- `CreateOrder`: Vytvoření nového obchodního pokynu.
- `ConfirmOrder`: Potvrzení existujícího pokynu.
- `GetFee`: Výpočet poplatků pro zamýšlený obchod.
- `GetIbisOrders`: Získání pokynů ze systému IBIS.
- `SetSynchronizedOrder`: Označení pokynu jako synchronizovaného.

### 2.4 Šablony pokynů (Order Templates)
- `CreateOrderTemplate`, `UpdateOrderTemplate`, `DeleteOrderTemplate`: Správa šablon pokynů.
- `CreateOrderTemplateSet`, `UpdateOrderTemplateSet`, `DeleteOrderTemplateSet`: Správa sad šablon.

### 2.5 MiFID a klientské testy (Exams)
- `GenerateClientExam`: Generování nového testu pro klienta.
- `PerformClientExam`: Vyhodnocení vyplněného testu.
- `GetExamDefinitionsForClient`: Seznam definic testů dostupných pro klienta.
- `GetClientExamsView`: Přehled proběhlých testů klienta.
- `GetActiveClientExamForInvestmentContract`: Získání aktivního testu pro investiční smlouvu.

### 2.6 Smlouvy (Contracts)
- `CreateContract`: Vytvoření obecné smlouvy.
- `CreateInvestmentContract`: Vytvoření investiční smlouvy.
- `CreateAccountContract`, `CreateTVContract`, `CreateEdcContract`: Vytvoření specifických typů smluv.
- `GetActiveInvestmentContract`: Získání aktuálně platné investiční smlouvy.

### 2.7 Synchronizace a chyby
- `SyncClientToIbis`: Synchronizace dat klienta do systému IBIS.
- `GetErrors`: Získání seznamu chyb při synchronizaci.
- `SyncFailedContracts`, `SyncFailedInvestmentStrategies`, atd.: Opakování neúspěšných synchronizací pro různé entity.

### 2.8 Verifikace a ostatní
- `IsValidVerificationCode`: Ověření platnosti verifikačního kódu.
- `GenerateBankIdentityVerificationCode`: Generování kódu pro verifikaci přes Bankovní identitu.
- `UpdatePortfolioCustomName`: Změna uživatelského názvu portfolia.

## 3. Klíčové datové struktury

Většina datových typů je definována ve jmenném prostoru `http://schemas.datacontract.org/2004/07/Models`.

### 3.1 Client
Základní entita reprezentující klienta. Rozšiřuje typ `Person`.
- `Id`: Identifikátor klienta (ABO).
- `AssetAccounts`: Seznam majetkových účtů (`ArrayOfAssetAccount`).
- `BankAccounts`: Seznam bankovních účtů (`ArrayOfBankAccount`).
- `CanTrade`: Příznak, zda klient může obchodovat.
- `ActiveInvestmentContract`: Informace o platné investiční smlouvě.

### 3.2 Instrument
Reprezentuje investiční nástroj (např. dluhopis, akcie).
- `Id`: Interní ID.
- `Isin`: ISIN kód nástroje.
- `Name`: Název nástroje.
- `Currency`: Měna nástroje.
- `Auv`: Aktuální hodnota (např. alikvotní úrokový výnos).
- `MaturityDate`: Datum splatnosti.

### 3.3 Order
Reprezentuje obchodní pokyn.
- `Client`: Odkaz na klienta.
- `Instrument`: Odkaz na nástroj.
- `Action`: Typ operace (Nákup/Prodej).
- `Amount`: Množství/Objem.
- `BankFee`: Vypočtený poplatek banky.

### 3.4 MiFID Exams (Novinka ve verzi 2)
Struktury pro klientské testy.
- `Question`: Jednotlivá otázka v testu.
    - `AdditionalInfo`: Doplňující informace k otázce (typ `QuestionAdditionalInfo`).
- `QuestionAdditionalInfo`: Struktura obsahující pole:
    - `Title`: Nadpis informace.
    - `Subtitle`: Podnadpis.
    - `Text`: Hlavní text doplňující informace.
    - `LinkText`: Text odkazu (pokud je relevantní).

## 4. Technické detaily

### Jmenné prostory
- `wsdl`: `http://schemas.xmlsoap.org/wsdl/`
- `xsd`: `http://www.w3.org/2001/XMLSchema`
- `tns`: `http://tempuri.org/`
- `models`: `http://schemas.datacontract.org/2004/07/Models`

### Chybové stavy
Služba definuje standardní SOAP Faulty. Specifické validační chyby jsou vraceny v rámci synchronizačních operací nebo jako součást výsledků MiFID testů.

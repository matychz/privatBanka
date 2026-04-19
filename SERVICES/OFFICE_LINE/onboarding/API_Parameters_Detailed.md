# Detailní parametry Onboarding API operací (v12.0.0)

Seznam všech parametrů pro jednotlivé operace Onboarding API.

## Společné parametry (Headers)

Všechny endpointy kromě úvodního `POST /v1/onboarding` vyžadují autorizaci.

| Parametr | Typ | Umístění | Povinný | Popis |
| :--- | :--- | :--- | :--- | :--- |
| `Authorization` | `string` | Header | Ano | Formát: `Bearer <token>`. Token získáte v odpovědi na `POST /v1/onboarding`. |
| `Accept-Language` | `string` | Header | Ne | Preferovaný jazyk pro chybové hlášky (např. `cs-CZ`, `sk-SK`). |
| `Idempotency-Key` | `string` | Header | Ano* | Klíč pro zajištění idempotence u POST/PUT operací (min. 8 znaků). |

---

## 1. Správa session (Onboarding)

### `POST /v1/onboarding`
Inicializace nového procesu onboardingu.
- **Body (Request):**
  - `onboardingCountry` (string, povinné): `CZ`, `SK` nebo `OTHER`.
  - `channel` (string, volitelné): `MOBILE` (default) nebo `WEB`.
  - `pushIdentifier` (string, volitelné): Token pro push notifikace.
  - `deviceInfo` (object, volitelné): Detaily o zařízení (`platform`, `appVersion`, `osVersion`, `language`, `deviceName`, `deviceModel`, `deviceManufacturer`).
- **Response (201):**
  - `processId`: Unikátní identifikátor procesu (GUID).
  - `token`: Autentizační token.
  - `expiresAt`: Čas expirace procesu.
  - `packageVersion`: Aktuální verze regulatorních dokumentů.
  - `zenIdProfile`: Konfigurační profil pro ZenID SDK.

### `GET /v1/onboarding/{processId}/status`
Zjištění aktuálního stavu (makrokroku) procesu.
- **Path:** `processId`
- **Response (200):**
  - `step`: Název aktuálního makrokroku (např. `PHONE_VERIFICATION`, `IDENTITY_CAPTURE`, `AML_DATA_COLLECTION`, `CONTRACT_SIGNATURE`, `READY_FOR_TOKEN_ACTIVATION`).
  - `status`: Stav kroku (`IN_PROGRESS`, `COMPLETED`, `FAILED`).

### `POST /v1/onboarding/{processId}/otp/resend`
Znovuzaslání posledního vygenerovaného OTP (SMS nebo E-mail).
- **Path:** `processId`
- **Response (200):** `OtpInitiatedStepResponse` (obsahuje časy pro cooldown a expiraci).

### `PUT /v1/onboarding/{processId}/push-registration`
Dodatečná registrace nebo aktualizace push identifikátoru pro notifikace.
- **Path:** `processId`
- **Body:**
  - `pushIdentifier` (string, povinné): Nový token pro push notifikace.

---

## 2. Kontaktní údaje a verifikace

### `POST /v1/onboarding/{processId}/phone`
Zadání telefonního čísla.
- **Path:** `processId`
- **Body:**
  - `phoneNumber` (string): Číslo v mezinárodním formátu (např. `+420777111222`).
- **Response (200):** Detaily o odeslaném OTP (`expiresInSeconds`, `cooldownSeconds`, `remainingAttempts`).

### `POST /v1/onboarding/{processId}/phone/otp/verify`
Ověření SMS kódu.
- **Path:** `processId`
- **Body:**
  - `code` (string): 6-místný číselný kód.

### `POST /v1/onboarding/{processId}/email`
Zadání e-mailové adresy.
- **Path:** `processId`
- **Body:**
  - `email` (string): E-mailová adresa.

### `POST /v1/onboarding/{processId}/email/otp/verify`
Ověření e-mailového kódu.
- **Path:** `processId`
- **Body:**
  - `code` (string): 6-místný číselný kód.

---

## 3. Identita (ZenID integrace)

### `POST /v1/onboarding/{processId}/identity/init`
Inicializace identity v ZenID.
- **Path:** `processId`
- **Body:**
  - `sdkChallengeToken` (string): Token získaný ze ZenID SDK.
- **Response (200):**
  - `sdkInitPayload`: Payload pro inicializaci SDK.

### `POST /v1/onboarding/{processId}/identity/sample`
Nahrání vzorku (fotky dokladu nebo selfie).
- **Path:** `processId`
- **Body (Multipart/Form-Data):**
  - `kind` (string): `DOCUMENT_FRONT`, `DOCUMENT_BACK`, `SELFIE`.
  - `file` (binary): Soubor obrázku.

### `POST /v1/onboarding/{processId}/identity/finalize`
Spuštění OCR a vyhodnocení identity.
- **Path:** `processId`
- **Response (200):** Výsledná data a stav (`decision`: `APPROVED`/`REJECTED`, `minedData`: objekt s vytěženými údaji).

### `PUT /v1/onboarding/{processId}/identity/mined-data/confirmation`
Potvrzení nebo úprava vytěžených dat klientem.
- **Path:** `processId`
- **Body (IdentityMinedDataConfirmationRequest):**
  - `givenName`, `familyName`, `birthDate`, `birthPlace`, `birthNumber`, `documentNumber`, `documentExpiry`, `documentCountry`, `nationality`, `sex`, `titleBefore`, `titleAfter`.
  - `address`: Objekt s adresou (`street`, `buildingNumber`, `city`, `zipCode`, `countryRegionId`).

---

## 4. AML data a prohlášení

### `POST /v1/onboarding/{processId}/data/submit`
Odeslání všech sebraných AML dat a souhlasů.
- **Path:** `processId`
- **Body (OnboardingDataSubmitRequest):**
  - `payloadVersion` (string): Verze schématu.
  - `data` (object):
    - `biometricDataProcessing` (boolean): Souhlas s biometrikou.
    - `plannedInvestmentOverLimit` (boolean): Plánované investice nad limit.
    - `regulatoryStatements`: Souhlas s verzí dokumentů (`accepted`, `packageVersion`).
    - `privacyConsents`: Souhlasy se zpracováním dat (`dataProcessing`) a marketingem (`marketing`).
    - `incomeAndAssets`: Údaje o příjmech (`occupationCode`, `mainIncomeSourceCode`, `monthlyIncomeRangeCode`, `savingsAndInvestmentsRangeCode`).
    - `productUsage`: Účel využívání produktů (`usagePurposeCode`, `paymentCountryGroupCode`).

---

## 5. Dokumenty a podpis

### `POST /v1/onboarding/{processId}/documents/contracts`
Vygenerování smluvní dokumentace.
- **Path:** `processId`
- **Response (200):** Seznam dokumentů (`documentId`, `name`, `fileName`, `documentHash`).

### `GET /v1/onboarding/{processId}/documents/contracts/{documentId}`
Stažení konkrétního dokumentu v PDF.
- **Path:** `processId`, `documentId`.

### `POST /v1/onboarding/{processId}/documents/contracts/{documentId}/otp/request`
Vyžádání SMS OTP pro podpis dokumentu.
- **Path:** `processId`, `documentId`.

### `POST /v1/onboarding/{processId}/documents/contracts/{documentId}/otp/verify`
Ověření podpisu pomocí OTP.
- **Path:** `processId`, `documentId`.
- **Body:**
  - `code` (string): Podpisový kód.

---

## 6. Produkty a aktivace

### `POST /v1/onboarding/{processId}/products`
Výběr doplňkových produktů.
- **Path:** `processId`
- **Body (ProductSelectionSubmitRequest):**
  - `products` (array): Seznam vybraných produktů.
    - `productType` (string): Typ produktu (např. `CURRENT_ACCOUNT`, `SAVINGS_ACCOUNT`).
    - `currency` (string): Měna produktu (např. `CZK`, `EUR`).

### `GET /v1/onboarding/{processId}/credentials/public-key`
Získání veřejného klíče pro zašifrování hesla.

### `POST /v1/onboarding/{processId}/credentials`
Nastavení přístupových údajů (hesla).
- **Body:**
  - `password` (string): Šifrované heslo.

### `GET /v1/onboarding/{processId}/credentials`
Získání přiděleného uživatelského jména (k dispozici až po založení v Centrisu).

### `POST /v1/onboarding/{processId}/token/activate`
Finální aktivace mobilního tokenu. Vrátí aktivační data (`username`, `activationOtp`, `activationGuid`).

---

## 7. Regulatorní dokumenty

### `GET /v1/onboarding/{processId}/regulatory-documents/{packageVersion}/{documentCode}`
Stažení statických regulatorních dokumentů.
- **Path:** `processId`, `packageVersion`, `documentCode`.

---

## 8. Číselníky a výčtové typy (Enums)

Povolené hodnoty pro klíčové parametry AML a dalších dat.

### Povolání (`OccupationCode`)
- `ADMINISTRATION_ECONOMICS_PUBLIC_SERVICE_LAW`: Administrativa, ekonomika, veřejná správa, právo.
- `SECURITY_AND_PROTECTION`: Bezpečnost a ochrana.
- `TOURISM_CULTURE_AND_SERVICES`: Cestovní ruch, kultura a služby.
- `HEALTHCARE_SOCIAL_CARE_AND_PHARMACEUTICAL_INDUSTRY`: Zdravotnictví, sociální péče, farmacie.
- `MANAGEMENT_AND_BUSINESS`: Management a obchod.
- `INDUSTRY_AND_MANUFACTURING_AND_LOGISTICS_AND_ENERGY`: Průmysl, výroba, logistika a energetika.
- `AGRICULTURE_FORESTRY_AND_CRAFTS`: Zemědělství, lesnictví a řemesla.
- `EDUCATION_SCIENCE_AND_RESEARCH`: Vzdělávání, věda a výzkum.
- `INFORMATION_TECHNOLOGY`: Informační technologie.
- `STUDENT`: Student.

### Zdroj příjmů (`MainIncomeSourceCode`)
- `EMPLOYMENT`: Zaměstnání.
- `BUSINESS_OR_SELF_EMPLOYMENT`: Podnikání nebo OSVČ.
- `PENSIONS_AND_SOCIAL_BENEFITS`: Důchody a sociální dávky.
- `INCOME_FROM_CAPITAL_ASSETS`: Příjmy z kapitálového majetku.
- `LOANS`: Půjčky.
- `SALE_OF_IMMOVABLE_AND_MOVABLE_PROPERTY`: Prodej nemovitého a movitého majetku.
- `PROPERTY_RENTAL`: Pronájem majetku.
- `INHERITANCE`: Dědictví.
- `GIFT`: Dar.
- `OTHER`: Jiné.

### Měsíční příjem (`MonthlyIncomeRangeCode`)
- `UP_TO_50_000_CZK`: Do 50 000 Kč.
- `UP_TO_100_000_CZK`: Do 100 000 Kč.
- `ABOVE_100_000_CZK`: Nad 100 000 Kč.

### Úspory a investice (`SavingsAndInvestmentsRangeCode`)
- `UP_TO_1_000_000_CZK`: Do 1 000 000 Kč.
- `UP_TO_10_000_000_CZK`: Do 10 000 000 Kč.
- `ABOVE_10_000_000_CZK`: Nad 10 000 000 Kč.

### Účel využívání produktů (`UsagePurposeCode`)
- `INCOME_OPERATIONS`: Příjmové operace.
- `CASH_TRANSACTIONS`: Hotovostní transakce.
- `DAILY_EXPENSES`: Běžné výdaje.
- `CREDIT_PRODUCTS_USAGE`: Využívání úvěrových produktů.
- `CAPITAL_ACCUMULATION`: Tvorba kapitálu.

### Skupiny zemí pro platby (`PaymentCountryGroupCode`)
- `INSIDE_EUROPE`: V rámci Evropy.
- `OUTSIDE_EUROPE`: Mimo Evropu.

### Kódy regulatorních dokumentů (`RegulatoryDocumentCode`)
- `PSI`: Předsmluvní informace.
- `VOP`: Všeobecné obchodní podmínky.
- `SAP`: Sazebník poplatků.

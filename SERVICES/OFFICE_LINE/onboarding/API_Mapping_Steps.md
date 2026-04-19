# Mapování API operací na kroky Onboardingu

Identifikace konkrétní API operace volané v jednotlivých krocích onboardingu na základě vizuálních návrhů (Figma) a technické specifikace REST ONB API.

## Přehled kroků a volání

| Krok (Screenshot) | Název obrazovky | Hlavní API operace | Popis akce | Vstupní data (Request) | Výstupní data (Response) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **1. intro.png** | Intro | `POST /v1/onboarding` | Inicializace procesu, získání `processId` a `token`. | `onboardingCountry`, `deviceInfo`, `pushIdentifier` | `processId`, `token`, `expiresAt`, `packageVersion`, `zenIdProfile` |
| **2. kontaktní údaje - telefonní čílo.png** | Telefonní číslo | `POST /v1/onboarding/{processId}/phone`<br>`POST /v1/onboarding/{processId}/phone/otp/verify` | Zadání čísla, zaslání SMS OTP a jeho následné ověření. | `phoneNumber`<br>`code` (OTP) | `otp` (expiresIn, cooldown, attempts)<br>`step`, `status` (COMPLETED) |
| **3. kontaktní údaje - email.png** | E-mail | `POST /v1/onboarding/{processId}/email`<br>`POST /v1/onboarding/{processId}/email/otp/verify` | Zadání e-mailu, zaslání e-mail OTP a jeho následné ověření. | `email`<br>`code` (OTP) | `otp` (expiresIn, cooldown, attempts)<br>`step`, `status` (COMPLETED) |
| **4. biometrické údaje.png** | Souhlas s biometrikou | (Žádné přímé volání) | Informační obrazovka před spuštěním ZenID SDK. | - | - |
| **5. ověření identity.png** | OCR a Liveness | `POST /v1/onboarding/{processId}/identity/init`<br>`POST /v1/onboarding/{processId}/identity/sample`<br>`POST /v1/onboarding/{processId}/identity/finalize`<br>`PUT /v1/onboarding/{processId}/identity/mined-data/confirmation` | Inicializace ZenID, upload vzorků (doklad, selfie), finalizace a potvrzení vytěžených dat. | `sdkChallengeToken`<br>`kind`, `file`<br>(finalize nemá body)<br>`givenName`, `familyName`, `address`, ... | `sdkInitPayload`<br>`kind`, `state`<br>`minedData`, `decision`<br>`step`, `status` (COMPLETED) |
| **6. regulační prohlášení.png** | PEP a sankce | (Součást `data/submit`) | Uživatel deklaruje, zda je politicky exponovanou osobou. | (Viz krok 9) | (Viz krok 9) |
| **7. údaje o příjmech a majetku.png** | AML údaje 1 | (Součást `data/submit`) | Sběr informací o zdroji příjmů. | (Viz krok 9) | (Viz krok 9) |
| **8. účel a způsob využívání produktů.png** | AML údaje 2 | (Součást `data/submit`) | Sběr informací o účelu vztahu. | (Viz krok 9) | (Viz krok 9) |
| **9. prohlášení klienta.png** | Souhlasy | `POST /v1/onboarding/{processId}/data/submit` | Odeslání všech AML dat, prohlášení a souhlasů k vyhodnocení. | `payloadVersion`, `data` (biometricDataProcessing, plannedInvestmentOverLimit, regulatoryStatements, privacyConsents, incomeAndAssets, productUsage) | `step`, `status` (COMPLETED) |
| **10. smluvní dokumenty.png** | Dokumentace | `POST /v1/onboarding/{processId}/documents/contracts`<br>`GET /v1/onboarding/{processId}/documents/contracts/{documentId}` | Vygenerování smluvní dokumentace a její stažení pro náhled. | (contracts nemá body)<br>(path: documentId) | `documents` (documentId, name, fileName, documentHash)<br>`application/pdf` (binary) |
| **11. podpis a zpracování.png** | Podpis | `POST /v1/onboarding/{processId}/documents/contracts/{documentId}/otp/request`<br>`POST /v1/onboarding/{processId}/documents/contracts/{documentId}/otp/verify` | Vyžádání podpisového OTP a potvrzení podpisu smlouvy. | (request nemá body)<br>`code` (OTP) | `202 Accepted`<br>`step`, `status` (COMPLETED) |
| **12. další produkty.png** | Výběr produktů | `POST /v1/onboarding/{processId}/products` | Volitelný výběr doplňkových produktů/účtů. | `products` (productType, currency) | `step`, `status` (COMPLETED) |
| **13. dokončení onboardingu - autetizace.png** | Nastavení hesla | `GET /v1/onboarding/{processId}/credentials/public-key`<br>`POST /v1/onboarding/{processId}/credentials` | Získání šifrovacího klíče a nastavení hesla pro budoucí přístup. | (public-key nemá body)<br>`password` (encrypted) | `publicKey`<br>`step`, `status` (COMPLETED) |
| **14. dokončení onboardingu - povolení interakcí.png** | Notifikace | `PUT /v1/onboarding/{processId}/push-registration` | (Volitelné) Registrace push tokenu pro oznámení o dokončení. | `pushIdentifier` | `204 No Content` |
| **15. dokončení onboardingu - aktivace.png** | Aktivace klíče | `GET /v1/onboarding/{processId}/status`<br>`POST /v1/onboarding/{processId}/token/activate` | Čekání na stav `READY_FOR_TOKEN_ACTIVATION` a spuštění aktivace mobilního klíče. | (status nemá body)<br>(activate nemá body) | `step`, `status` (READY_FOR_TOKEN_ACTIVATION)<br>`username`, `activationOtp`, `activationGuid` |
| **16. dokončení onboardingu - dashboard.png** | Hotovo | (Žádné volání) | Úspěšné dokončení, uživatel je v aplikaci. | - | - |

## Poznámky k implementaci
- **Autorizace:** Všechny endpointy (kromě prvního `POST /v1/onboarding`) vyžadují `Authorization: Bearer <token>`.
- **Resend:** Kdykoliv je vyžadováno OTP, lze použít `POST /v1/onboarding/{processId}/otp/resend` pro znovuzaslání.
- **Status:** Průběžně lze kontrolovat stav procesu pomocí `GET /v1/onboarding/{processId}/status`.
- **Zpracování na pozadí:** Po kroku 11 (Podpis) nebo 13 (Heslo) dochází k asynchronnímu zakládání v systémech Centris a AXA.

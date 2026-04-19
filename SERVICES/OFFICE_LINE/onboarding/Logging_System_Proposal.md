# Návrh systému sběru logů pro Onboarding API

Tento dokument definuje systém sběru logů pro backendové Onboarding API v PrivatBance. Cílem je zajistit data pro business monitoring (konverzní funnel), aplikační monitoring (výkon a chyby) a splnění auditních požadavků.

## 1. Cíle a principy
- **End-to-End sledování:** Každý proces onboardingu je sledovatelný od prvního requestu až po finální aktivaci produktu.
- **Strukturované logování:** Logy jsou generovány ve formátu JSON a splňují standardy definované v `Koncepce_logovani_PrivatBanka.md`.
- **Oddělení business a technických dat:** Rozlišení mezi provozními logy (debug/info) a business eventy (milestones).

## 2. Identifikátory a Korelace
Pro efektivní propojování logů jsou povinné tyto identifikátory v každém log záznamu:
- `correlationId`: Technické ID requestu (předávané v hlavičce `X-Correlation-ID`), umístěné v top-level úrovni logu.
- `processId`: Business ID procesu (např. GUID vygenerovaný v kroku 1), umístěné uvnitř objektu `message`.
- `sessionId`: ID session uživatele (pokud se liší od `processId`), umístěné uvnitř objektu `message`.

## 3. Struktura logu (Atributy)
Logy jsou navrženy jako dvouúrovňové pro zajištění kompatibility napříč systémy. První úroveň obsahuje metadata společná pro celou banku, pole `message` pak obsahuje detailní JSON s daty konkrétního systému.

### 3.1 Top-level pole (Společná)
| Atribut | Popis | Příklad |
| :--- | :--- | :--- |
| `timestamp` | Čas události v UTC (ISO8601) | `2026-04-17T21:30:15.123Z` |
| `level` | Úroveň logování (Info, Warn, Error, Audit) | `Info` |
| `system` | Identifikátor systému/komponenty | `office-line` |
| `correlationId` | Technické ID requestu (GUID) | `550e8400-e29b-41d4-a716...` |
| `message` | **JSON objekt** obsahující systémově specifická data | `{ "processId": "...", ... }` |

### 3.2 Pole uvnitř objektu `message` (Onboarding specifická)
Kromě `processId` budou onboarding logy v objektu `message` obsahovat:

| Atribut | Popis | Příklad |
| :--- | :--- | :--- |
| `processId` | Business ID procesu | `ONB-2026-000456` |
| `operation` | Název operace (např. dle `Koncepce_logovani`) | `FinalizeIdentity` |
| `onboarding.step` | Název kroku (viz mapování níže) | `IDENTITY_CAPTURE` |
| `onboarding.substep` | Detailní operace v rámci kroku | `ZENID_LIVENESS_CHECK` |
| `onboarding.status` | Stav operace | `STARTED`, `COMPLETED`, `FAILED` |
| `onboarding.duration_ms` | Doba trvání operace v milisekundách | `1250` |
| `onboarding.error_code` | Kód chyby (pokud nastala) | `OTP_EXPIRED` |
| `onboarding.client_type` | Typ klienta / země | `CZ_RESIDENT` |
| `onboarding.channel` | Kanál (Mobile/Web) | `MOBILE` |
| `onboarding.client.gender` | Pohlaví (ne-GDPR statistika) | `M`, `F`, `O` |
| `onboarding.client.age_group` | Věková skupina (vypočtená) | `25-34` |
| `onboarding.client.nationality` | Státní příslušnost (ISO kód) | `CZ` |

## 4. Mapování událostí na kroky procesu

| Krok | API Endpoint | Business Event | Klíčová metadata k logování |
| :--- | :--- | :--- | :--- |
| **1. Intro** | `POST /v1/onboarding` | `PROCESS_STARTED` | `channel`, `deviceInfo`, `appVersion` |
| **2. Telefon** | `.../phone/otp/verify` | `PHONE_VERIFIED` | `attemptsCount`, `durationMs` |
| **3. E-mail** | `.../email/otp/verify` | `EMAIL_VERIFIED` | `domain` (anonymizovaně) |
| **5. Identita** | `.../identity/finalize` | `IDENTITY_VERIFIED` | `zenid.decision`, `zenid.confidenceScore` |
| **9. Souhlasy** | `.../data/submit` | `AML_DATA_SUBMITTED` | `aml.result` (OK/REVIEW), `riskLevel` |
| **11. Podpis** | `.../otp/verify` | `CONTRACT_SIGNED` | `documentCount`, `signatureType` |
| **13. Heslo** | `POST /v1/credentials` | `CREDENTIALS_SET` | - |
| **15. Aktivace** | `.../token/activate` | `ONBOARDING_COMPLETED` | `productTypes`, `totalProcessTimeSec` |

## 5. Business Monitoring (Kibana Dashboardy)
Systém bude poskytovat data pro tyto vizualizace:
1. **Conversion Funnel:** Procento uživatelů přecházejících mezi kroky 1 -> 5 -> 9 -> 11 -> 15.
2. **Drop-off Analysis:** Identifikace nejčastějšího bodu opuštění procesu.
3. **Zpracování Identity:** Průměrné skóre ZenID a poměr automatických vs. manuálních schválení.
4. **Časová náročnost:** Jak dlouho trvá průměrný onboarding (celkově i po jednotlivých krocích).

## 6. Aplikační Monitoring a Alerting
Nad logy budou definovány tyto alerty:
- **High Error Rate:** Pokud víc než 5 % requestů v kroku "Identita" končí chybou 5xx.
- **Latency Spike:** Pokud P95 latence u `data/submit` překročí 10 sekund.
- **ZenID Unavailability:** Detekce výpadku integrace s Trask ZenID.
- **OTP Delivery Failure:** Zvýšený počet neúspěšných verifikací SMS kódu.

## 7. Bezpečnost a GDPR
- **Maskování OÚ:** Logy nesmí obsahovat jména, rodná čísla ani nehashované e-maily/telefony (v souladu s `Koncepce_logovani_PrivatBanka.md`).
- **Auditní stopa:** Každé volání `GET` na klientské dokumenty musí být logováno s úrovní `Audit` včetně identifikace volajícího subjektu.
- **Retence:** Business eventy (milestones) budou uchovávány 2 roky pro analýzu trendů, detailní technické logy 30 dní.

## 8. Příklad JSON logu (Business Event)
```json
{
  "timestamp": "2026-04-17T21:30:15.123Z",
  "level": "Info",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440000",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "FinalizeIdentity",
    "description": "Identity verification completed successfully for process ONB-2026-000456",
    "onboarding": {
      "step": "IDENTITY_CAPTURE",
      "substep": "ZENID_FINALIZE",
      "status": "COMPLETED",
      "duration_ms": 2450,
      "client": {
        "gender": "M",
        "age_group": "35-44",
        "nationality": "CZ"
      },
      "zenid": {
        "decision": "APPROVED",
        "confidenceScore": 0.98
      }
    }
  }
}
```

## 9. Implementace ve zdrojovém kódu (.NET)

Pro generování logů v požadovaném formátu přímo z aplikací (Office-Line, API Gateway) doporučujeme tyto přístupy dle použité knihovny.

### 9.1 Serilog (Doporučeno)
Serilog je ideální pro strukturované logování. Pole `message` lze naplnit vnořeným objektem.

**Konfigurace:**
```csharp
Log.Logger = new LoggerConfiguration()
    .WriteTo.Console(new ExpressionTemplate(
        "{ {@timestamp, @level, system: 'office-line', correlationId, message: @rest} }\n"))
    .Enrich.FromLogContext()
    .CreateLogger();
```

**Použití v kódu:**
```csharp
var onboardingData = new {
    processId = "ONB-2026-000456",
    operation = "FinalizeIdentity",
    onboarding = new {
        step = "IDENTITY_CAPTURE",
        status = "COMPLETED",
        duration_ms = 2450
    }
};

Log.Information("{@message}", onboardingData);
```

### 9.2 Log4net
Pro starší komponenty využívající Log4net je nutné použít custom `Layout`, který serializuje log událost do JSON.

**App.config / log4net.config:**
```xml
<appender name="JsonFileAppender" type="log4net.Appender.RollingFileAppender">
    <file value="logs/office-line.json.log" />
    <layout type="log4net.Layout.SerializedLayout, log4net.Ext.Json">
        <decorator type="log4net.Layout.Decorators.StandardTypesDecorator, log4net.Ext.Json" />
        <member value="timestamp:utcdate" />
        <member value="level:level" />
        <member value="system:literal{office-line}" />
        <member value="correlationId:property{correlationId}" />
        <member value="message:messageobject" />
    </layout>
</appender>
```

### 9.3 Manuální serializace (Middleware)
Pokud aplikace nepoužívá pokročilý logging framework, lze využít `System.Text.Json` pro vytvoření obálky.

```csharp
public class LogEnvelope {
    public string timestamp { get; set; } = DateTime.UtcNow.ToString("O");
    public string level { get; set; }
    public string system { get; set; } = "office-line";
    public string correlationId { get; set; }
    public object message { get; set; }
}
```

## 10. Předávání logů do Elasticu

Existují dva hlavní způsoby, jak tyto JSON logy z aplikace dostat do Elasticu:

1.  **Filebeat / Elastic Agent (Sidecar):** Aplikace zapisuje JSON do souboru na disk a agent jej odesílá. Toto je nejbezpečnější metoda (při výpadku sítě jsou logy na disku).
    - V konfiguraci agenta nastavte `parsers: [{ndjson: {}}]`.
2.  **Direct Push (HTTP Sink):** Aplikace posílá logy přímo na Ingest endpoint Elasticu přes HTTP.
    - Vyžaduje knihovnu `Elastic.Serilog.Sinks` nebo podobnou.
    - Riziko ztráty dat při nedostupnosti sítě, pokud není implementována lokální fronta.

## 11. Detailní příklady JSON logů pro všechny kroky
Tato sekce obsahuje příklady logů pro každou API operaci definovanou v `API_Mapping_Steps.md`. Všechny logy sledují dvouúrovňovou strukturu (Top-level + Message).

### 11.1 Krok 1: Intro (Inicializace procesu)
**Operace:** `POST /v1/onboarding`
```json
{
  "timestamp": "2026-04-17T21:30:00.000Z",
  "level": "Info",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440001",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "InitiateOnboarding",
    "description": "New onboarding process started",
    "onboarding": {
      "step": "INTRO",
      "status": "COMPLETED",
      "duration_ms": 150,
      "channel": "MOBILE",
      "deviceInfo": "iPhone 15, iOS 17.2",
      "country": "CZ"
    }
  }
}
```

### 11.2 Krok 2: Telefonní číslo
**Operace:** `POST /v1/onboarding/{id}/phone` (Odeslání OTP)
```json
{
  "timestamp": "2026-04-17T21:31:10.000Z",
  "level": "Info",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440002",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "RequestPhoneOtp",
    "onboarding": {
      "step": "CONTACT_PHONE",
      "substep": "OTP_SENT",
      "status": "COMPLETED",
      "duration_ms": 450
    }
  }
}
```
**Operace:** `POST /v1/onboarding/{id}/phone/otp/verify` (Ověření OTP)
```json
{
  "timestamp": "2026-04-17T21:31:45.000Z",
  "level": "Info",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440003",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "VerifyPhoneOtp",
    "onboarding": {
      "step": "CONTACT_PHONE",
      "substep": "OTP_VERIFIED",
      "status": "COMPLETED",
      "duration_ms": 120,
      "attemptsCount": 1
    }
  }
}
```

### 11.3 Krok 3: E-mail
**Operace:** `POST /v1/onboarding/{id}/email/otp/verify`
```json
{
  "timestamp": "2026-04-17T21:32:30.000Z",
  "level": "Info",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440005",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "VerifyEmailOtp",
    "onboarding": {
      "step": "CONTACT_EMAIL",
      "substep": "OTP_VERIFIED",
      "status": "COMPLETED",
      "duration_ms": 110,
      "emailDomain": "seznam.cz"
    }
  }
}
```

### 11.4 Krok 5: Ověření identity (ZenID)
**Operace:** `POST /v1/onboarding/{id}/identity/finalize` (Výsledek OCR/Liveness)
```json
{
  "timestamp": "2026-04-17T21:35:00.000Z",
  "level": "Info",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440010",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "FinalizeIdentity",
    "onboarding": {
      "step": "IDENTITY_CAPTURE",
      "substep": "ZENID_FINALIZE",
      "status": "COMPLETED",
      "duration_ms": 3200,
      "client": {
        "gender": "F",
        "age_group": "25-34",
        "nationality": "CZ"
      },
      "zenid": {
        "decision": "APPROVED",
        "confidenceScore": 0.992,
        "documentType": "ID_CARD_CZ"
      }
    }
  }
}
```
**Operace:** `PUT /v1/onboarding/{id}/identity/mined-data/confirmation`
```json
{
  "timestamp": "2026-04-17T21:36:15.000Z",
  "level": "Info",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440012",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "ConfirmMinedData",
    "onboarding": {
      "step": "IDENTITY_CAPTURE",
      "substep": "DATA_CONFIRMATION",
      "status": "COMPLETED",
      "duration_ms": 850
    }
  }
}
```

### 11.5 Krok 9: Souhlasy a AML data
**Operace:** `POST /v1/onboarding/{id}/data/submit`
```json
{
  "timestamp": "2026-04-17T21:38:20.000Z",
  "level": "Info",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440015",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "SubmitAmlData",
    "onboarding": {
      "step": "REGULATORY_DATA",
      "status": "COMPLETED",
      "duration_ms": 1850,
      "aml": {
        "riskLevel": "LOW",
        "pepStatus": false,
        "sanctionsCheck": "CLEAN"
      }
    }
  }
}
```

### 11.6 Krok 10: Dokumentace
**Operace:** `GET /v1/onboarding/{id}/documents/contracts/{docId}` (Náhled PDF)
```json
{
  "timestamp": "2026-04-17T21:39:40.000Z",
  "level": "Audit",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440018",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "DownloadContractPreview",
    "description": "User accessed contract PDF for preview",
    "onboarding": {
      "step": "DOCUMENTATION",
      "substep": "PREVIEW_DOWNLOAD",
      "status": "COMPLETED",
      "documentId": "DOC-998273"
    }
  }
}
```

### 11.7 Krok 11: Podpis smlouvy
**Operace:** `POST /v1/onboarding/{id}/documents/contracts/{docId}/otp/verify`
```json
{
  "timestamp": "2026-04-17T21:40:15.000Z",
  "level": "Audit",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440020",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "SignContract",
    "description": "User signed the contract document",
    "onboarding": {
      "step": "CONTRACT_SIGNATURE",
      "status": "COMPLETED",
      "duration_ms": 2100,
      "signatureType": "SMS_OTP",
      "documentId": "DOC-998273"
    }
  }
}
```

### 11.8 Krok 13: Nastavení hesla
**Operace:** `POST /v1/onboarding/{id}/credentials`
```json
{
  "timestamp": "2026-04-17T21:42:10.000Z",
  "level": "Info",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440025",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "SetCredentials",
    "onboarding": {
      "step": "CREDENTIALS_SETUP",
      "status": "COMPLETED",
      "duration_ms": 1200
    }
  }
}
```

### 11.9 Krok 15: Dokončení a Aktivace
**Operace:** `POST /v1/onboarding/{id}/token/activate`
```json
{
  "timestamp": "2026-04-17T21:45:00.000Z",
  "level": "Info",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440030",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "ActivateToken",
    "description": "Onboarding completed, mobile key activated",
    "onboarding": {
      "step": "ACTIVATION",
      "status": "COMPLETED",
      "duration_ms": 5400,
      "totalProcessTimeSec": 900
    }
  }
}
```

### 11.10 Doplňkové operace
**Krok 12 (Výběr produktů):** `POST /v1/onboarding/{id}/products`
```json
{
  "timestamp": "2026-04-17T21:41:00.000Z",
  "level": "Info",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440022",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "SelectProducts",
    "onboarding": {
      "step": "PRODUCT_SELECTION",
      "status": "COMPLETED",
      "duration_ms": 450,
      "products": ["CURRENT_ACCOUNT_CZK", "SAVINGS_ACCOUNT"]
    }
  }
}
```

**Krok 14 (Push notifikace):** `PUT /v1/onboarding/{id}/push-registration`
```json
{
  "timestamp": "2026-04-17T21:43:00.000Z",
  "level": "Info",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440028",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "RegisterPush",
    "onboarding": {
      "step": "PUSH_REGISTRATION",
      "status": "COMPLETED",
      "duration_ms": 150
    }
  }
}
```

**Křížová kontrola stavu:** `GET /v1/onboarding/{id}/status`
```json
{
  "timestamp": "2026-04-17T21:44:30.000Z",
  "level": "Info",
  "system": "office-line",
  "correlationId": "550e8400-e29b-41d4-a716-446655440029",
  "message": {
    "processId": "ONB-2026-000456",
    "operation": "GetStatus",
    "onboarding": {
      "step": "STATUS_POLLING",
      "status": "COMPLETED",
      "currentStep": "READY_FOR_TOKEN_ACTIVATION"
    }
  }
}
```

## 12. Příklady vyhledávání v Kibaně (KQL) pro Business KPI

Tato sekce obsahuje konkrétní KQL (Kibana Query Language) dotazy pro filtrování logů v nástroji Kibana (Discovery, Lens, Dashboards). Dotazy využívají dvouúrovňovou strukturu `message.onboarding.*`.

### 12.1 Sledování konverzního funnelu (Milestones)
- **Zahájení procesu (Top of Funnel):**
  `message.operation: "InitiateOnboarding"`
- **Dokončení celého procesu (Conversion):**
  `message.onboarding.step: "ACTIVATION" and message.onboarding.status: "COMPLETED"`
- **Uživatelé, kteří se dostali k podpisu smlouvy:**
  `message.onboarding.step: "CONTRACT_SIGNATURE"`
- **Uživatelé, kteří si vybrali produkty:**
  `message.onboarding.step: "PRODUCT_SELECTION"`

### 12.2 Analýza identity a KYC (ZenID KPI)
- **Automaticky schválená identita (Strait-through processing):**
  `message.onboarding.zenid.decision: "APPROVED"`
- **Zamítnutá identita (OCR/Liveness failure):**
  `message.onboarding.zenid.decision: "REJECTED"`
- **Nízké skóre důvěryhodnosti (např. pod 80 %):**
  `message.onboarding.zenid.confidenceScore < 0.8`
- **Distribuce typů dokladů:**
  `exists(message.onboarding.zenid.documentType)` (následně použít aggregaci na toto pole)

### 12.3 AML a Regulační metriky
- **Klienti s vysokým rizikem (AML High Risk):**
  `message.onboarding.aml.riskLevel: "HIGH"`
- **Politicky exponované osoby (PEP):**
  `message.onboarding.aml.pepStatus: true`
- **Neúspěšný check sankčních seznamů:**
  `not message.onboarding.aml.sanctionsCheck: "CLEAN"`

### 12.4 Provozní metriky a Latence (SLA Monitoring)
- **Jakákoliv operace trvající déle než 5 sekund:**
  `message.onboarding.duration_ms > 5000`
- **Pomalé ověřování identity (vliv na UX):**
  `message.onboarding.step: "IDENTITY_CAPTURE" and message.onboarding.duration_ms > 3000`
- **Chybové stavy a pády procesu:**
  `level: "Error" or message.onboarding.status: "FAILED"`

### 12.5 Support a Diagnostika (Tracing)
- **Sledování celého průchodu procesem pro jednoho klienta:**
  `message.processId: "ONB-2026-000456"`
- **Korelace technických logů napříč systémy pomocí CorrelationId:**
  `correlationId: "550e8400-e29b-41d4-a716-446655440030"`
- **Vyhledání logů pro konkrétního e-mailového poskytovatele:**
  `message.onboarding.emailDomain: "gmail.com"`

### 12.6 Analýza opuštění procesu (Drop-off Analysis)
- **Uživatelé, kteří dokončili e-mail, ale nezačali identitu:**
  `message.onboarding.step: "CONTACT_EMAIL" and message.onboarding.status: "COMPLETED" and not message.onboarding.step: "IDENTITY_CAPTURE"`
- **Procesy, které byly zahájeny (Intro), ale nikdy nedošly k podpisu:**
  `message.operation: "InitiateOnboarding" and not message.onboarding.step: "CONTRACT_SIGNATURE"`
- **Identifikace bodu selhání pro konkrétní typ klienta:**
  `message.onboarding.client_type: "CZ_RESIDENT" and message.onboarding.status: "FAILED"`

### 12.7 Uživatelská zkušenost (UX Metrics)
- **Opakované pokusy o zadání OTP (potenciální problém s doručitelností):**
  `message.onboarding.attemptsCount > 2`
- **Doba strávená v celém procesu (nad 15 minut):**
  `message.onboarding.totalProcessTimeSec > 900`
- **Příliš dlouhá pauza mezi odesláním a verifikací OTP (v sekundách):**
  `message.onboarding.duration_ms > 120000` (nad 2 minuty)
- **Distribuce mobilních zařízení pro optimalizaci UI:**
  `exists(message.onboarding.deviceInfo)` (následně agregace přes lens)

### 12.8 Produktové a Marketingové KPI
- **Počet vybraných produktů v jednom procesu:**
  `message.onboarding.step: "PRODUCT_SELECTION" and message.onboarding.products: *`
- **Zájem o spořicí účet v rámci onboardingu:**
  `message.onboarding.products: "SAVINGS_ACCOUNT"`
- **Konverzní poměr podle země klienta:**
  `message.onboarding.country: "CZ"`
- **Vliv verze aplikace na stabilitu onboardingu:**
  `message.onboarding.appVersion: "1.2.0"`

### 12.9 Specifické chyby a Troubleshooting
- **Expirované OTP kódy (pomalá odezva uživatele nebo brány):**
  `message.onboarding.error_code: "OTP_EXPIRED"`
- **Problémy s nahráváním dokumentů (příliš velké soubory):**
  `message.onboarding.error_code: "FILE_TOO_LARGE"`
- **Neúspěšné ověření PIN/Hesla při nastavování:**
  `message.onboarding.step: "CREDENTIALS_SETUP" and message.onboarding.status: "FAILED"`

### 12.10 Demografická analýza (Non-GDPR)
- **Rozdělení klientů podle pohlaví:**
  `exists(message.onboarding.client.gender)` (agregace nad tímto polem)
- **Počet mladých klientů (18-24 let):**
  `message.onboarding.client.age_group: "18-24"`
- **Poměr zahraničních klientů (non-CZ):**
  `not message.onboarding.client.nationality: "CZ"`
- **Konverzní poměr žen v mobilní aplikaci:**
  `message.onboarding.client.gender: "F" and message.onboarding.channel: "MOBILE" and message.onboarding.step: "ACTIVATION"`

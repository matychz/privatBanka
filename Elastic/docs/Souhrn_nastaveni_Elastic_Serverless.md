### Souhrn nastavení Elastic Serverless pro zpracování custom logů

Tento návod popisuje proces nastavení Elasticu pro sběr, parsování a ukládání vlastních aplikačních logů s využitím moderního přístupu Fleet a Elastic Agent (verze 8.x/9.x).

---

### 1. Vytvoření Elastic Serverless projektu
Před samotným nastavením sběru logů je nutné mít vytvořený **Serverless Project** v prostředí Elastic Cloud.

#### A. Přes Elastic Cloud (přímá registrace)
1. Přihlaste se do [Elastic Cloud Console](https://cloud.elastic.co/).
2. Klikněte na **Create project**.
3. Vyberte typ projektu **Observability** (vhodné pro logy a metriky).
4. Zadejte **Project Name** (např. `PrivatBanka-Logging`).
5. Vyberte cloudového poskytovatele (**Azure**) a region (např. `Germany West Central`).
6. Klikněte na **Create project**. Elastic automaticky vygeneruje endpointy a přístupové údaje.

#### B. Přes Azure Marketplace (integrovaný billing)
Pokud má banka existující Azure kontrakt (MACC), je výhodnější vytvořit instanci přímo přes Azure Portal:
1. V Azure Portalu vyhledejte **Elasticsearch (Elastic Cloud) Service**.
2. Klikněte na **Create**.
3. Vyberte Resource Group a název prostředku.
4. V sekci **Plan** vyberte odpovídající serverless plán.
5. Po vytvoření prostředku klikněte na **Manage changes in Elastic Cloud**.
6. Dále pokračujte vytvořením projektu typu **Observability** dle bodu A.

---

### 2. Koncepce indexů: `logs-<dataset>-<namespace>`
V Elasticu jsou data ukládána do tzv. **Data Streamů**. Názvy těchto streamů (a podkladových indexů) se automaticky skládají ze tří částí:

1.  **Type (`logs`):** Fixní předpona pro logová data.
2.  **Dataset (`<dataset>`):** Název aplikace nebo logického celku (např. `api.gw`, `ibconsole`). Definuje strukturu dat.
3.  **Namespace (`<namespace>`):** Označení prostředí (např. `dev`, `test`, `prod`). Slouží k logické izolaci dat různých prostředí.

**Příklad:** Logy z API Gateway na vývojovém prostředí budou v indexu `logs-api.gw-dev`.

---

### 3. Vytvoření Agent Policy
**Agent Policy** je centrální konfigurace, kterou agenti stahují z Fleet serveru. Určuje, co mají agenti sbírat.

1.  V Kibaně přejděte na **Management** -> **Fleet** -> **Agent Policies**.
2.  Klikněte na **Create agent policy**.
3.  **Doporučení:** Vytvořte samostatnou politiku pro každou kombinaci komponenty a prostředí (např. `API-Gateway-DEV`).
4.  V **Settings** politiky nastavte **Default namespace** (např. `dev`). Tím zajistíte, že všechna data z této politiky automaticky dostanou správný tag prostředí.

---

### 4. Integrace v Agent Policy (Custom Logs)
Do vytvořené politiky je třeba přidat konkrétní úkol – sběr souborů.

1.  V detailu politiky klikněte na **Add integration** a vyberte **Custom Logs**.
2.  **Integration name:** Např. `api-gw-logs-collection`.
3.  **Log file path:** Absolutní cesta k logům (např. `C:\App\Logs\*.log`).
4.  **Dataset name:** Zadejte název datasetu (např. `api.gw`).
5.  **Advanced options - Encoding:** Pokud logy obsahují diakritiku (např. ze systému Windows), nastavte `windows-1250`.
6.  **Custom configurations:** Zde se později propojí Ingest Pipeline.

---

### 5. Vytvoření Ingest Pipeline s Grok procesorem
**Ingest Pipeline** transformuje surový text logu na strukturovaný JSON ještě před jeho uložením do indexu. Tato pipeline zajišťuje, že se surový log rozdělí na jednotlivá pole a v poli `message` zůstane pouze čistý text bez redundantních dat.

#### Architektura zpracování (Logika)
Pipeline je navržena jako sekvence kroků (procesorů), které postupně transformují data:
1.  **Základní rozklad (Grok):** Identifikuje fixní části logu (datum, log level, ID požadavku, název loggeru).
2.  **Normalizace času (Date):** Převod textového datumu na standardní `@timestamp` v UTC.
3.  **Hloubková extrakce (Grok):** Hledání specifických vzorů pro `processId`, `correlationId` nebo `duration`.
4.  **Typování dat (Convert):** Zajištění, že číselné hodnoty (např. ms) jsou uloženy jako čísla.
5.  **Anonymizace (GDPR):** Detekce e-mailových adres a jejich nahrazení bezpečným MD5 hashem.
6.  **Čištění (Script):** Odstranění technického "šumu" z pole `message`.
7.  **Metadata:** Přidání statických polí a odstranění pomocných dočasných polí.

#### Kompletní JSON konfigurace (ibconsole-pipeline)
Tento JSON kód vložte v **Stack Management** -> **Ingest Pipelines** -> **Create pipeline** -> **Import processors** (nebo **Edit as JSON**).

```json
{
  "description": "Pipeline pro parsování logů ibconsole - čištění message a extrakce ID",
  "processors": [
    {
      "grok": {
        "description": "1. Krok: Odstranění času, levelu a loggeru z pole message",
        "field": "message",
        "patterns": [
          "^(?<temp_timestamp>%{YEAR}-%{MONTHNUM}-%{MONTHDAY} %{TIME})\\s+%{LOGLEVEL:log.level}\\s+%{NUMBER:requestId}\\s+\\[%{DATA:logger}\\]\\s+%{GREEDYDATA:message}",
          "%{GREEDYDATA:message}"
        ],
        "ignore_failure": true
      }
    },
    {
      "date": {
        "description": "2. Krok: Převod času na @timestamp",
        "field": "temp_timestamp",
        "formats": [
          "yyyy-MM-dd HH:mm:ss,SSS"
        ],
        "timezone": "Europe/Prague",
        "target_field": "@timestamp"
      }
    },
    {
      "grok": {
        "description": "3. Krok: Extrakce ID, operací a trvání",
        "field": "message",
        "patterns": [
          "Activity '%{DATA:operation}' Finished\\s*-\\s*%{NUMBER:duration:long}\\s*ms\\s*-\\s*traceId=%{UUID:correlationId}",
          "Activity '%{DATA:operation}' Finished\\s*-\\s*%{NUMBER:duration:long}\\s*ms\\s*-\\s*process\\s+%{WORD:processId}",
          "Activity '%{DATA:operation}' Finished\\s*-\\s*%{NUMBER:duration:long}\\s*ms",
          "Finished\\s*-\\s*%{NUMBER:duration:long}\\s*ms",
          "Activity '%{DATA:operation}' %{DATA:result}\\s*-\\s*%{GREEDYDATA:message_detail}\\s*-\\s*traceId=%{UUID:correlationId}",
          "Activity '%{DATA:operation}' %{DATA:result}\\s*-\\s*%{GREEDYDATA:message_detail}\\s*-\\s*process\\s+%{WORD:processId}",
          "Activity '%{DATA:operation}' %{DATA:result}\\s*-\\s*traceId=%{UUID:correlationId}",
          "Activity '%{DATA:operation}' %{DATA:result}\\s*-\\s*process\\s+%{WORD:processId}",
          "Onboarding\\.%{DATA:operation}: (?:Onboarding step set to %{DATA:step} in )?process %{WORD:processId}"
        ],
        "ignore_failure": true
      }
    },
    {
      "convert": {
        "description": "Zajištění, aby duration bylo číslo pro agregaci",
        "field": "duration",
        "type": "long",
        "ignore_missing": true
      }
    },
    {
      "convert": {
        "description": "Zajištění správného typu pole log.level pro agregaci",
        "field": "log.level",
        "type": "string",
        "ignore_missing": true
      }
    },
    {
      "grok": {
        "description": "Anonymizace A: Extrakce e-mailu do dočasného pole",
        "field": "message",
        "patterns": ["%{EMAILADDRESS:tmp_email_raw}"],
        "ignore_failure": true
      }
    },
    {
      "set": {
        "description": "Anonymizace B: Příprava pro hashování",
        "field": "tmp_email_norm",
        "copy_from": "tmp_email_raw",
        "ignore_empty_value": true
      }
    },
    {
      "lowercase": {
        "description": "Anonymizace C: Normalizace na malá písmena",
        "field": "tmp_email_norm",
        "ignore_missing": true
      }
    },
    {
      "fingerprint": {
        "description": "Anonymizace D: Výpočet MD5 hashe",
        "fields": ["tmp_email_norm"],
        "target_field": "tmp_email_hash",
        "method": "MD5",
        "ignore_missing": true
      }
    },
    {
      "script": {
        "description": "Anonymizace E: Nahrazení e-mailu hashem",
        "if": "ctx.tmp_email_raw != null && ctx.tmp_email_hash != null",
        "source": "ctx.message = ctx.message.replace(ctx.tmp_email_raw, '#EMAIL#' + ctx.tmp_email_hash + '#EMAIL#')"
      }
    },
    {
      "script": {
        "description": "4. Krok: Vyčištění pole message od již extrahovaných ID a trvání",
        "lang": "painless",
        "source": "if (ctx.message != null) { if (ctx.correlationId != null) { ctx.message = ctx.message.replace(' - traceId=' + ctx.correlationId, ''); } if (ctx.processId != null) { ctx.message = ctx.message.replace(' process ' + ctx.processId, ''); } if (ctx.duration != null) { String durStr = ctx.duration.toString(); ctx.message = ctx.message.replace(' - ' + durStr + ' ms', ''); } }"
      }
    },
    {
      "set": {
        "description": "Nastavení metadat systému",
        "field": "system",
        "value": "ibconsole"
      }
    },
    {
      "remove": {
        "description": "5. Krok: Odstranění pomocných polí",
        "field": [
          "temp_timestamp",
          "tmp_email_raw",
          "tmp_email_norm",
          "tmp_email_hash"
        ],
        "ignore_missing": true
      }
    }
  ]
}
```

**Propojení:** Název této pipeline (`ibconsole-pipeline`) vložte v nastavení integrace **Custom Logs** v Agent Policy do pole **Ingest Pipeline** (sekce Advanced options).

---

### 6. Testování Ingest Pipeline
Před nasazením do produkce je nutné pipeline ověřit, zda pole (`correlationId`, `processId`) extrahuje správně a citlivé údaje anonymizuje.

#### Testování v UI (Kibana)
1.  V **Stack Management** -> **Ingest Pipelines** klikněte na název pipeline.
2.  V menu zvolte **Test pipeline** -> **Add documents**.
3.  Vložte ukázkový JSON:
   ```json
   [
     {
       "_source": {
         "message": "2026-03-23 00:00:00,031 INFO 92153 [Logger] Activity 'Health' Started - traceId=e035baa8-4d74-4bf8-b5bc-0b1ca1c66cc6"
       }
     }
   ]
   ```
4.  Klikněte na **Run the test** a ověřte pole v pravé části.

#### Co kontrolovat (Checklist)
- [ ] **@timestamp**: Je čas v UTC a odpovídá času v logu?
- [ ] **log.level**: Je pole naplněno (INFO, ERROR, DEBUG)?
- [ ] **correlationId / processId**: Jsou ID správně vytažena bez okolních znaků?
- [ ] **Anonymizace**: Pokud log obsahoval e-mail, je v `message` nahrazen tagem `#EMAIL#...#EMAIL#`?
- [ ] **Tags**: Neobsahuje pole `tags` chybu `_grokparsefailure`?

---

### 7. Vytvoření Agenta (Instalace)
Agent se instaluje přímo na server, kde vznikají logy.

1.  Ve Fleet přejděte na **Agents** -> **Add agent**.
2.  Vyberte připravenou **Agent Policy** (např. `API-Gateway-DEV`).
3.  Kibana vygeneruje instalační příkaz pro PowerShell (Windows).
4.  Spusťte PowerShell jako administrátor a vložte příkaz.

**Důležité (verze 9.x):** Parametr `--namespace` se již v CLI nepoužívá. Namespace je řízen centrálně skrze **Agent Policy**, kterou agentovi přiřadíte při instalaci (pomocí tokenu).

---

### 8. Shrnutí workflow
1.  **Definice:** Rozhodněte o názvu datasetu (např. `onboarding`) a namespace (`dev`/`prod`).
2.  **Pipeline:** Vytvořte Ingest Pipeline s Grok procesorem pro parsování logů.
3.  **Policy:** Vytvořte Agent Policy se správným Default Namespace.
4.  **Integrace:** Přidejte "Custom Logs", nastavte cestu k logům a propojte vytvořenou Pipeline.
5.  **Instalace:** Nainstalujte agenta na cílový server pomocí tokenu dané politiky.
6.  **Kontrola:** V **Discover** ověřte, že data jsou v indexu `logs-onboarding-dev`.

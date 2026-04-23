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

**Příklad:** Logy z API Gateway na vývojovém prostředí budou v indexu `logs-onboarding-sample`.

---

### 3. Vytvoření Agent Policy
**Agent Policy** je centrální konfigurace, kterou agenti stahují z Fleet serveru. Určuje, co mají agenti sbírat.

1.  V Kibaně přejděte na **Management** -> **Fleet** -> **Agent Policies**.
2.  Klikněte na **Create agent policy**.
3.  **Doporučení:** Vytvořte samostatnou politiku (např. `Onboarding-App`).
4.  V **Settings** politiky nastavte **Default namespace** na `sample`. Tím zajistíte, že všechna data z této politiky automaticky dostanou správný tag a budou v indexu `logs-onboarding-sample`.

---

### 4. Integrace v Agent Policy (Custom Logs)
Do vytvořené politiky je třeba přidat konkrétní úkol – sběr souborů.

1.  V detailu politiky klikněte na **Add integration** a vyberte **Custom Logs**.
2.  **Integration name:** Např. `onboarding-logs-collection`.
3.  **Log file path:** Absolutní cesta k logům (např. `C:\App\Logs\onboarding.log`).
4.  **Dataset name:** Zadejte název datasetu `onboarding`.
5.  **Advanced options - Encoding:** Pokud logy obsahují diakritiku (např. ze systému Windows), nastavte `windows-1250`.
6.  **Custom configurations:** Zde se později propojí Ingest Pipeline.

---

### 5. Vytvoření Ingest Pipeline s Grok procesorem
**Ingest Pipeline** transformuje surový text logu na strukturovaný JSON ještě před jeho uložením do indexu. Tato pipeline zajišťuje, že se surový log rozdělí na jednotlivá pole a v poli `message` zůstane kompletní text zprávy pro lepší čitelnost.

#### Architektura zpracování (Logika)
Pipeline je navržena jako sekvence kroků (procesorů), které postupně transformují data:
1.  **Základní rozklad (Grok):** Identifikuje fixní části logu (datum, log level, ID požadavku, název loggeru).
2.  **Normalizace času (Date):** Převod textového datumu na standardní `@timestamp` v UTC.
3.  **Hloubková extrakce (Grok):** Extrakce metadat z konce zprávy (za svislítkem `|`).
4.  **Parsování (KV):** Rozklad metadat na jednotlivá pole `onboarding.*`.
5.  **Typování dat (Convert):** Zajištění, že číselné hodnoty (např. ms) jsou uloženy jako čísla.
6.  **Expanze (Dot Expander):** Převedení tečkové notace na hierarchický JSON.
7.  **Metadata:** Odstranění pomocných dočasných polí.

#### Kompletní JSON konfigurace (onboarding-pipeline)
Aktuální a kompletní JSON konfiguraci pro Ingest Pipeline naleznete v souboru:
`SERVICES/OFFICE_LINE/onboarding/elastic/onboarding_grok_pipeline.json`

Podrobný popis jednotlivých kroků parsování a návod na instalaci v Kibaně je k dispozici v dokumentu:
[4. Vytvoření Ingest Pipeline s Grok procesorem](./4.%20Vytvoření%20Ingest%20Pipeline%20s%20Grok%20procesorem.md)

**Propojení:** Název této pipeline (`onboarding-pipeline`) vložte v nastavení integrace **Custom Logs** v Agent Policy do pole **Ingest Pipeline** (sekce Advanced options).
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
2.  Vyberte připravenou **Agent Policy** (např. `Onboarding-App`).
3.  Kibana vygeneruje instalační příkaz pro PowerShell (Windows).
4.  Spusťte PowerShell jako administrátor a vložte příkaz.

**Důležité (verze 9.x):** Parametr `--namespace` se již v CLI nepoužívá. Namespace je řízen centrálně skrze **Agent Policy**, kterou agentovi přiřadíte při instalaci (pomocí tokenu).

---

### 8. Import Vizualizací a Dashboardů (Saved Objects)
**DŮLEŽITÉ:** Dashboardy a vizualizace jsou uloženy ve formátu **NDJSON** (Newline Delimited JSON). To znamená, že každý řádek souboru je samostatný validní JSON objekt. Tento formát je vyžadován Kibanou pro import/export Saved Objects.

**VAROVÁNÍ:**
- **Soubor se NESMÍ přeformátovávat (pretty-print) ani upravovat v běžných textových editorech**, které by mohly změnit kódování nebo konce řádků. Pokud nástroj rozdělí jeden řádek na více řádků, soubor se stane pro Kibanu nečitelným.
- Pokud při importu narazíte na chybu *"Unexpected non-whitespace character after JSON at position..."*, obvykle to znamená, že se soubor pokoušíte nahrát do špatné sekce (např. Ingest Pipelines) nebo že soubor obsahuje neviditelné znaky/špatné konce řádků. Použijte soubory přímo z adresáře `Elastic/exports/` bez jakýchkoliv úprav.
- Pokud vizualizace v dashboardu neukazují žádná data (No results found), ujistěte se, že používáte nejnovější verzi souboru `onboarding_kpi_dashboard.ndjson`. Předchozí verze mohly obsahovat chybně pojmenovaná pole (přípona `.keyword`), která nejsou v prostředí Elastic Serverless pro dynamická pole dostupná.
- Tyto soubory se **NEIMPORTUJÍ** v sekci Ingest Pipelines. Pokud se o to pokusíte, Elastic zobrazí chybu: *"Please ensure the JSON is a valid pipeline object"*.

Správný postup importu:
1.  V Kibaně přejděte do **Management** -> **Stack Management**.
2.  V levém menu v sekci **Kibana** klikněte na **Saved Objects**. (NEMÍCHAT s Ingest Pipelines v sekci Ingest!)
3.  Klikněte na **Import** v pravém horním rohu.
4.  Nahrajte soubor:
    - `Elastic/exports/onboarding_kpi_dashboard.ndjson` (Hlavní KPI dashboard)
    - `Elastic/exports/onboarding_dashboard.ndjson` (Technický monitoring)
5.  **Dostupné formáty:** 
    - Pro import do Kibany používejte vždy soubor `onboarding_kpi_dashboard.ndjson`.
6.  Pokud se objeví dotaz na konflikt ID, zvolte **Check for existing objects** a případně **Overwrite**.
7.  Dashboardy naleznete v sekci **Analytics** -> **Dashboard**.

---

### 9. Shrnutí workflow
1.  **Definice:** Rozhodněte o názvu datasetu (např. `onboarding`) a namespace (např. `sample` pro testovací data).
2.  **Pipeline:** Vytvořte Ingest Pipeline s Grok procesorem pro parsování logů (importujte JSON v sekci Ingest Pipelines).
3.  **Policy:** Vytvořte Agent Policy se správným Default Namespace.
4.  **Integrace:** Přidejte "Custom Logs", nastavte cestu k logům a propojte vytvořenou Pipeline.
5.  **Instalace:** Nainstalujte agenta na cílový server pomocí tokenu dané politiky.
6.  **Dashboardy:** Importujte `.ndjson` soubory v sekci **Saved Objects**.
7.  **Kontrola:** V **Discover** ověřte, že data jsou v indexu `logs-onboarding-sample`.

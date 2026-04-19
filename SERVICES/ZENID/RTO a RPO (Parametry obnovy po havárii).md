### RTO a RPO (Parametry obnovy po havárii)

Tyto dva parametry jsou základem strategie pro obnovu po havárii (Disaster Recovery) a definují, jak moc je služba odolná vůči výpadku.

#### 1. RTO (Recovery Time Objective) – Cíl doby obnovy
*   **Definice:** Maximální přípustná doba, po kterou může být systém nedostupný po vzniku incidentu (např. výpadek serveru, kybernetický útok).
*   **Klíčová otázka:** „Jak rychle musíme službu obnovit?“
*   **V kontextu ZenID (Trask):**
    *   **Návrh Trasku:** 12 hodin.
    *   **Stanovisko banky:** Tomáš Hanuš (IT) to rozporuje. U moderního cloudového (SaaS) řešení v HA (High Availability) režimu je 12 hodin příliš mnoho. Očekává se řádově kratší doba (minuty až jednotky hodin).

#### 2. RPO (Recovery Point Objective) – Cíl bodu obnovy
*   **Definice:** Maximální přípustné množství ztracených dat vyjádřené v čase. Určuje, k jakému okamžiku v minulosti se musíme být schopni vrátit (např. čas poslední zálohy).
*   **Klíčová otázka:** „O kolik dat můžeme přijít?“
*   **V kontextu ZenID (Trask):**
    *   **Návrh Trasku:** 6 hodin.
    *   **Stanovisko banky:** Je třeba provést analýzu, o jaká data by banka přišla. Pokud jde o logy/audity, které banka stahuje v reálném čase, je to akceptovatelné. Pokud by šlo o data rozpracovaných registrací, je 6 hodin rizikových.

#### 3. MTO (Maximum Tolerable Downtime)
*   **Definice:** Maximální tolerovatelná doba výpadku. Je to absolutní strop, po jehož překročení dochází k nevratným škodám na byznysu nebo reputaci.
*   **Význam:** Zatímco RTO je cílová hodnota, MTO je nepřekročitelná hranice vyžadovaná regulátorem.
*   **Stav vyjednávání:** Trask odmítá definovat, banka na tom trvá kvůli splnění požadavků DORA.

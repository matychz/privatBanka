# AXA Core Banking – Přehled systému a integrace

Tento dokument shrnuje roli a technické propojení systému **AXA Core Banking** v rámci ekosystému Privatbanky a projektu digitálního onboardingu.

## 1. Role systému AXA
**AXA** je centrální bankovní systém (Core Banking), který slouží jako "single source of truth" pro finanční data a operace.

**Hlavní odpovědnosti:**
*   **Správa účtů:** Vedení běžných a spořicích účtů klientů.
*   **Zůstatky a transakce:** Reálné zůstatky, historie pohybů a clearing.
*   **Platební styk:** Provádění tuzemských i zahraničních plateb.
*   **Blokace a rezervace:** Správa finančních blokací (např. při nákupu cenných papírů).
*   **Settlement:** Konečné vypořádání obchodů a výplata kupónů.

## 2. Integrace v rámci projektu
V projektu digitálního onboardingu a prodeje dluhopisů figuruje AXA v několika klíčových scénářích:

### A. Onboarding (Background Processing)
Během fáze `BACKGROUND_PROCESSING` dochází k provizování klienta a produktů:
1.  **Centris** (po vytvoření kontraktu) asynchronně volá **AXA Core** pro založení bankovních produktů (účtů).
2.  **AXA Core** po úspěšném založení generuje události (Events), které jsou přes **Message Queue (MQ)** doručovány do **OfficeLine**.

### B. Prodej cenných papírů (Securities Trading)
Při nákupu dluhopisu v mobilní aplikaci:
1.  **OfficeLine (EB)** dotazuje **AXA** na disponibilní zůstatek na zvoleném účtu.
2.  Před odesláním pokynu k vypořádání do Centrisu provede **AXA** rezervaci (blokaci) prostředků na účtu klienta.
3.  Po potvrzení settlementu v Centrisu dojde v **AXA** k finálnímu odepsání prostředků.

## 3. Technická rozhraní (High-level)
Integrace mezi OfficeLine (e-banking backendem) a AXA probíhá primárně přes interní API/Middleware:

| Operace | Typ | Popis |
|---|---|---|
| `VerifyBalance` | Synchronní | Ověření, zda má klient dostatek prostředků pro nákup. |
| `ReserveFunds` | Synchronní | Vytvoření blokace na účtu do doby vypořádání obchodu. |
| `CommitPayment` | Asynchronní | Finální zúčtování platby po potvrzení obchodu. |
| `AccountProvisioning` | Asynchronní | Založení nového účtu na základě požadavku z Centrisu. |

### D. Monitoring a Hypercare (Klíčové pro Go-Live)
Stav transakcí v AXA je kritický pro stabilitu po spuštění. V rámci "Hypercare" fáze se zaměřujeme na:
1.  **Konzistence blokací:** Sledování, zda každá rezervace prostředků (`ReserveFunds`) má odpovídající pokyn v Centrisu a následný settlement.
2.  **Zpracování MQ událostí:** Monitoring fronty pro zakládání účtů, aby nedocházelo k prodlevám v onboardingu.
3.  **Odsouhlasení (Reconciliation):** Denní porovnání stavu objednávek v OfficeLine/Centris proti reálným pohybům v AXA Core.

*Detailní postupy naleznete v dokumentu [AXA Monitoring & Hypercare](AXA_Monitoring_Hypercare.md).*

## 4. Technická rozhraní (High-level)

---
*Zdroj: DigitalnyOnBoarding Wiki (TR-OL-ONB-krok-BACKGROUND_PROCESSING.md, Prodej-dluhopisu-varianty.md)*

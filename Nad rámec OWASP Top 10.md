Nad rámec OWASP Top 10: Co by mělo tvořit komplexní bezpečnostní strategii?
Pokud je OWASP Top 10 považován za "povinné minimum" (baseline), pro projekt typu DigitalnyOnBoarding v bankovním prostředí je nutné strategii rozšířit o další specifické oblasti a pokročilejší standardy.
Zde jsou klíčové oblasti, které by měly být součástí komplexního testování a zabezpečení:
1. OWASP ASVS (Application Security Verification Standard)
   Zatímco Top 10 je seznam rizik, ASVS je detailní standard pro testování. Obsahuje stovky kontrolních bodů rozdělených do tří úrovní (L1–L3). Pro bankovní aplikaci se doporučuje cílit na L2 (Standardní důvěrné aplikace) nebo L3 (Aplikace s vysokou hodnotou/kritické).
   •
   Co navíc: Detailní požadavky na šifrování, ověřování identity, validaci vstupů a architekturu.
2. OWASP API Security Top 10
   Vzhledem k tomu, že projekt stojí na REST API (Mobile API, Onboarding API, LAG API), je kritické zaměřit se na specifika API, která "běžný" Top 10 pokrývá jen částečně:
   •
   BOLA (Broken Object Level Authorization): Schopnost manipulovat s ID v URL a získat data jiného procesu/klienta (klíčové pro /v1/onboarding/{processId}).
   •
   Mass Assignment: Možnost poslat v JSONu pole, která by klient neměl měnit (např. změna stavu AML kontroly v requestu).
   •
   Unrestricted Resource Consumption: Nedostatečný rate limiting, který by mohl vést k vyčerpání prostředků backendu (OfficeLine).
3. OWASP Mobile Top 10
   Jelikož je onboarding navržen jako "mobile-first", je nutné testovat i klientskou stranu (iOS/Android aplikaci):
   •
   Bezpečné ukládání dat v zařízení: Jsou tokeny a citlivá data v Keychainu/Keystoru?
   •
   Obrana proti reverznímu inženýrství: Obfuskace kódu, detekce Root/Jailbreak.
   •
   Certificate Pinning: Ochrana proti odposlechu komunikace (Man-in-the-Middle) i v případě, že útočník podvrhne certifikát.
4. Testování byznysové logiky (Business Logic Flaws)
   Toto je oblast, kterou automatizované skenery neodhalí. Jde o zneužití legitimních funkcí k nelegitimním účelům:
   •
   KYC/AML Bypass: Lze procesem projít s neplatnými nebo upravenými daty (např. podvržení liveness testu v ZenID)?
   •
   Race Conditions: Co se stane, když pošlu dva požadavky na aktivaci tokenu ve stejný okamžik?
   •
   Změna pořadí kroků: Lze přeskočit AML kontrolu a přejít přímo k podpisu smluv?
5. Compliance a Regulatorní požadavky (Banking Specific)
   V bankovnictví musíte splňovat specifické standardy:
   •
   PSD2 / SCA (Strong Customer Authentication): Ověření, zda implementace eCobra Tokenu (ECT) a OTP splňuje požadavky na dvoufaktorové ověření.
   •
   GDPR: Zajištění, že osobní údaje (včetně biometriky ze ZenID) jsou zpracovávány a ukládány v souladu s ochranou soukromí.
6. Supply Chain Security (Bezpečnost dodavatelského řetězce)
   •
   SCA (Software Composition Analysis): Pravidelné skenování závislostí (NuGet, NPM) na známé zranitelnosti (CVE).
   •
   Zabezpečení CI/CD: Ochrana build serverů a deployment pipeline, aby do produkce nebyl vložen škodlivý kód.
7. Observability a Incident Response (Zmiňovaný "Open Point")
   Jak je uvedeno ve vaší dokumentaci, observabilita na DEV/TEST je klíčová:
   •
   Detekce útoků v reálném čase: Pokud někdo zkouší brute-force na OTP, musí to systém okamžitě nahlásit.
   •
   Forenzní připravenost: Logy musí být dostatečné pro to, aby šlo po incidentu zjistit, co přesně se stalo, ale nesmí obsahovat citlivá data (např. hesla nebo biometriku).
   Shrnutí pro váš projekt:
   Pro DigitalnyOnBoarding bych doporučil prioritně přidat OWASP API Security Top 10 a testování byznysové logiky onboardingu, protože to jsou oblasti s nejvyšším rizikem dopadu na banku. Pokud máte mobilní aplikaci, OWASP Mobile Top 10 je rovněž nezbytností.
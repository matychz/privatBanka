OWASP Top 10: Testovací metodika a standard bezpečnosti
OWASP Top 10 (Open Web Application Security Project) je celosvětově uznávaný standard a osvětový dokument, který definuje 10 nejkritičtějších bezpečnostních rizik pro webové aplikace. V kontextu projektu DigitalnyOnBoarding slouží jako základní rámec pro provádění penetračních testů, aby bylo zajištěno, že aplikace (Mobile API, OfficeLine, atd.) jsou odolné proti nejčastějším útokům.
Zde je přehled aktuálních kategorií dle nejnovější verze (OWASP Top 10:2021):
1. A01:2021-Broken Access Control (Narušení řízení přístupu)
   Uživatelé mohou přistupovat k datům nebo funkcím, ke kterým nemají mít oprávnění. Například se běžný uživatel dostane k administrativnímu rozhraní nebo k údajům jiného klienta.
2. A02:2021-Cryptographic Failures (Kryptografická selhání)
   Dříve známé jako "Sensitive Data Exposure". Týká se nedostatečné ochrany citlivých dat (hesla, čísla účtů, osobní údaje) při přenosu nebo ukládání (např. slabé šifrování, chybějící HTTPS).
3. A03:2021-Injection (Injekce)
   Útočník vkládá škodlivý kód do dotazů, které aplikace zpracovává. Patří sem známý SQL Injection, ale i NoSQL nebo LDAP injection. Správné ošetření vstupů je klíčovou obranou.
4. A04:2021-Insecure Design (Nezabezpečený návrh)
   Zaměřuje se na chyby v architektuře a designu aplikace. I dokonale napsaný kód může být nebezpečný, pokud je samotný proces (např. obnova hesla) navržen chybně.
5. A05:2021-Security Misconfiguration (Chybná konfigurace zabezpečení)
   Aplikace nebo server jsou špatně nastaveny – například jsou ponechána výchozí hesla, zapnuté zbytečné funkce nebo odhaleny detailní chybové hlášky, které pomáhají útočníkovi.
6. A06:2021-Vulnerable and Outdated Components (Zranitelné a zastaralé komponenty)
   Používání knihoven, frameworků nebo jiných komponent, které mají známé bezpečnostní díry. (Např. stará verze .NET runtime nebo ReactJS).
7. A07:2021-Identification and Authentication Failures (Chyby identifikace a autentizace)
   Problémy s potvrzením identity uživatele – například slabá politika hesel, možnost útoku hrubou silou (brute force) nebo špatná správa session (tokenů).
8. A08:2021-Software and Data Integrity Failures (Chyby integrity softwaru a dat)
   Nedostatečné ověření integrity kódu nebo dat. Například pokud aplikace přijímá serializovaná data od uživatele bez kontroly, zda s nimi nebylo manipulováno.
9. A09:2021-Security Logging and Monitoring Failures (Chyby logování a monitorování)
   Nedostatečné záznamy o kritických událostech. Pokud se útočník pokouší o průnik, ale systém to nezaloguje nebo na to neupozorní, útočník má více času na úspěšný útok. Pozn.: Toto je v dokumentaci DigitalnyOnBoarding zmíněno jako "OPEN POINT" pro DEV prostředí.
10. A10:2021-Server-Side Request Forgery (SSRF)
    Útočník donutí server, aby odeslal HTTP požadavek na místo, kam by se útočník sám nedostal (např. do vnitřní sítě banky za firewall).
    Proč je to důležité pro DigitalnyOnBoarding?
    Při penetračních testech vašeho projektu se testeři zaměřují právě na tyto oblasti. Vzhledem k tomu, že pracujete s citlivými daty (KYC, ZenID) a finančními transakcemi, je shoda s OWASP Top 10 naprostým minimem pro zajištění bezpečnosti klientů PrivatBanky.
    V souboru Pentesty_Summary.md je tato metodika uvedena jako povolená aktivita, což znamená, že testeři mají za úkol tyto zranitelnosti aktivně hledat a simulovat na ně útoky.
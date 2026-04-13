# Technické řešení Redirectu a Deferred DeepLinků
Tento dokument detailně popisuje technický mechanizmus přesměrování do obchodů (App Store / Google Play) a následného předání dat do mobilní aplikace po její instalaci.

## 1. Principy DeepLinků
Pro optimální uživatelskou zkušenost se využívají dva doplňující se mechanizmy:
1.  **Nativní DeepLink (Universal Link / App Link)**: Pokud je aplikace již nainstalována, OS (iOS/Android) automaticky zachytí URL a otevře aplikaci přímo.
2.  **Deferred DeepLink (Odložený DeepLink)**: Pokud aplikace není nainstalována, dojde k přesměrování do prohlížeče, který následně uživatele pošle do příslušného storu (App Store/Google Play). Po instalaci a prvním spuštění musí aplikace získat data, která byla v původním odkazu.

## 2. Technický flow při naskenování QR kódu
### Krok 1: Skenování (Systémový foťák)
QR kód obsahuje URL, např. `https://download.privatbanka.sk/app?type=branch&token=JWT_TOKEN_DATA`.

### Krok 2: Rozcestník (Redirector)
Pokud se otevře prohlížeč, stránka na `download.privatbanka.sk` provede:
1.  **Detekci OS**: Pomocí `User-Agent` zjistí, zda jde o iOS nebo Android.
2.  **Otisk (Fingerprint)**: Pro iOS uloží na server (např. OfficeLine BE) dočasný záznam: `[IP adresa, Model zařízení, OS verze] -> [token data]`.
3.  **Přesměrování**:
    *   **Android**: Přesměruje na Play Store URL s parametrem `referrer`:
        `https://play.google.com/store/apps/details?id=sk.privatbanka.app&referrer=token%3DJWT_TOKEN_DATA`
    *   **iOS**: Přesměruje na App Store URL:
        `https://apps.apple.com/app/idXXXXXXXXX`

### Krok 3: První spuštění aplikace po instalaci
Aplikace potřebuje získat `token`, aby mohl proces onboardingu automaticky pokračovat.

#### A. Mechanizmus pro Android (Install Referrer)
Mobilní aplikace využije **Google Play Install Referrer API**. Po spuštění se dotáže knihovny, která vrátí hodnotu parametru `referrer` (v tomto případě `token=JWT_TOKEN_DATA`), se kterým byl Play Store otevřen.

#### B. Mechanizmus pro iOS (Matching / Fingerprinting)
Protože Apple nenabízí přímý "Install Referrer", využívá se tzv. **Device Matching**:
1.  Při prvním startu aplikace odešle na OfficeLine BE svůj otisk: `[IP adresa, Model zařízení, OS verze]`.
2.  BE porovná tento otisk se záznamy uloženými v Kroku 2 (Redirector).
3.  Pokud najde shodu (např. IP adresa a model souhlasí v časovém okně 1h), vrátí aplikaci příslušná data (`token`).

## 3. Bezpečnostní aspekty
*   **Krátká platnost otisku**: Záznamy pro matching na BE by měly mít expiraci v řádu desítek minut (uživatel obvykle stahuje a instaluje aplikaci ihned).
*   **Jednorázové použití**: Po úspěšném spárování (Claim) je otisk na BE smazán.
*   **JWT Token**: Data v QR kódu by měla být podepsaná (JWT), aby nebylo možné je podvrhnout uživatelem nebo třetí stranou.

## 4. Alternativy (Third-party)
V případě požadavku na vyšší přesnost a robustnost lze použít hotová řešení:
*   **Firebase Dynamic Links** (Upozornění: Google oznámil jejich ukončení k 8/2025).
*   **Branch.io** nebo **AppsFlyer**: Průmyslové standardy pro DeepLinking, které řeší matching s vysokou přesností.

---
**Souvislost s QR onboardingem**: Tento mechanizmus zajistí, že i klient bez nainstalované aplikace může plynule pokračovat v procesu, který začal na pobočce naskenováním QR kódu u bankéře.

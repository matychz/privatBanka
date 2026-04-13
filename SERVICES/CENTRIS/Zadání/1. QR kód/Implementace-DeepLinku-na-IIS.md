# Implementace DeepLinků na Microsoft IIS (Universal Links / App Links)

Tento dokument popisuje technickou konfiguraci serveru Microsoft IIS (Internet Information Services) pro podporu nativních odkazů do aplikace (DeepLinků) a odloženého přesměrování (Deferred DeepLinking).

## 1. Prerekvizity
*   **HTTPS**: Povinné (Apple i Google vyžadují validní SSL certifikát).
*   **URL Rewrite Module**: Doporučen pro pokročilé přesměrování (není striktně nutný pro asociační soubory, ale nezbytný pro redirector).

## 2. Podpora Universal Links (iOS) a App Links (Android)
Aby operační systém věděl, že má otevřít vaši aplikaci pro danou doménu, musí server servírovat "asociační" soubory v adresáři `.well-known`.

### Soubory k hostování:
1.  **iOS**: `/.well-known/apple-app-site-association` (soubor **BEZ** přípony).
2.  **Android**: `/.well-known/assetlinks.json` (soubor s příponou `.json`).

### Konfigurace v IIS (`web.config`):
IIS standardně blokuje soubory bez přípony a skryté složky (začínající tečkou). Je nutné toto povolit v `web.config`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <system.webServer>
        <staticContent>
            <!-- Povolení MIME typu pro soubor bez přípony (iOS) -->
            <mimeMap fileExtension="." mimeType="application/json" />
            <!-- Povolení MIME typu pro .json (Android) -->
            <remove fileExtension=".json" />
            <mimeMap fileExtension=".json" mimeType="application/json" />
        </staticContent>
        
        <security>
            <requestFiltering>
                <!-- Povolení přístupu k adresáři .well-known (skrytý adresář) -->
                <fileExtensions allowUnlisted="true">
                    <remove fileExtension="." />
                    <add fileExtension="." allowed="true" />
                </fileExtensions>
            </requestFiltering>
        </security>
    </system.webServer>
</configuration>
```

## 3. Redirector (Přesměrování do Storu)
Pokud aplikace není nainstalována (Universal/App Link nezafunguje), uživatel skončí v prohlížeči na URL `https://download.privatbanka.sk/app?token=...`. 
Tato stránka musí provést detekci OS a přesměrování.

### Možnost A: Jednoduchý Redirect přes URL Rewrite (Statický)
Pokud nepotřebujete složitou logiku (fingerprinting), lze využít `URL Rewrite`:

```xml
<rewrite>
    <rules>
        <rule name="Redirect to Android Store" stopProcessing="true">
            <match url="^app$" />
            <conditions>
                <add input="{HTTP_USER_AGENT}" pattern="Android" />
            </conditions>
            <action type="Redirect" url="https://play.google.com/store/apps/details?id=sk.privatbanka.app&amp;referrer={QUERY_STRING}" />
        </rule>
        <rule name="Redirect to iOS Store" stopProcessing="true">
            <match url="^app$" />
            <conditions>
                <add input="{HTTP_USER_AGENT}" pattern="iPhone|iPad" />
            </conditions>
            <action type="Redirect" url="https://apps.apple.com/app/idXXXXXXXXX" />
        </rule>
    </rules>
</rewrite>
```

### Možnost B: JavaScript Redirector (Doporučeno pro iOS matching)
Pro iOS (kde nefunguje Install Referrer) je potřeba v prohlížeči spustit skript, který pošle otisk zařízení na OfficeLine BE.

**Příklad `index.html` na serveru `download.privatbanka.sk`:**
```html
<script>
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    const userAgent = navigator.userAgent || navigator.vendor || window.opera;

    if (/android/i.test(userAgent)) {
        // Android: Play Store s referrerem
        window.location.replace("https://play.google.com/store/apps/details?id=sk.privatbanka.app&referrer=token%3D" + encodeURIComponent(token));
    } else if (/iPad|iPhone|iPod/.test(userAgent) && !window.MSStream) {
        // iOS: Volání BE pro uložení otisku a pak App Store
        fetch('https://api.privatbanka.sk/v1/onboarding/fingerprint', {
            method: 'POST',
            body: JSON.stringify({ token: token, ua: userAgent })
        }).finally(() => {
            window.location.replace("https://apps.apple.com/app/idXXXXXXXXX");
        });
    } else {
        // Desktop: Zobrazení informací nebo QR kódu
        window.location.replace("https://www.privatbanka.sk");
    }
</script>
```

## 4. Časté chyby v IIS
1.  **Chybějící HTTPS**: IIS musí mít správně nabindovaný port 443 s certifikátem.
2.  **Request Filtering**: IIS může blokovat tečku v URL (např. `/app.json`). Zkontrolujte `allowDoubleEscaping` v sekci `requestFiltering`.
3.  **Caching**: Asociační soubory by neměly být cachovány příliš dlouho, aby bylo možné měnit nastavení DeepLinků bez prodlevy.

---
**Související dokumentace**:
*   [Technické řešení Redirectu a DeepLinků](Technické-řešení-Redirect-a-DeepLinky.md)
*   [QR kód - dokončení onboardingu](1.%20QR%20kód%20-%20dokončení%20onboardingu.md)

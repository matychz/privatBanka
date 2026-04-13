# Příklady volání jednotlivých aplikací

Tento dokument slouží jako hlavní rozcestník k detailním příkladům volání pro klíčové aplikace systému PrivatBanky.

## 1. TradingService (SOAP)
Webová služba pro investiční bankovnictví (správa cenných papírů, pokyny, MiFID testy, smlouvy).
- **Protokol:** SOAP 1.2
- **Zabezpečení:** WS-Security, WS-Addressing
- [**Detailní příklady pro všech ~70 operací (TradingService_Examples.md)**](../../CENTRIS/TradingService/TradingService_Examples.md)

## 2. LegacyAuthGateway (REST)
Brána pro autentizaci a propojení nového Internet Bankingu se starým systémem.
- **Protokol:** REST (JSON)
- **Hlavní funkce:** Výměna kódu za token, redirect URL do starého IB.
- [**Detailní příklady volání (LegacyAuthGateway_Examples.md)**](../../../LegacyAuthGateway%20API/LegacyAuthGateway_Examples.md)

## 3. Mobile API (REST)
API pro mobilní aplikaci (Digipass, platby, karty, přehledy produktů).
- **Protokol:** REST (JSON)
- **Hlavní funkce:** Aktivace zařízení, platební operace, správa karet.
- [**Detailní příklady a přehled endpointů (MobileAPI_Examples.md)**](MobileAPI_Examples.md)

---

## Obecné technické požadavky
- **HTTPS:** Veškerá komunikace musí probíhat přes šifrovaný kanál.
- **Autentizace:**
    - U SOAP služeb (TradingService) se používá `UsernameToken`.
    - U REST služeb se používá `Authorization: Bearer <token>`.
- **Kódování:** Všechny textové přenosy musí být v kódování **UTF-8**.

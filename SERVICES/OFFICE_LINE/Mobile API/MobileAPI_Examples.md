# Příklady volání Mobile API (REST)

Tento dokument obsahuje přehled a příklady volání pro mobilní API PrivatBanky. API používá standardní REST principy a formát JSON.

## 1. Autentizace a základní hlavičky

Většina požadavků vyžaduje Bearer token v hlavičce `Authorization`.

```http
GET /api/v2/products/overview HTTP/1.1
Host: ma-dev.privatbanka.sk
Authorization: Bearer <access_token>
Accept: application/json
```

---

## 2. Aktivace a Digipass

### Inicializace aktivace (POST /digipass/activation)
```json
{
  "activationId": "MY-REALM-USER-123"
}
```

### Registrace asymetrického tokenu (POST /asymtokenactivation)
Slouží k aktivaci biometrického nebo PIN ověřování.
```json
{
  "publicKey": "BASE64_KEY...",
  "deviceId": "device-uuid-123",
  "deviceName": "iPhone 15"
}
```

---

## 3. Klient a Účet (Client & User)

### Informace o klientovi (GET /client/info)
Vrací základní údaje o přihlášeném uživateli.

### Preference uživatele (GET /user/preferences)
Nastavení jazyka, notifikací apod.

---

## 4. Produkty (Products)

### Přehled produktů (GET /product)
Vrací seznam všech běžných, termínovaných a majetkových účtů.

### Detail termínovaného vkladu (GET /timeDeposit/{id})

---

## 5. Platby (Payments)

### Tuzemská platba (POST /payment)
```json
{
  "sourceAccount": "7000123456/8020",
  "destinationAccount": "11223344/0200",
  "amount": 150.00,
  "currency": "EUR",
  "constantSymbol": "0308",
  "variableSymbol": "2024001",
  "note": "Úhrada faktury"
}
```

### Vyhledávání v transakcích (POST /transaction/search)
```json
{
  "accountNumber": "7000123456/8020",
  "dateFrom": "2024-01-01",
  "dateTo": "2024-03-31"
}
```

### SEPA Inkaso (POST /sepaDirectDebit/request)
Vytvoření nového mandátu nebo žádosti o inkaso.

---

## 6. Trvalé příkazy (Standing Orders)

### Vytvoření trvalého příkazu (POST /standingOrder/request)
```json
{
  "sourceAccount": "7000123456/8020",
  "destinationAccount": "99887766/0900",
  "amount": 50.00,
  "periodicity": "Monthly",
  "dayInMonth": 15
}
```

---

## 7. Platební karty (Cards)

### Žádost o novou kartu (POST /paymentCardRequest/newDebit)
### Změna limitů karty (POST /paymentCardRequest/cardLimitsChange)
```json
{
  "cardId": "card-9988",
  "dailyLimit": 1000.00,
  "internetLimit": 500.00
}
```
### Blokace/Odblokování karty (POST /paymentCardRequest/block)

---

## 8. Zprávy a Notifikace (Messages)

### Seznam zpráv (GET /message/paged?page=0&size=20)
### Počet nepřečtených zpráv (GET /message/count)

---

## 9. Ostatní a Číselníky

- **Pobočky a bankomaty:** `GET /poi/branch`, `GET /poi/atm`
- **Kurzovní lístek:** `GET /exchangeRate`
- **Číselníky měn a symbolů:** `GET /enumeration/currency`, `GET /enumeration/constantSymbol`
- **MiFID data:** `GET /mifid`

---

## Kompletní seznam dostupných endpointů (Cesty)

| Modul | Endpointy |
| :--- | :--- |
| **Aktivace** | `/digipass/activation`, `/asymtokenactivation`, `/asymtoken/dictionary` |
| **Klient** | `/client`, `/client/info`, `/user`, `/user/preferences`, `/partner` |
| **Platby** | `/payment`, `/payment/bankInfo`, `/transaction/search`, `/exchangeRate` |
| **Příkazy** | `/standingOrder`, `/sepaDirectDebit`, `/sddTemplate`, `/template` |
| **Karty** | `/paymentCardRequest/*`, `/request/cardLimitsChange` |
| **Zprávy** | `/message`, `/pushNotification` |
| **Produkty** | `/product`, `/timeDeposit`, `/portfolio/securities/*` |
| **Ostatní** | `/enumeration/*`, `/poi/*`, `/mifid`, `/report` |

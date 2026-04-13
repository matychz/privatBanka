# Příklady volání LegacyAuthGateway (REST)

Tato brána zajišťuje autentizaci a přechod mezi novým a starým Internet Bankingem.

## 1. Získání přístupového tokenu (POST /v1/token)

Slouží k výměně jednorázového kódu ze starého IB za přístupový token (UUID) pro nové IB.

### Request (Výměna kódu):
```http
POST /api/v1/token HTTP/1.1
Host: ibank.privatbanka.sk
Content-Type: application/json

{
  "code": "a1b2c3d4-e5f6-7890-abcd-1234567890ef"
}
```

### Response (200 OK):
```json
{
  "token": "76e3427f-5563-4d43-9824-345098234abc"
}
```

### Response (401 Unauthorized - login vyžadován):
V hlavičce `WWW-Authenticate` je vrácena URL adresa přihlašovacího formuláře starého IB.
```http
HTTP/1.1 401 Unauthorized
WWW-Authenticate: https://ibank.privatbanka.sk/ExtranetRedirect/Pages/Login.aspx
```

---

## 2. Zrušení přístupového tokenu (DELETE /v1/token)

Zneplatní aktuálně používaný přístupový token.

### Request:
```http
DELETE /api/v1/token HTTP/1.1
Host: ibank.privatbanka.sk
Authorization: Bearer 76e3427f-5563-4d43-9824-345098234abc
```

### Response (204 No Content):
(Prázdné tělo)

---

## 3. Získání URL pro redirect (POST /v1/url)

Generuje URL adresu a jednorázový kód pro přesměrování uživatele na konkrétní funkci ve starém IB, která ještě není v novém IB dostupná.

### Request:
```http
POST /api/v1/url HTTP/1.1
Host: ibank.privatbanka.sk
Authorization: Bearer 76e3427f-5563-4d43-9824-345098234abc
Content-Type: application/json

{
  "pageIdentifier": "StandingOrders",
  "clientId": "123456789"
}
```

### Response (200 OK):
```json
{
  "url": "https://ibank.privatbanka.sk/Extranet/Pages/StandingOrders.aspx",
  "code": "one-time-bridge-code-999"
}
```

---

## Možné chybové stavy
Brána vrací chyby v jednotném formátu:

```json
{
  "code": "VALIDATION_ERROR",
  "message": "The field clientId is required.",
  "field": "clientId",
  "details": null
}
```

# Kompletní příklady volání TradingService (SOAP)

Tento dokument obsahuje příklady pro **všechny** operace webové služby `TradingService`.

## 1. Společná šablona (Envelope)

Všechny požadavky musí používat SOAP 1.2 a obsahovat WS-Addressing a WS-Security hlavičky.

```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" 
               xmlns:tem="http://tempuri.org/" 
               xmlns:mod="http://schemas.datacontract.org/2004/07/Models"
               xmlns:wsa="http://www.w3.org/2005/08/addressing">
   <soap:Header>
      <wsa:Action>http://tempuri.org/ITradingService/[NÁZEV_OPERACE]</wsa:Action>
      <wsa:To>https://localhost/OnlineTrading/TradingService.svc</wsa:To>
      <wsa:MessageID>urn:uuid:[UUID]</wsa:MessageID>
      <!-- Zde WS-Security (viz dokumentace) -->
   </soap:Header>
   <soap:Body>
      <!-- Tělo operace -->
   </soap:Body>
</soap:Envelope>
```

---

## 2. Správa investičních nástrojů (Instruments)

### GetInstruments
```xml
<tem:GetInstruments>
   <tem:language>Czech</tem:language>
   <tem:filter>
      <mod:FulltextSearch>Privatbanka</mod:FulltextSearch>
   </tem:filter>
</tem:GetInstruments>
```

### GetInstrumentsForClient
```xml
<tem:GetInstrumentsForClient>
   <tem:clientAbo>123456789</tem:clientAbo>
   <tem:language>Czech</tem:language>
</tem:GetInstrumentsForClient>
```

### GetInstrument
```xml
<tem:GetInstrument>
   <tem:instrumentId>123</tem:instrumentId>
   <tem:language>Czech</tem:language>
</tem:GetInstrument>
```

### CreateInstrument / UpdateInstrument
```xml
<tem:CreateInstrument>
   <tem:instrument>
      <mod:Isin>SK1110001234</mod:Isin>
      <mod:Name>Nový dluhopis</mod:Name>
   </tem:instrument>
</tem:CreateInstrument>
```

### DeleteInstrument
```xml
<tem:DeleteInstrument>
   <tem:instrumentId>123</tem:instrumentId>
</tem:DeleteInstrument>
```

---

## 3. Správa klientů (Clients)

### GetClient / GetClientAddress / GetClientContacts
```xml
<tem:GetClient>
   <tem:abo>123456789</tem:abo>
   <tem:language>Czech</tem:language>
</tem:GetClient>
```

### GetClientRepresentativePersons
```xml
<tem:GetClientRepresentativePersons>
   <tem:abo>123456789</tem:abo>
</tem:GetClientRepresentativePersons>
```

### SetDisponentContactDetails / SetDisponentAccountDetails / SetDisponentPaymentDetails
```xml
<tem:SetDisponentContactDetails>
   <tem:clientAbo>123456789</tem:clientAbo>
   <tem:details> <!-- Typ mod:DisponentContactDetails -->
      <mod:Email>jan.novak@email.cz</mod:Email>
   </tem:details>
</tem:SetDisponentContactDetails>
```

### SetTaxDomicileDeclaration / SetAMLDeclaration
```xml
<tem:SetTaxDomicileDeclaration>
   <tem:clientAbo>123456789</tem:clientAbo>
   <tem:declaration> <!-- Typ mod:TaxDomicileDeclaration -->
      <mod:CountryCode>CZ</mod:CountryCode>
   </tem:declaration>
</tem:SetTaxDomicileDeclaration>
```

---

## 4. Obchodní pokyny a šablony (Orders & Templates)

### CreateOrder
```xml
<tem:CreateOrder>
   <tem:order>
      <mod:Action><mod:Id>1</mod:Id></mod:Action>
      <mod:Client><mod:Id>123456789</mod:Id></mod:Client>
      <mod:Instrument><mod:Id>123</mod:Id></mod:Instrument>
      <mod:Quantity>10</mod:Quantity>
   </tem:order>
</tem:CreateOrder>
```

### ConfirmOrder
```xml
<tem:ConfirmOrder>
   <tem:orderId>998877</tem:orderId>
   <tem:verificationCode>123456</tem:verificationCode>
</tem:ConfirmOrder>
```

### GetFee
```xml
<tem:GetFee>
   <tem:clientAbo>123456789</tem:clientAbo>
   <tem:instrumentId>123</tem:instrumentId>
   <tem:amount>1000</tem:amount>
</tem:GetFee>
```

### GetIbisOrders / SetSynchronizedOrder / SetSynchronizedError
```xml
<tem:GetIbisOrders />
```
```xml
<tem:SetSynchronizedOrder>
   <tem:orderId>998877</tem:orderId>
</tem:SetSynchronizedOrder>
```

### Správa šablon (Create/Update/Delete OrderTemplate/Set)
```xml
<tem:CreateOrderTemplate>
   <tem:template>
      <mod:Name>Moje šablona</mod:Name>
      <mod:InstrumentId>123</mod:InstrumentId>
   </tem:template>
</tem:CreateOrderTemplate>
```

---

## 5. MiFID Testy a Zkoušky (Exams)

### GenerateClientExam (všechny varianty)
`GenerateClientExam`, `GenerateClientExamForInvestmentContract`, `GenerateClientExamForInvestmentContractAsset`
```xml
<tem:GenerateClientExam>
   <tem:clientAbo>123456789</tem:clientAbo>
   <tem:examDefinitionId>1</tem:examDefinitionId>
   <tem:language>Czech</tem:language>
</tem:GenerateClientExam>
```

### PerformClientExam
```xml
<tem:PerformClientExam>
   <tem:clientExam> <!-- Typ mod:ClientExam -->
      <mod:Id>456</mod:Id>
      <mod:Answers> <!-- Pole odpovědí --> </mod:Answers>
   </tem:clientExam>
</tem:PerformClientExam>
```

### GetExamDefinitionsForClient / GetClientExamsView
```xml
<tem:GetExamDefinitionsForClient>
   <tem:clientAbo>123456789</tem:clientAbo>
   <tem:language>Czech</tem:language>
</tem:GetExamDefinitionsForClient>
```

### GetActiveClientExam...
`GetActiveClientExamForInvestmentContract`, `GetActiveClientExamForInvestmentContractAsset`, `GetActiveClientExamForInvestmentStrategyChange`
```xml
<tem:GetActiveClientExamForInvestmentContract>
   <tem:clientAbo>123456789</tem:clientAbo>
</tem:GetActiveClientExamForInvestmentContract>
```

---

## 6. Smlouvy a Strategie (Contracts & Strategies)

### CreateContract / CreateInvestmentContract
```xml
<tem:CreateInvestmentContract>
   <tem:contract>
      <mod:ClientAbo>123456789</mod:ClientAbo>
      <mod:StrategyId>1</mod:StrategyId>
   </tem:contract>
</tem:CreateInvestmentContract>
```

### CreateAccountContract / CreateTVContract / CreateEdcContract
```xml
<tem:CreateTVContract>
   <tem:clientAbo>123456789</tem:clientAbo>
   <tem:amount>50000</tem:amount>
</tem:CreateTVContract>
```

### GetActiveInvestmentContract / GetClientInvestmentStrategies
```xml
<tem:GetActiveInvestmentContract>
   <tem:clientAbo>123456789</tem:clientAbo>
</tem:GetActiveInvestmentContract>
```

### Investiční strategie
`CreateInvestmentStrategy`, `UpdateInvestmentStrategy`, `CreateInvestmentStrategyAsset`, `GetAllowedStrategyTypeList`, `GetAllowedStrategyTypeListAsset`
```xml
<tem:GetAllowedStrategyTypeList>
   <tem:language>Czech</tem:language>
</tem:GetAllowedStrategyTypeList>
```

---

## 7. Synchronizace a Opakování (Sync & Retries)

### SyncClientToIbis
```xml
<tem:SyncClientToIbis>
   <tem:clientAbo>123456789</tem:clientAbo>
</tem:SyncClientToIbis>
```

### GetErrors
```xml
<tem:GetErrors />
```

### SyncFailed... (Všechny varianty)
Operace slouží k ručnímu spuštění synchronizace entit, které dříve selhaly. Většinou nevyžadují parametry.
- `SyncFailedContracts`, `SyncFailedInvestmentContracts`, `SyncFailedInvestmentStrategies`, `SyncFailedContactDetails`, `SyncFailedPaymentDetails`, `SyncFailedAccountDetails`, `SyncFailedAmlDeclarations`, `SyncFailedTaxDomicileDeclarations`, `SyncFailedAccountContracts`, `SyncFailedTVContracts`, `SyncFailedStatementsGfi`, `SyncFailedStatementsKuv`, `SyncFailedEdcContracts`, `SyncFailedDocumentsToSign`.

Příklad volání:
```xml
<tem:SyncFailedContracts />
```

---

## 8. Dokumenty a Verifikace

### SaveStatementGFI / SaveStatementKUV
```xml
<tem:SaveStatementGFI>
   <tem:clientAbo>123456789</tem:clientAbo>
   <tem:data>[BASE64_DATA]</tem:data>
</tem:SaveStatementGFI>
```

### SetDocumentState
```xml
<tem:SetDocumentState>
   <tem:documentId>789</tem:documentId>
   <tem:state>Signed</tem:state>
</tem:SetDocumentState>
```

### IsValidVerificationCode
```xml
<tem:IsValidVerificationCode>
   <tem:clientAbo>123456789</tem:clientAbo>
   <tem:code>123456</tem:code>
</tem:IsValidVerificationCode>
```

### GenerateBankIdentityVerificationCode
```xml
<tem:GenerateBankIdentityVerificationCode>
   <tem:clientAbo>123456789</tem:clientAbo>
</tem:GenerateBankIdentityVerificationCode>
```

### UpdatePortfolioCustomName
```xml
<tem:UpdatePortfolioCustomName>
   <tem:clientAbo>123456789</tem:clientAbo>
   <tem:portfolioId>1</tem:portfolioId>
   <tem:customName>Moje úspory</tem:customName>
</tem:UpdatePortfolioCustomName>
```

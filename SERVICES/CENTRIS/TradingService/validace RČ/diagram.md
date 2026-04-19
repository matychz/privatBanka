::: mermaid

sequenceDiagram
autonumber
participant App as Volající aplikace
participant Val as Validation Logic
participant Identity as Identifikační číslo (RC)
participant BD as BirthDate Object

    App->>Val: Validate(birthDate, sex)
    
    Note over Val: Základní kontroly (Null/Empty)
    
    alt Type je Unknown nebo Null
        Val-->>App: MissingType
    else Identity je prázdná
        Val-->>App: InvalidIdentity
    else Country je neplatná
        Val-->>App: MissingCountry
    end

    Note over Val: Validace Slovenského/Českého RC

    alt Délka != 9 a != 10
        Val-->>App: InvalidIdentity
    else Délka OK
        Val->>Identity: Parsování (Year, Month, Day, Number)
        
        Note over Val: Logika Identity (Region)
        
        alt Neplatné datum (den > 31, měsíc mimo intervaly)
            Val-->>App: InvalidIdentity
        else Staré RC (rok < 54 & číslo < 1000)
            Val->>Val: Nastav Valid (bez modula)
        else Moderní RC (rok >= 54 nebo nové milénium)
            Val->>Val: Výpočet Modulo 11
            alt identityNumber % 11 == 0
                Val->>Val: Nastav Valid
            else
                Val-->>App: InvalidIdentity
            end
        end

        Note over Val: Křížová kontrola (Region BirthDate)

        alt Pokud je result == Valid AND birthDate != null
            Val->>Val: Normalizace měsíce (month - 50 pokud žena)
            Val->>BD: Porovnání (Year.Last2, Month, Day)
            alt Shoda s objektem birthDate
                Val-->>App: Valid
            else Neshoda s datem narození
                Val-->>App: Invalid (Neshoda údajů)
            end
        else Result je už Invalid
            Val-->>App: InvalidIdentity
        end
    end

:::
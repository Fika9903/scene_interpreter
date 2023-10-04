# Scene Interpreter

## Installation
För att installera alla nödvändiga moduler, kör:
pip install -r requirements.txt

## Plan

### Steg 1: Skapa en miljö i Unreal Engine
Först, skapa en miljö inuti Unreal Engine vi kan extrahera objekt och deras positioner.

### Steg 2: Identifiera objekt
Identifiera alla objekt i den skapade miljön och notera deras positioner.

### Steg 3: Extrahera och Konvertera Information
- Extrahera information om objekten med hjälp av C++.
- Konvertera den extraherade informationen till en JSON beskrivning av allt i scenen. JSON beskrivningen ska innehålla:
  - Tidpunkt för scenen
  - En beskrivning av miljön
  - En lista över alla objekt tillsammans med en beskrivning av varje objekt
  - Koordinater för alla objekt, kombinerat med en mänsklig beskrivning av positionen (t.ex. "i hörnet" istället för xyz-koordinater).

### Steg 4: Använd scenen som input
- Använd den genererade JSON beskrivningen av scenen som input till vår existerande kod.
- Den senaste JSON scenen ska skickas till en LLM tillsammans med den eller de föregående scenerna.
- Programmet kan ha en interrupt loop som väntar på en användarfråga. När en fråga tas emot ska den läsa av alla scener och skicka dem till en AI för tolkning.


# scene_interpreter
#
# "pip install -r requirements.txt" för att installera alla moduler

1.	Skapa en miljö i unreal engine
2.	Identifiera alla objekt i miljön med dess position
3.	Extrahera informationen med c++ och konvertera till en JSON beskrivning av allt i scenen.
JSON beskrivningen av scenen ska bestå av:
-Tid för scenen
-En beskrivning av övriga miljön
-Alla objekt samt en beskrivning av dem
-Koordinater för samtliga objekt kombinerat med en mänsklig beskrivning av     positionen (exempelvis i hörnet i stället för xyz).
4.   Använd scenen som input till vår existerande kod. Den senaste JSON scenen ska skickas till en LLM tillsammans med den förra (eller flera) scenen. Vi kan ha en interrupt loop som väntar på en användarfråga och när den får det läser den av alla scener och skickar till en ai för att tolka scenerna.


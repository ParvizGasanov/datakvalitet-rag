# Rapport – Datakvalitet och RAG-system med Netflix-data

## 1. Inledning

I detta projekt har vi arbetat med datakvalitet och en enkel RAG-applikation. RAG står för Retrieval Augmented Generation och betyder att en AI-modell först hämtar relevant information från en datakälla och sedan använder den informationen för att skapa ett svar.

Vi valde att använda ett Netflix-dataset från Kaggle. Datasetet innehåller information om filmer och TV-serier, till exempel titel, typ, land, kategori, utgivningsår och beskrivning.

Projektet är gjort av Parviz och Meridona.

## 2. Syfte

Syftet med projektet var att undersöka hur datakvalitet påverkar ett AI-system. Innan datan kan användas i en RAG-applikation behöver den kontrolleras och rensas. Om datan innehåller tomma värden, dubbletter eller otydlig text kan AI-systemet ge sämre eller mer osäkra svar.

Målet var därför att:

- läsa in och undersöka ett dataset
- identifiera datakvalitetsproblem
- rensa och förbereda datan
- skapa en textkolumn som kan användas i RAG
- bygga en enkel RAG-applikation
- testa om applikationen kan svara baserat på datasetet

## 3. Dataset

Datasetet innehåller Netflix-titlar och flera kolumner med information om varje titel. Exempel på kolumner är `title`, `type`, `director`, `cast`, `country`, `release_year`, `rating`, `duration`, `listed_in` och `description`.

Den viktigaste kolumnen för RAG-applikationen blev `rag_text`, som vi skapade själva. Den samlar information från flera kolumner till en sammanhängande text. På så sätt får AI-systemet mer kontext när det söker efter relevanta svar.

## 4. Datakvalitet och preprocessing

Först läste vi in originalfilen `netflix_titles.csv`. Sedan kontrollerade vi datasetets storlek, kolumner, datatyper och saknade värden.

Vi såg att vissa kolumner hade tomma värden. För att göra datan mer användbar ersatte vi saknade textvärden med `Unknown`. Det gör att varje rad fortfarande kan användas även om viss information saknas.

Vi kontrollerade också dubbletter. Dubbletter kan vara ett problem eftersom samma information då kan räknas flera gånger eller påverka sökresultatet i RAG-systemet.

Efter det rensade vi extra mellanslag i textkolumner. Detta är viktigt eftersom till exempel `" Sweden "` och `"Sweden"` annars kan behandlas som olika värden.

Till sist skapade vi kolumnen `rag_text` och sparade den rensade datan som `cleaned_data.csv`.

## 5. RAG-applikationen

I den andra notebooken byggde vi RAG-applikationen. Först läste vi in den rensade datan. Sedan skapade vi ett mindre urval som användes i RAG-demonstrationen.

Raderna omvandlades till LangChain `Document`-objekt. Varje dokument innehöll texten från `rag_text` och metadata som titel, typ, land och utgivningsår.

Därefter skapade vi embeddings med Gemini. Embeddings betyder att texten omvandlas till numeriska vektorer. Dessa vektorer sparades i ChromaDB, som fungerar som en vektordatabas.

När vektordatabasen var skapad byggde vi en retriever. Retrieverns uppgift är att hitta de mest relevanta dokumenten när användaren ställer en fråga.

Till sist kopplade vi retrievern till Gemini med en prompt. Prompten instruerade modellen att bara svara baserat på informationen i datasetet.

## 6. Begränsning med API-kvot

Vi kunde inte använda hela datasetet i RAG-applikationen eftersom embedding-API:t gav felet `RESOURCE_EXHAUSTED`. Det betyder att API-gränsen eller kvoten överskreds.

För att lösa detta använde vi ett mindre urval:

- alla titlar kopplade till Sverige
- 30 slumpmässiga andra titlar

Detta gjorde att RAG-applikationen fungerade tekniskt, samtidigt som hela datasetet fortfarande rensades i preprocessing-delen.

## 7. Testning

Vi testade RAG-systemet med frågor där svaret fanns i urvalet, till exempel frågor om Netflix-titlar från Sverige. Systemet kunde då hämta relevanta dokument från ChromaDB och skapa ett svar baserat på dessa dokument.

Vi testade också en fråga där svaret inte fanns, till exempel titlar från Mars. Då svarade systemet att informationen inte kunde hittas i datasetet. Detta var viktigt eftersom ett RAG-system inte ska hitta på svar när information saknas.

## 8. Resultat

Resultatet blev en fungerande enkel RAG-applikation. Den kan söka i den rensade Netflix-datan och svara på frågor baserat på informationen i datasetet.

Projektet visar också att preprocessing är en viktig del av arbetet. Utan rensad och tydlig data blir det svårare för AI-systemet att hitta rätt information.

## 9. Slutsats

Projektet visar sambandet mellan datakvalitet och AI. RAG-system är beroende av bra data. Om datan är ofullständig, inkonsekvent eller ostrukturerad kan svaren bli sämre.

Genom att rensa datasetet, hantera saknade värden, kontrollera dubbletter och skapa en tydlig `rag_text` gjorde vi datan mer användbar för AI-systemet.

En begränsning var API-kvoten, vilket gjorde att vi behövde använda ett mindre urval i RAG-demonstrationen. Trots detta uppnåddes projektets mål: att visa hur rensad data kan användas i en enkel RAG-applikation.

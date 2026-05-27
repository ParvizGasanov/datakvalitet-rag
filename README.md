# Datakvalitet och RAG-system

Detta projekt är gjort av Parviz och Meridona.

## Syfte

Syftet med projektet är att arbeta med datakvalitet och bygga en enkel RAG-applikation baserad på ett Netflix-dataset.

## Dataset

Vi använder datasetet Netflix Movies and TV Shows från Kaggle.

Datasetet innehåller information om filmer och TV-serier, till exempel titel, typ, land, år, kategori och beskrivning.

## Projektstruktur

- `data/netflix_titles.csv` innehåller originaldatan.
- `data/cleaned_data.csv` innehåller den rensade datan.
- `notebooks/01_data_preprocessing.ipynb` innehåller datarensning och förberedelse.
- `notebooks/02_rag_application.ipynb` innehåller RAG-applikationen.
- `requirements.txt` innehåller projektets Python-paket.
- `.env` innehåller API-nyckeln och ska inte laddas upp till GitHub.
- `.gitignore` ser till att känsliga och onödiga filer inte laddas upp.

## Datarensning

I preprocessing-notebooken har vi:

- läst in CSV-filen
- kontrollerat kolumner och datatyper
- kontrollerat saknade värden
- fyllt saknade textvärden med `Unknown`
- kontrollerat och tagit bort dubbletter
- rensat extra mellanslag i textkolumner
- skapat kolumnen `rag_text`
- sparat den rensade datan som `cleaned_data.csv`

## RAG-applikation

I RAG-notebooken har vi:

- läst in den rensade datan
- skapat ett mindre urval för RAG
- omvandlat rader till LangChain Document-objekt
- skapat embeddings med Gemini
- sparat vektorerna i ChromaDB
- skapat en retriever
- kopplat retrievern till Gemini
- testat frågor mot datasetet

På grund av API-begränsningar använde vi ett mindre urval i RAG-demonstrationen:
alla titlar kopplade till Sverige och 30 slumpmässiga andra titlar.

## Viktigt

API-nyckeln ligger i `.env` och ska inte delas eller laddas upp till GitHub.

## Slutsats

I projektet har vi arbetat med datakvalitet genom att kontrollera och rensa ett Netflix-dataset. Vi har hanterat saknade värden, dubbletter och textformat. Därefter byggde vi en enkel RAG-applikation som kan svara på frågor baserat på den rensade datan.

Projektet visar hur datakvalitet påverkar AI-system. Om datan är otydlig, saknas eller är felaktig blir också svaren från RAG-systemet sämre. Därför är preprocessing en viktig del innan man använder data i AI-applikationer.

En begränsning i projektet var att embedding-API:t hade kvotbegränsningar. Därför använde vi ett mindre urval i RAG-demonstrationen, men hela datasetet rensades i preprocessing-delen.
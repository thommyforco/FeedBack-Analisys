from fastapi import FastAPI
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
import numpy as np

app = FastAPI()

# Dataset di training minimale
testi = [
    # POSITIVO - Recensione
    "prodotto fantastico ottimo eccellente perfetto adoro",
    "sono molto soddisfatto funziona benissimo consiglio",
    "bellissimo prodotto qualità top soddisfatto felice",
    "spedizione velocissima prodotto come descritto grazie",
    "esperienza meravigliosa tornerò sicuramente bravi",
    "super contento acquisto perfetto lo ricompro",

    # NEGATIVO - Lamentela
    "prodotto pessimo non funziona terribile deluso",
    "servizio orribile problema grave inaccettabile arrabbiato",
    "non funziona rotto difettoso rimborso lamentela",
    "esperienza negativa mai più deluso amareggiato",
    "qualità pessima soldi buttati vergognoso",
    "assistenza inesistente problema irrisolto scandaloso",

    # NEGATIVO - Problema Tecnico
    "problema tecnico errore non carica crash bug",
    "applicazione non funziona errore continuo blocco sistema",
    "crash improvviso perso dati errore tecnico grave",
    "non riesco ad accedere errore login problema tecnico",

    # NEUTRO - Richiesta Info
    "vorrei informazioni come funziona dettagli spiegazione",
    "richiesta informazioni domanda chiarimento quando disponibile",
    "potete spiegarmi come si usa vorrei capire",
    "ho una domanda riguardo al prodotto informazioni",

    # NEUTRO - Fatturazione
    "fattura pagamento bolletta costo prezzo addebito",
    "problema con la fattura importo errato rimborso",
    "non ho ricevuto la fattura pagamento in sospeso",
    "richiesta rimborso pagamento duplicato fattura errata",
]

sentiment_labels = [
    "POSITIVO", "POSITIVO", "POSITIVO", "POSITIVO", "POSITIVO", "POSITIVO",
    "NEGATIVO", "NEGATIVO", "NEGATIVO", "NEGATIVO", "NEGATIVO", "NEGATIVO",
    "NEGATIVO", "NEGATIVO", "NEGATIVO", "NEGATIVO",
    "NEUTRO", "NEUTRO", "NEUTRO", "NEUTRO",
    "NEUTRO", "NEUTRO", "NEUTRO", "NEUTRO",
]

categoria_labels = [
    "Recensione", "Recensione", "Recensione", "Recensione", "Recensione", "Recensione",
    "Lamentela", "Lamentela", "Lamentela", "Lamentela", "Lamentela", "Lamentela",
    "Problema Tecnico", "Problema Tecnico", "Problema Tecnico", "Problema Tecnico",
    "Richiesta Info", "Richiesta Info", "Richiesta Info", "Richiesta Info",
    "Fatturazione", "Fatturazione", "Fatturazione", "Fatturazione",
]

# Addestramento modelli
vectorizer_s = TfidfVectorizer()
X_s = vectorizer_s.fit_transform(testi)
clf_sentiment = DecisionTreeClassifier()
clf_sentiment.fit(X_s, sentiment_labels)

vectorizer_c = TfidfVectorizer()
X_c = vectorizer_c.fit_transform(testi)
clf_categoria = DecisionTreeClassifier()
clf_categoria.fit(X_c, categoria_labels)


class FeedbackRequest(BaseModel):
    testo: str


class FeedbackResponse(BaseModel):
    sentiment: str
    categoria: str


@app.post("/analizza", response_model=FeedbackResponse)
def analizza_feedback(request: FeedbackRequest):
    testo_vec_s = vectorizer_s.transform([request.testo])
    testo_vec_c = vectorizer_c.transform([request.testo])

    sentiment = clf_sentiment.predict(testo_vec_s)[0]
    categoria = clf_categoria.predict(testo_vec_c)[0]

    return FeedbackResponse(sentiment=sentiment, categoria=categoria)


@app.get("/health")
def health():
    return {"status": "ok"}
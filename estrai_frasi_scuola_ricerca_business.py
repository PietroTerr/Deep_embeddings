"""
Estrae 10 frasi relative ad argomenti scolastici/accademici, di ricerca o di
business dal dataset GPT-2 Output Dataset
(https://github.com/openai/gpt-2-output-dataset).

Scarica in streaming (senza salvare tutto il file) webtext.test.jsonl da
Azure Blob Storage, spezza il testo in frasi e seleziona quelle che
contengono parole chiave legate a scuola, ricerca o business.

Uso:
    python estrai_frasi_scuola_ricerca_business.py
"""

import json
import re
import urllib.request

DATASET_URL = "https://openaipublic.blob.core.windows.net/gpt-2/output-dataset/v1/webtext.test.jsonl"
OUTPUT_FILE = "frasi_scuola_ricerca_business.txt"
NUM_FRASI = 10

PAROLE_CHIAVE_SCUOLA = [
    "school", "student", "university", "college", "professor", "teacher",
    "classroom", "curriculum", "degree", "academic", "campus", "homework",
    "exam", "thesis", "scholarship", "education", "tuition", "faculty",
    "kindergarten", "graduate", "undergraduate",
]

PAROLE_CHIAVE_RICERCA = [
    "research", "researcher", "scientist", "laboratory", "experiment",
    "hypothesis", "peer-reviewed", "journal article", "clinical trial",
    "scientific study", "findings show", "published in the journal",
    "data suggest", "study found", "according to the study",
]

PAROLE_CHIAVE_BUSINESS = [
    "business", "company", "startup", "market", "revenue", "profit",
    "CEO", "corporate", "investment", "entrepreneur", "stock", "economy",
    "industry", "sales", "customer", "enterprise", "finance", "executive",
    "shareholder", "venture capital", "quarterly earnings",
]

TUTTE_LE_PAROLE = PAROLE_CHIAVE_SCUOLA + PAROLE_CHIAVE_RICERCA + PAROLE_CHIAVE_BUSINESS

KEYWORD_RE = re.compile(r"\b(" + "|".join(re.escape(p) for p in TUTTE_LE_PAROLE) + r")", re.IGNORECASE)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def frasi_da_testo(testo):
    testo = testo.replace("\n", " ")
    for frase in SENTENCE_SPLIT_RE.split(testo):
        frase = frase.strip()
        if len(frase.split()) >= 5:
            yield frase


def estrai_frasi(url, num_frasi):
    trovate = []
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as risposta:
        for riga in risposta:
            riga = riga.decode("utf-8", errors="ignore").strip()
            if not riga:
                continue
            try:
                record = json.loads(riga)
            except json.JSONDecodeError:
                continue

            for frase in frasi_da_testo(record.get("text", "")):
                if KEYWORD_RE.search(frase):
                    trovate.append(frase)
                    if len(trovate) >= num_frasi:
                        return trovate
    return trovate


def main():
    print(f"Scarico e analizzo: {DATASET_URL}")
    frasi = estrai_frasi(DATASET_URL, NUM_FRASI)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for i, frase in enumerate(frasi, 1):
            f.write(f"{i}. {frase}\n\n")

    print(f"Trovate {len(frasi)} frasi. Salvate in: {OUTPUT_FILE}\n")
    for i, frase in enumerate(frasi, 1):
        print(f"{i}. {frase}\n")


if __name__ == "__main__":
    main()

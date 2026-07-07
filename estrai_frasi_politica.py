"""
Estrae 10 frasi che parlano di politica dal dataset GPT-2 Output Dataset
(https://github.com/openai/gpt-2-output-dataset).

Scarica (in streaming, senza salvare tutto il file) il file webtext.test.jsonl
ospitato su Azure Blob Storage, ne legge le righe JSONL (ognuna con un campo
"text"), spezza il testo in frasi e seleziona quelle che contengono parole
chiave legate alla politica.

Uso:
    python estrai_frasi_politica.py
"""

import json
import re
import urllib.request

DATASET_URL = "https://openaipublic.blob.core.windows.net/gpt-2/output-dataset/v1/webtext.test.jsonl"
OUTPUT_FILE = "frasi_politica.txt"
NUM_FRASI = 10

PAROLE_CHIAVE = [
    "politic", "president", "election", "vote", "voting", "voter",
    "government", "senate", "senator", "congress", "congressional",
    "democrat", "republican", "parliament", "minister", "legislat",
    "campaign", "policy", "policies", "governor", "mayor", "cabinet",
    "diplomat", "geopolit", "lawmaker", "constitution", "referendum",
    "impeach", "administration", "white house", "capitol hill",
]

KEYWORD_RE = re.compile(r"\b(" + "|".join(PAROLE_CHIAVE) + r")", re.IGNORECASE)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def frasi_da_testo(testo):
    testo = testo.replace("\n", " ")
    for frase in SENTENCE_SPLIT_RE.split(testo):
        frase = frase.strip()
        if len(frase.split()) >= 5:
            yield frase


def estrai_frasi_politiche(url, num_frasi):
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
    frasi = estrai_frasi_politiche(DATASET_URL, NUM_FRASI)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for i, frase in enumerate(frasi, 1):
            f.write(f"{i}. {frase}\n\n")

    print(f"Trovate {len(frasi)} frasi. Salvate in: {OUTPUT_FILE}\n")
    for i, frase in enumerate(frasi, 1):
        print(f"{i}. {frase}\n")


if __name__ == "__main__":
    main()

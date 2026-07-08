# 🗺️ Roadmap del Progetto: Analisi Sintattica con Qwen + SupCon
## Fase 1: Setup e Troncamento del Modello
Scelta del Layer: Carica Qwen e seleziona i primi layer (es. mantieni solo fino al Layer 4 o 6) per isolare la sintassi ed eliminare la semantica profonda.
Configurazione QLoRA: Applica QLoRA su questi layer selezionati per rendere l'addestramento leggero ed efficiente.
Testa di Proiezione: Aggiungi in cima a Qwen un piccolo Multi-Layer Perceptron (MLP) composto da 1-2 layer fully connected (es. che riduca la dimensionalità da 1024 a 256).
## Fase 2: Addestramento Sintattico (Contrastive)
Fine-tuning con SupCon Loss: Addestra il blocco Qwen (QLoRA) + Testa di Proiezione usando la Supervised Contrastive Learning Loss.
In questa fase, la loss costringerà il modello a modificare i pesi per avvicinare geometricamente le strutture sintattiche simili (Umano con Umano, GPT con GPT) e allontanare quelle diverse.
## Fase 3: Validazione Visiva (Il controllo con UMAP)
Estrai gli embedding generati dal modello addestrato per un set di frasi di test (puoi usare sia l'output di Qwen che quello della testa di proiezione).
Applica UMAP per ridurre i vettori a 2 dimensioni.
Crea un grafico a dispersione (scatter plot) colorando i punti in base alla label (Umano vs GPT).
Obiettivo: Verificare visivamente la presenza di due nuvole distinte e separate.
## Fase 4: Classificazione e Benchmark (I tuoi due test)
Ora che lo spazio degli embedding è ottimizzato, rimuovi la testa di proiezione e metti a confronto le due strategie sul set di test:
### Strategia A (Classificatore Lineare - Deep Learning):
Blocca i pesi di Qwen+LoRA.
Aggiungi un singolo layer lineare in cima.
Addestralo con la classica Cross-Entropy Loss per pochissimi epoch.
Calcola le metriche (Accuracy, F1-Score).
### Strategia B (Classificatore Classico - Machine Learning):
Estrai gli embedding dal Qwen+LoRA ottimizzato e salvali come una normale matrice di numeri.
Addestra un algoritmo classico come KNN o SVM su questi vettori.
Calcola le stesse metriche.
## Fase 5: Confronto Finale
Confronta i risultati della Strategia A e della Strategia B. Quella che otterrà l'F1-Score più alto (e la maggiore stabilità) sarà la tua pipeline definitiva per il text forensics sintattico.

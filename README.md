# 💧 Avène Product Expert — Agent RAG Multilingue

Agent IA conversationnel capable de répondre à des questions sur les produits Avène en **français, anglais et espagnol**, en s'appuyant sur des notices PDF officielles.

> Projet développé dans le cadre d'une candidature chez **Pierre Fabre Laboratories** (programme IA for All).

## 🎯 Cas d'usage

Automatiser les réponses aux questions produits pour les équipes métiers Pierre Fabre, en s'appuyant sur la documentation officielle des gammes dermo-cosmétiques.

## 🏗️ Architecture
PDF Avène → Chunking → FAISS Vectorstore → Retriever
↓
Question utilisateur → Détection langue → LangGraph Agent → Réponse traduite

## ⚙️ Stack technique

- **LangGraph** — orchestration de l'agent (retrieve → generate)
- **Mistral AI** — LLM + embeddings
- **FAISS** — base vectorielle locale
- **LangChain** — pipeline RAG
- **Streamlit** — interface web déployée
- **langdetect** — détection automatique de la langue

## 🌍 Langues supportées

| Langue | Exemple de question |
|--------|-------------------|
| 🇫🇷 Français | Quelles sont les indications de ce produit ? |
| 🇬🇧 Anglais | Is this product suitable for sensitive skin? |
| 🇪🇸 Espagnol | ¿Cómo se aplica este producto Avène? |

## 🚀 Demo

👉 [Accéder à l'application](https://agent-rag-avene-pierelefabre.streamlit.app/))

## 📦 Installation locale

```bash
git clone https://github.com/Eudes9/agent-rag-avene.git
cd agent-rag-avene
pip install -r requirements.txt
```

Crée un fichier `.env` :
MISTRAL_API_KEY=ta_clé_ici

Lance l'app :
```bash
streamlit run app.py
```

## 👤 Auteur

**Jean-Eudes Gbada** — Data Scientist & AI Engineer
[LinkedIn](https://linkedin.com/in/ton-profil) · [GitHub](https://github.com/Eudes9)

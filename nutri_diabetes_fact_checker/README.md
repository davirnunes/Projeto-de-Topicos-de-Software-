# 🩺 Fact-Checker de Diabetes e Nutrição

Sistema de verificação de alegações sobre diabetes e nutrição usando IA, RAG (Retrieval-Augmented Generation) e bases de conhecimento oficiais.

## Arquitetura

```
alegação do usuário
        │
        ▼
┌───────────────┐      ┌─────────────────┐
│ Classificador │      │    ChromaDB     │
│ TF-IDF + LR   │      │ (base de conhe- │
│ FAKE/REAL      │◄────►│  cimento RAG)   │
└───────┬───────┘      └────────┬────────┘
        │                       │
        ▼                       ▼
┌───────────────────────────────────────┐
│         fact_checker.py               │
│  - Classificação + Confiança          │
│  - Evidências da base oficial         │
│  - Persistência no PostgreSQL         │
└───────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Criar e ativar ambiente virtual
python -m venv venv
.\venv\Scripts\activate    # Windows
source venv/bin/activate   # Linux/Mac

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Raspar dados oficiais (SBD, Ministério da Saúde, SciELO)
python scripts/scraper.py

# 4. Ingerir no ChromaDB
python scripts/batch_ingest.py

# 5. Gerar dataset de treino
python scripts/dataset_builder.py

# 6. Treinar o classificador
python scripts/fact_checker.py --train

# 7. Verificar uma alegação
python scripts/fact_checker.py "Chá de manga cura diabetes"

# 8. Modo interativo
python scripts/fact_checker.py --interactive
```

## Estrutura do Projeto

```
nutri_diabetes_fact_checker/
├── data/
│   ├── raw/
│   │   ├── guidelines/       # Textos oficiais raspados (SBD, MS)
│   │   └── factchecks.json   # Manchetes de fact-checking
│   └── processed/
│       ├── *_full.csv         # Dataset completo
│       ├── *_train.csv        # Split de treino (80%)
│       ├── *_test.csv         # Split de teste (20%)
│       └── classifier.joblib # Modelo treinado
├── db/
│   ├── schema.sql             # DDL do PostgreSQL
│   └── database.py            # Camada de acesso ao banco
├── knowledge_base/
│   └── chromadb/              # Vetores persistidos
├── scripts/
│   ├── scraper.py             # Raspagem de fontes oficiais
│   ├── batch_ingest.py        # Ingestão no ChromaDB
│   ├── dataset_builder.py     # Geração do dataset rotulado
│   └── fact_checker.py        # Motor central (treino + inferência)
├── docker-compose.yml         # PostgreSQL via Docker
├── requirements.txt
├── .gitignore
└── README.md
```

## Componentes

| Componente | Arquivo | Descrição |
|---|---|---|
| **Scraper** | `scraper.py` | Raspa 10+ fontes oficiais (SBD, MS, SciELO) + fact-checks |
| **Ingestão** | `batch_ingest.py` | Processa .pdf e .txt, embeddings multilíngues, dedup por hash |
| **Dataset** | `dataset_builder.py` | 60+ exemplos curados, dedup, train/test split |
| **Classificador** | `fact_checker.py` | TF-IDF + Logistic Regression + busca RAG no ChromaDB |
| **Banco** | `database.py` | Context-manager, rollback automático, INSERT/SELECT |

## PostgreSQL (opcional)

```bash
# Subir o banco com Docker
docker-compose up -d

# O schema é aplicado automaticamente via docker-entrypoint-initdb.d
```

## Modelo de Embeddings

Usa `paraphrase-multilingual-MiniLM-L12-v2` (multilíngue, incluindo português) em vez do `all-MiniLM-L6-v2` (apenas inglês), garantindo qualidade na busca semântica de textos em português.

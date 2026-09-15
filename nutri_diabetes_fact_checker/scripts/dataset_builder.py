import pandas as pd
import os
import re

def clean_text(text):
    """
    Função simples para limpar o texto:
    - Converter para minúsculas
    - Remover caracteres especiais e pontuação excessiva
    - Remover espaços extras
    """
    if not isinstance(text, str):
        return ""
    
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def build_dataset(output_path):
    """
    Gera um dataset inicial (mockado/sintético para MVP)
    e salva em CSV na pasta processed.
    """
    print("Gerando dataset inicial...")
    
    data = [
        # FAKE
        {"text": "Chá de folha de manga cura diabetes em 3 dias.", "label": "FAKE", "source": "fake_news_mock"},
        {"text": "Diabéticos nunca mais precisarão de insulina se comerem quiabo com água em jejum.", "label": "FAKE", "source": "fake_news_mock"},
        {"text": "Mel natural não eleva a glicose no sangue, diabéticos podem comer à vontade.", "label": "FAKE", "source": "fake_news_mock"},
        {"text": "Cortar 100% dos carboidratos cura diabetes tipo 1.", "label": "FAKE", "source": "fake_news_mock"},
        {"text": "A cura do diabetes está no vinagre de maçã tomado toda manhã.", "label": "FAKE", "source": "fake_news_mock"},
        
        # REAL
        {"text": "O diabetes mellitus tipo 2 é uma doença crônica caracterizada pela resistência à insulina.", "label": "REAL", "source": "medical_guidelines_mock"},
        {"text": "É fundamental que pacientes diabéticos controlem a ingestão de carboidratos, priorizando os de baixo índice glicêmico.", "label": "REAL", "source": "medical_guidelines_mock"},
        {"text": "A prática de exercícios físicos regulares ajuda a melhorar a sensibilidade à insulina.", "label": "REAL", "source": "medical_guidelines_mock"},
        {"text": "O uso de insulina é obrigatório no tratamento de pacientes com diabetes tipo 1.", "label": "REAL", "source": "medical_guidelines_mock"},
        {"text": "Monitorar a glicemia capilar diariamente ajuda a prevenir episódios de hipoglicemia e hiperglicemia.", "label": "REAL", "source": "medical_guidelines_mock"},
    ]
    
    df = pd.DataFrame(data)
    
    # Limpeza básica (apenas para exemplo de pipeline)
    df['cleaned_text'] = df['text'].apply(clean_text)
    
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"Dataset salvo com sucesso em: {output_path}")
    print(f"Total de registros: {len(df)}")
    print("\nAmostra do dataset:")
    print(df.head())

if __name__ == "__main__":
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUT_CSV = os.path.join(PROJECT_ROOT, "data", "processed", "diabetes_nutrition_dataset.csv")
    build_dataset(OUTPUT_CSV)

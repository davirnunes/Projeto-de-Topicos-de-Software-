import os
import psycopg2
from psycopg2.extras import RealDictCursor
import json

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "factchecker")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "adminpassword")

def get_connection():
    """Retorna uma conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def test_insert_analysis():
    """
    Testa a inserção de um registro na tabela Analysis_History.
    """
    conn = get_connection()
    if not conn:
        return
        
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        insert_query = """
        INSERT INTO Analysis_History (input_text, classification, confidence_score, matched_sources)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
        """
        
        mock_data = (
            "Chá de folha de manga cura diabetes em 3 dias.",
            "FAKE",
            0.9850,
            json.dumps([{"source": "SBD_cartilha_2024.pdf", "page": 12, "relevance": 0.89}])
        )
        
        cursor.execute(insert_query, mock_data)
        conn.commit()
        
        inserted_row = cursor.fetchone()
        print("Registro inserido com sucesso!")
        print(inserted_row)
        
        cursor.close()
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print("Testando conexão e inserção no banco de dados...")
    test_insert_analysis()

import os
import hashlib
from tqdm import tqdm
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def generate_chunk_id(chunk_text, source_name):
    """Gera um ID único (hash) para o chunk baseado no texto e fonte para evitar duplicidade"""
    content_to_hash = f"{source_name}_{chunk_text}".encode('utf-8')
    return hashlib.md5(content_to_hash).hexdigest()

def process_pdfs_in_directory(raw_dir, chunk_size=1000, chunk_overlap=100):
    """Lê todos os PDFs e retorna os chunks com metadata atualizada."""
    all_chunks = []
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    
    pdf_files = [f for f in os.listdir(raw_dir) if f.lower().endswith('.txt')]
    print(f"Encontrados {len(pdf_files)} TXTs no diretório.")
    
    for filename in tqdm(pdf_files, desc="Processando Documentos"):
        file_path = os.path.join(raw_dir, filename)
        try:
            loader = TextLoader(file_path, encoding='utf-8')
            documents = loader.load()
            chunks = text_splitter.split_documents(documents)
            
            for chunk in chunks:
                # Enriquece o metadata
                chunk.metadata['source_file'] = filename
                chunk.metadata['chunk_id'] = generate_chunk_id(chunk.page_content, filename)
                all_chunks.append(chunk)
        except Exception as e:
            print(f"Erro ao processar {filename}: {e}")
            
    return all_chunks

def batch_ingest_chroma(chunks, persist_directory, batch_size=200):
    """Realiza a ingestão no ChromaDB em lotes."""
    if not chunks:
        print("Nenhum chunk para ingerir.")
        return
        
    print("Inicializando embeddings (HuggingFace)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Inicializa ou carrega a vector store
    vectorstore = Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
    
    # Extrai IDs existentes para não duplicar
    # Note: O Chroma gerencia IDs se passados explicitamente.
    # Vamos extrair apenas os chunks únicos
    unique_chunks = {chunk.metadata['chunk_id']: chunk for chunk in chunks}
    chunks_to_insert = list(unique_chunks.values())
    ids = list(unique_chunks.keys())
    
    print(f"Total de chunks a serem analisados/inseridos: {len(chunks_to_insert)}")
    
    for i in tqdm(range(0, len(chunks_to_insert), batch_size), desc="Ingerindo Lotes no ChromaDB"):
        batch = chunks_to_insert[i:i + batch_size]
        batch_ids = ids[i:i + batch_size]
        
        # Tentar inserir no ChromaDB passando os IDs explícitos.
        # O Chroma geralmente sobrescreve ou ignora IDs repetidos dependendo da versão,
        # mas forçar os IDs ajuda no controle de versão do documento.
        try:
            vectorstore.add_documents(documents=batch, ids=batch_ids)
        except Exception as e:
            print(f"Erro no lote {i}-{i+batch_size}: {e}")

    print("Processo de ingestão em larga escala concluído.")

def main():
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_DATA_DIR = os.path.join(PROJECT_ROOT, "data", "raw", "guidelines")
    CHROMA_DB_DIR = os.path.join(PROJECT_ROOT, "knowledge_base", "chromadb")
    
    if not os.path.exists(RAW_DATA_DIR):
        os.makedirs(RAW_DATA_DIR, exist_ok=True)
        print(f"Diretório {RAW_DATA_DIR} criado. Por favor, baixe PDFs ou rode o crawler.py antes.")
        return
        
    chunks = process_pdfs_in_directory(RAW_DATA_DIR)
    batch_ingest_chroma(chunks, CHROMA_DB_DIR)

if __name__ == "__main__":
    main()

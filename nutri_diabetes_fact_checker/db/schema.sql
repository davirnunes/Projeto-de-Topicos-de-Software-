CREATE TABLE IF NOT EXISTS Analysis_History (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    input_text TEXT NOT NULL,
    classification VARCHAR(50), -- ex: 'REAL', 'FAKE', 'INCONCLUSIVE'
    confidence_score NUMERIC(5, 4),
    matched_sources JSONB,      -- Documentos do ChromaDB que justificaram a decisão
    analysis_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    user_feedback BOOLEAN
);

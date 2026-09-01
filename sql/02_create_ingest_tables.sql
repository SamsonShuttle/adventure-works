CREATE TABLE IF NOT EXISTS ingest.pipeline_runs (
  pipeline_run_id UUID PRIMARY KEY,
  pipeline_name VARCHAR(100) NOT NULL,
  started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  status VARCHAR(20) NOT NULL,
  error_message VARCHAR(500),
  summary JSONB
);
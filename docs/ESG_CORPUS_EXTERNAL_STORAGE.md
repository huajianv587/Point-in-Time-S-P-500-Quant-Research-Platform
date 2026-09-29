# External ESG Corpus

The repository contains the ESG/RAG pipeline, not the raw annual-report corpus.
The PDFs are large and may carry source-specific usage restrictions, so keep them
outside Git and point the runtime at them with `ESG_CORPUS_ROOT`.

## Setup

```bash
export ESG_CORPUS_ROOT="/absolute/path/to/esg_reports"
python scripts/esg_corpus_pipeline.py coverage --corpus-root "$ESG_CORPUS_ROOT"
```

If `ESG_CORPUS_ROOT` is unset, the runtime checks `esg_reports/`, then the
project sibling directory `../量化平台数据/esg_reports`, and finally the legacy
`ESG报告/` path. A missing corpus is reported as unavailable; it is not replaced
with synthetic evidence.

The external corpus should include the PDF files and, when available, the small
CSV audit files (`company_file_inventory_20_companies.csv`,
`download_check.csv`, and `pdf_year_audit.csv`). Generated embeddings and corpus
manifests belong under ignored `storage/`.

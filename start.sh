#!/usr/bin/env bash

echo "Running ETL..."
python scripts/create_clean_table.py

echo "Starting FastAPI backend..."
uvicorn backend.main:app --host 0.0.0.0 --port 8000 &

echo "Starting Streamlit frontend..."
streamlit run app.py --server.port 10000 --server.address 0.0.0.0
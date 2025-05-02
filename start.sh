#!/bin/bash
# Arquivo start.sh

# Inicia o backend
docker-compose up -d

# Inicia o frontend
cd frontend
npm run dev
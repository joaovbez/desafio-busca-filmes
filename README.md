# desafio-busca-filmes

Um repo que busca construir uma busca eficiente para achar filmes de um dataset específico.

## Como rodar

Dois processos, dois terminais. O `/search` devolve filmes reais do CSV, ainda **sem** busca inteligente: qualquer `q` retorna os mais bem avaliados.

O arquivo `tmdb_5000_movies.csv` fica na **raiz** do repositório (não vai para o Git).

### Backend (FastAPI)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

No terminal deve aparecer algo como `loaded 4803 movies`.

API e Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend (Vite)

```bash
cd frontend
npm install
npm run dev
```

Página: [http://localhost:5173](http://localhost:5173). Os dois processos precisam estar no ar.

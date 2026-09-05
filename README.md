# desafio-busca-filmes

Um repo que busca construir uma busca eficiente para achar filmes de um dataset específico.

## Como rodar (Etapa 1)

Dois processos, dois terminais. Ainda **não** há busca real. A API já libera CORS para `http://localhost:5173`. O React tem a caixa de busca, mas **ainda não** chama o `/search`.

### Backend (FastAPI)

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

API e Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

Teste o `GET /search` com algum `q` (ex.: `Inception`). A query volta no JSON; o filme da lista é um stub, não veio do CSV.

### Frontend (Vite)

```bash
cd frontend
npm install
npm run dev
```

Página: [http://localhost:5173](http://localhost:5173) (caixa + botão; ainda sem `fetch`).

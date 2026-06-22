# Servidor — Processamento de Reconhecimento Facial

API responsável por detectar e reconhecer rostos, e gerenciar o estado da chamada durante a janela de 15 minutos.

## Instalação

```bash
cd servidor
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edite o .env com sua API_KEY e demais configurações
```

> **Nota:** `face_recognition` depende do `dlib`, que pode exigir compilador C++ instalado no sistema. Consulte a [documentação do dlib](http://dlib.net/) caso a instalação falhe.

## Executando

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A documentação interativa (Swagger) fica disponível em `http://localhost:8000/docs`.

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| POST | `/chamada/iniciar` | Inicia a janela de chamada para uma turma |
| POST | `/chamada/frame` | Recebe um frame e processa reconhecimento |
| GET | `/chamada/status` | Consulta presentes/ausentes em tempo real |
| POST | `/chamada/finalizar` | Encerra a janela e persiste o resultado |

Todas as rotas (exceto `/docs`) exigem o header `X-API-Key`.

## Estrutura

```
servidor/
├── app/
│   ├── main.py              # ponto de entrada FastAPI
│   ├── api/                 # rotas/endpoints
│   ├── core/                # lógica de detecção, reconhecimento e presença
│   ├── modelos/             # schemas Pydantic
│   └── banco/               # acesso a dados (SQLite)
├── dados/
│   ├── encodings/           # banco de encodings por turma (.pkl) — não versionado
│   └── db/                  # banco de presenças (SQLite) — não versionado
└── testes/                  # testes automatizados
```

"""
Ponto de entrada da API do servidor de reconhecimento facial.

Roda na máquina que processa o reconhecimento (não no PC da sala).
Para iniciar: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

TODO:
- Instanciar o FastAPI app
- Registrar os routers de servidor/app/api/
- Middleware de autenticação (X-API-Key)
"""

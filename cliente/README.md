# Cliente — Captura na Sala de Aula

Script leve que roda no PC da sala de aula. Não carrega nenhum modelo de IA — apenas captura frames da webcam e os envia para o servidor de processamento.

## Instalação

```bash
cd cliente
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# edite o .env com a URL do servidor (IP do Tailscale) e a API_KEY
```

## Executando

```bash
python app/captura.py
```

O script abre a câmera, captura frames periodicamente durante a janela de chamada e os envia ao servidor. Ao final da janela (15 minutos, configurável no servidor), o script encerra automaticamente.

## Pré-requisitos de rede

Este cliente precisa alcançar o servidor através do [Tailscale](https://tailscale.com/). Veja [`infra/tailscale.md`](../infra/tailscale.md) para o passo a passo de configuração.

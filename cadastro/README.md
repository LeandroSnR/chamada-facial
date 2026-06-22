# Cadastro — Geração de Encodings

Script offline que transforma as fotos oficiais dos alunos em encodings faciais, usados posteriormente pelo servidor para reconhecimento.

Esse script roda **uma vez por turma** (ou sempre que uma foto for atualizada), não durante a chamada do dia a dia.

## Organização das fotos

Coloque as fotos oficiais seguindo esta estrutura (não versionada — veja `.gitignore`):

```
cadastro/fotos_oficiais/
└── 9A/
    ├── 123_ana.jpg
    ├── 124_bruno.jpg
    └── 125_carla.jpg
```

Recomendações para as fotos:
- Um rosto por imagem, em boa iluminação e de frente (similar a foto de documento).
- Nome do arquivo no formato `<matricula>_<nome>.jpg` (usado para identificar o aluno no encoding).

## Instalação

```bash
cd cadastro
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Executando

```bash
python gerar_encodings.py --turma 9A
```

Isso gera o arquivo `servidor/dados/encodings/9A.pkl`, que o servidor usa para comparar os rostos capturados durante a chamada.

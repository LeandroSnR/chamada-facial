# Chamada Facial 📸✅

Sistema de registro de presença escolar usando reconhecimento facial, com arquitetura cliente-servidor: a captura roda em uma máquina leve (PC da sala de aula) e o processamento pesado roda em outra máquina, comunicando-se de forma segura através de uma rede privada (Tailscale).

> Projeto criado com fins de aprendizado prático de Visão Computacional (OpenCV) e arquitetura cliente-servidor.

## Como funciona

Durante os primeiros 15 minutos da aula, uma câmera apontada para a sala captura frames periodicamente. Cada frame é processado pelo servidor, que detecta e reconhece os rostos presentes, comparando-os com o banco de encodings da turma. Alunos reconhecidos em qualquer frame da janela são marcados como **presentes**; os demais ficam como **ausentes** até confirmação manual do professor.

```
┌────────────────┐        rede privada         ┌──────────────────────┐
│  PC da sala     │ ────── (Tailscale) ───────► │  Servidor             │
│  (cliente)      │ ◄──────────────────────────  │  (processamento)     │
│                 │                              │                      │
│  - Captura      │                              │  - Detecção de rosto │
│    frames       │                              │  - Reconhecimento    │
│  - Sem IA local │                              │  - Registro de       │
│                 │                              │    presença          │
└────────────────┘                              └──────────────────────┘
```

## Estrutura do projeto

```
chamada-facial/
├── cadastro/          # Script para gerar encodings a partir das fotos oficiais
├── cliente/           # App leve que roda no PC da sala (captura + envio)
├── servidor/          # API que processa reconhecimento facial e gerencia a chamada
├── docs/              # Documentação adicional e diagramas
└── infra/             # Configurações de rede/deploy (Tailscale, etc.)
```

Veja o README de cada subpasta para detalhes de instalação e uso.

## Stack

- **OpenCV** — captura de vídeo e detecção de rosto
- **face_recognition** (dlib) — geração e comparação de encodings faciais
- **FastAPI** — API do servidor de processamento
- **SQLite** — persistência do histórico de chamadas
- **Tailscale** — rede privada entre o cliente e o servidor

## Privacidade e dados sensíveis

Este projeto lida com dados biométricos de menores de idade. Antes de usar em qualquer contexto real, leia [`docs/PRIVACIDADE.md`](docs/PRIVACIDADE.md).

Resumindo os princípios adotados:
- Frames de vídeo nunca são persistidos — são processados em memória e descartados.
- Apenas os encodings (vetores numéricos) são armazenados, nunca as fotos originais além das já existentes no cadastro oficial.
- Toda comunicação entre cliente e servidor passa por rede privada (Tailscale), não por internet pública exposta.
- Pressupõe autorização de uso de imagem já formalizada com responsáveis/alunos.

## Status do projeto

🚧 Em desenvolvimento — consulte as [issues](../../issues) para acompanhar o progresso.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

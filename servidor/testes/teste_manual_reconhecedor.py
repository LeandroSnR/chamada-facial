"""
Script de teste manual do reconhecedor.py: gera encodings de duas (ou
mais) fotos e verifica se o sistema reconhece corretamente a mesma
pessoa em fotos diferentes, e rejeita pessoas diferentes.

Uso:
    python testes/teste_manual_reconhecedor.py foto_cadastro.jpg foto_chamada.jpg [foto_outra_pessoa.jpg]

- foto_cadastro.jpg: simula a foto oficial (cadastro)
- foto_chamada.jpg: simula uma foto capturada na chamada (mesma pessoa)
- foto_outra_pessoa.jpg (opcional): foto de outra pessoa, para validar
  que o sistema NÃO confunde os dois.

Cada imagem deve conter exatamente um rosto claramente visível.
"""

import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.detector import DetectorRosto
from app.core.reconhecedor import (
    EncodingConhecido,
    THRESHOLD_PADRAO,
    gerar_encoding,
    identificar,
)


def encoding_da_foto(caminho: str, detector: DetectorRosto):
    frame = cv2.imread(caminho)
    if frame is None:
        print(f"Não foi possível ler: {caminho}")
        sys.exit(1)

    rostos = detector.detectar(frame)
    if not rostos:
        print(f"Nenhum rosto detectado em: {caminho}")
        sys.exit(1)
    if len(rostos) > 1:
        print(
            f"Atenção: {len(rostos)} rostos detectados em {caminho}, "
            "usando o primeiro (confiança mais alta não garantida pela ordem)."
        )

    encoding = gerar_encoding(frame, rostos[0])
    if encoding is None:
        print(f"Não foi possível gerar encoding para o rosto em: {caminho}")
        sys.exit(1)

    return encoding


def main() -> None:
    if len(sys.argv) < 3:
        print(
            "Uso: python testes/teste_manual_reconhecedor.py "
            "foto_cadastro.jpg foto_chamada.jpg [foto_outra_pessoa.jpg]"
        )
        sys.exit(1)

    caminho_cadastro = sys.argv[1]
    caminho_chamada = sys.argv[2]
    caminho_outra_pessoa = sys.argv[3] if len(sys.argv) > 3 else None

    detector = DetectorRosto()

    print("Gerando encoding da foto de cadastro...")
    encoding_cadastro = encoding_da_foto(caminho_cadastro, detector)

    print("Gerando encoding da foto da chamada...")
    encoding_chamada = encoding_da_foto(caminho_chamada, detector)

    banco = [
        EncodingConhecido(aluno_id="1", nome="Pessoa do cadastro", vetor=encoding_cadastro)
    ]

    print(f"\nThreshold usado: {THRESHOLD_PADRAO}")

    resultado = identificar(encoding_chamada, banco)
    print(f"\n[Mesma pessoa esperada] Resultado: {resultado}")
    if resultado.aluno_id is not None:
        print("✅ Reconheceu corretamente como a mesma pessoa.")
    else:
        print("❌ NÃO reconheceu — pode ser threshold muito exigente, ou fotos muito diferentes.")

    if caminho_outra_pessoa:
        print("\nGerando encoding da foto de outra pessoa...")
        encoding_outra = encoding_da_foto(caminho_outra_pessoa, detector)
        resultado_outra = identificar(encoding_outra, banco)
        print(f"\n[Pessoa diferente esperada] Resultado: {resultado_outra}")
        if resultado_outra.aluno_id is None:
            print("✅ Corretamente NÃO confundiu com outra pessoa.")
        else:
            print("❌ ALERTA: confundiu com outra pessoa — threshold pode estar permissivo demais.")


if __name__ == "__main__":
    main()

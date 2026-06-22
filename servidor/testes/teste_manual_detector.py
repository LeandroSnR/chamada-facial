"""
Script de teste manual e visual do DetectorRosto.

Não é um teste automatizado (pytest) — é uma forma rápida de você
validar visualmente se a detecção está funcionando bem com uma foto
real, antes de integrar ao resto do sistema.

Uso:
    python testes/teste_manual_detector.py caminho/para/sua_foto.jpg

Gera um arquivo `saida_deteccao.jpg` na mesma pasta, com retângulos
desenhados sobre os rostos detectados e a confiança de cada um.
"""

import sys
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.core.detector import DetectorRosto


def main() -> None:
    if len(sys.argv) != 2:
        print("Uso: python testes/teste_manual_detector.py <caminho_da_imagem>")
        sys.exit(1)

    caminho_imagem = Path(sys.argv[1])
    if not caminho_imagem.exists():
        print(f"Arquivo não encontrado: {caminho_imagem}")
        sys.exit(1)

    frame = cv2.imread(str(caminho_imagem))
    if frame is None:
        print(f"Não foi possível ler a imagem (formato inválido?): {caminho_imagem}")
        sys.exit(1)

    detector = DetectorRosto()
    rostos = detector.detectar(frame)

    print(f"Rostos detectados: {len(rostos)}")
    for i, rosto in enumerate(rostos, start=1):
        print(f"  [{i}] confiança={rosto.confianca:.2f} caixa={rosto.caixa}")

    # Desenha as caixas no frame original para inspeção visual
    for rosto in rostos:
        x1, y1, x2, y2 = rosto.caixa
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        texto = f"{rosto.confianca:.2f}"
        cv2.putText(
            frame, texto, (x1, max(y1 - 10, 0)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2,
        )

    saida = Path(__file__).resolve().parent / "saida_deteccao.jpg"
    cv2.imwrite(str(saida), frame)
    print(f"\nImagem com detecções salva em: {saida}")


if __name__ == "__main__":
    main()

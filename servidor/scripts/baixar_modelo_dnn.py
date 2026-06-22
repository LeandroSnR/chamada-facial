"""
Baixa os arquivos do modelo de detecção facial DNN do OpenCV.

Esses arquivos não são versionados no Git (são binários e podem ser
obtidos sempre da mesma fonte oficial), então este script precisa ser
rodado uma vez após clonar o repositório, antes de iniciar o servidor.

Uso:
    python scripts/baixar_modelo_dnn.py
"""

import sys
import urllib.request
from pathlib import Path

DESTINO = Path(__file__).resolve().parent.parent / "app" / "modelos_dnn"

ARQUIVOS = {
    "deploy.prototxt": (
        "https://raw.githubusercontent.com/opencv/opencv/master/"
        "samples/dnn/face_detector/deploy.prototxt"
    ),
    "res10_300x300_ssd_iter_140000.caffemodel": (
        "https://raw.githubusercontent.com/opencv/opencv_3rdparty/"
        "dnn_samples_face_detector_20170830/"
        "res10_300x300_ssd_iter_140000.caffemodel"
    ),
}


def baixar(nome: str, url: str, destino: Path) -> None:
    caminho = destino / nome
    if caminho.exists():
        print(f"[OK] {nome} já existe, pulando.")
        return

    print(f"Baixando {nome}...")
    try:
        urllib.request.urlretrieve(url, caminho)
        tamanho_kb = caminho.stat().st_size / 1024
        print(f"[OK] {nome} baixado ({tamanho_kb:.0f} KB)")
    except Exception as e:
        print(f"[FALHA] Não foi possível baixar {nome}: {e}")
        sys.exit(1)


def main() -> None:
    DESTINO.mkdir(parents=True, exist_ok=True)
    print(f"Destino: {DESTINO}\n")

    for nome, url in ARQUIVOS.items():
        baixar(nome, url, DESTINO)

    print("\nModelo de detecção facial pronto para uso.")


if __name__ == "__main__":
    main()

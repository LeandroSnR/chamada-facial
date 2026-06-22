"""
Wrapper sobre o OpenCV para detecção de rostos em um frame, usando o
modelo DNN (SSD + ResNet-10) que acompanha o OpenCV.

Por que DNN em vez de Haar Cascade: a câmera da sala captura rostos em
ângulos e iluminação variados (diferente de uma foto de documento), e o
DNN é bem mais robusto a essa variação, com custo de performance baixo
para o volume de 1 frame a cada poucos segundos.

Responsabilidades deste módulo:
- Carregar o modelo DNN uma única vez (reaproveitado entre chamadas)
- Receber um frame (numpy array, formato BGR do OpenCV)
- Detectar bounding boxes de rostos com confiança acima de um limiar
- Retornar os recortes de rosto (crops) prontos para gerar encoding
  no módulo reconhecedor.py
"""

from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

# Arquivos do modelo, baixados via servidor/scripts/baixar_modelo_dnn.py
_DIR_MODELOS = Path(__file__).resolve().parent.parent / "modelos_dnn"
_CAMINHO_PROTOTXT = _DIR_MODELOS / "deploy.prototxt"
_CAMINHO_PESOS = _DIR_MODELOS / "res10_300x300_ssd_iter_140000.caffemodel"

# Tamanho de entrada esperado pelo modelo (fixo pela arquitetura treinada)
_TAMANHO_ENTRADA = (300, 300)

# Confiança mínima para considerar uma detecção válida.
# Valores entre 0.5 e 0.7 são um bom ponto de partida: abaixo disso,
# o modelo passa a aceitar muitos falsos positivos (sombras, objetos).
CONFIANCA_MINIMA_PADRAO = 0.6


@dataclass
class RostoDetectado:
    """Representa um rosto encontrado em um frame."""

    caixa: tuple[int, int, int, int]  # (x1, y1, x2, y2) em pixels do frame original
    confianca: float
    recorte: np.ndarray  # imagem (BGR) já recortada, pronta para gerar encoding


class DetectorRosto:
    """
    Carrega o modelo DNN uma única vez e expõe o método `detectar`,
    reutilizado a cada frame recebido pela API.
    """

    def __init__(self, confianca_minima: float = CONFIANCA_MINIMA_PADRAO):
        if not _CAMINHO_PROTOTXT.exists() or not _CAMINHO_PESOS.exists():
            raise FileNotFoundError(
                "Arquivos do modelo DNN não encontrados em "
                f"'{_DIR_MODELOS}'. Rode primeiro:\n"
                "  python scripts/baixar_modelo_dnn.py"
            )

        self.confianca_minima = confianca_minima
        self._rede = cv2.dnn.readNetFromCaffe(
            str(_CAMINHO_PROTOTXT), str(_CAMINHO_PESOS)
        )

    def detectar(self, frame: np.ndarray) -> list[RostoDetectado]:
        """
        Detecta todos os rostos em um frame.

        Args:
            frame: imagem no formato BGR (padrão do OpenCV), shape (H, W, 3).

        Returns:
            Lista de RostoDetectado, uma entrada por rosto encontrado,
            já ordenada implicitamente pela ordem de detecção do modelo.
        """
        altura, largura = frame.shape[:2]

        # O modelo espera um "blob" 300x300, normalizado pela média de
        # subtração usada no treinamento original (104, 177, 123 em BGR).
        blob = cv2.dnn.blobFromImage(
            frame,
            scalefactor=1.0,
            size=_TAMANHO_ENTRADA,
            mean=(104.0, 177.0, 123.0),
            swapRB=False,
            crop=False,
        )
        self._rede.setInput(blob)
        deteccoes = self._rede.forward()

        rostos: list[RostoDetectado] = []

        # `deteccoes` tem shape (1, 1, N, 7); cada linha é uma detecção
        # candidata: [_, _, confianca, x1, y1, x2, y2] em coordenadas
        # normalizadas (0.0 a 1.0), que precisam ser escaladas pro
        # tamanho real do frame.
        for i in range(deteccoes.shape[2]):
            confianca = float(deteccoes[0, 0, i, 2])
            if confianca < self.confianca_minima:
                continue

            caixa_normalizada = deteccoes[0, 0, i, 3:7]
            x1, y1, x2, y2 = (
                caixa_normalizada * np.array([largura, altura, largura, altura])
            ).astype(int)

            # Garante que a caixa não saia dos limites do frame (o modelo
            # pode retornar coordenadas levemente fora em casos de borda).
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(largura, x2), min(altura, y2)

            if x2 <= x1 or y2 <= y1:
                continue  # caixa inválida, descarta

            recorte = frame[y1:y2, x1:x2].copy()

            rostos.append(
                RostoDetectado(
                    caixa=(x1, y1, x2, y2),
                    confianca=confianca,
                    recorte=recorte,
                )
            )

        return rostos

"""
Geração e comparação de encodings faciais, usando face_recognition (dlib).

Um encoding é um vetor de 128 números que representa as características
geométricas de um rosto. Rostos da mesma pessoa geram vetores próximos
entre si (pequena distância euclidiana); rostos de pessoas diferentes
geram vetores distantes.

Este módulo reaproveita a detecção já feita pelo detector.py (OpenCV DNN)
em vez de deixar o face_recognition redetectar o rosto internamente —
evita trabalho duplicado e mantém consistência entre "o que foi
detectado no frame" e "o que foi usado para gerar o encoding".

Responsabilidades:
- Gerar o encoding de um rosto, dada a imagem completa e a caixa já
  detectada pelo detector.py
- Comparar um encoding contra um banco de encodings conhecidos (de uma
  turma) e retornar o melhor match, se houver, respeitando o threshold
"""

from dataclasses import dataclass

import face_recognition
import numpy as np

from app.core.detector import RostoDetectado

# Distância máxima para considerar dois encodings como a mesma pessoa.
# face_recognition usa distância euclidiana entre vetores de 128 posições.
# Valores menores = mais exigente (menos falsos positivos, mais falsos
# negativos). 0.6 é o valor de referência da própria biblioteca; usamos
# um pouco mais conservador (0.55) porque temos múltiplas chances ao
# longo da janela de 15 minutos, então podemos exigir mais confiança por
# tentativa sem aumentar muito a chance de "falso ausente".
THRESHOLD_PADRAO = 0.55


@dataclass
class EncodingConhecido:
    """Um encoding já cadastrado, associado a um aluno."""

    aluno_id: str
    nome: str
    vetor: np.ndarray  # shape (128,)


@dataclass
class ResultadoReconhecimento:
    """Resultado da tentativa de identificar um rosto."""

    aluno_id: str | None  # None significa "não identificado"
    nome: str | None
    distancia: float | None  # menor distância encontrada, para diagnóstico


def gerar_encoding(frame_bgr: np.ndarray, rosto: RostoDetectado) -> np.ndarray | None:
    """
    Gera o encoding de um rosto já detectado.

    Args:
        frame_bgr: o frame original completo (formato BGR do OpenCV),
            de onde o rosto foi recortado.
        rosto: o RostoDetectado retornado pelo detector.py, contendo a
            caixa (x1, y1, x2, y2) no frame original.

    Returns:
        Vetor numpy de shape (128,), ou None se não foi possível gerar
        o encoding (caso raro: dlib não conseguir extrair landmarks
        suficientes do recorte, mesmo já tendo sido detectado pelo
        OpenCV — acontece ocasionalmente em rostos muito pequenos ou
        de baixa qualidade).
    """
    # face_recognition trabalha em RGB; o OpenCV usa BGR por padrão.
    frame_rgb = frame_bgr[:, :, ::-1]

    x1, y1, x2, y2 = rosto.caixa
    # face_recognition espera localizações no formato (top, right, bottom, left)
    localizacao = (y1, x2, y2, x1)

    encodings = face_recognition.face_encodings(
        frame_rgb, known_face_locations=[localizacao]
    )

    if not encodings:
        return None

    return encodings[0]


def identificar(
    encoding: np.ndarray,
    banco: list[EncodingConhecido],
    threshold: float = THRESHOLD_PADRAO,
) -> ResultadoReconhecimento:
    """
    Compara um encoding contra o banco de encodings conhecidos da turma
    e retorna o melhor match dentro do threshold, se houver.

    Args:
        encoding: vetor gerado por gerar_encoding().
        banco: lista de encodings cadastrados (normalmente, os alunos
            de uma turma específica).
        threshold: distância máxima para considerar match.

    Returns:
        ResultadoReconhecimento com aluno_id/nome preenchidos se houver
        match dentro do threshold, ou None nesses campos caso contrário.
        `distancia` é sempre preenchida quando o banco não está vazio,
        útil para logging/diagnóstico mesmo sem match.
    """
    if not banco:
        return ResultadoReconhecimento(aluno_id=None, nome=None, distancia=None)

    vetores_banco = np.array([item.vetor for item in banco])
    distancias = np.linalg.norm(vetores_banco - encoding, axis=1)

    indice_mais_proximo = int(np.argmin(distancias))
    menor_distancia = float(distancias[indice_mais_proximo])

    if menor_distancia <= threshold:
        melhor = banco[indice_mais_proximo]
        return ResultadoReconhecimento(
            aluno_id=melhor.aluno_id,
            nome=melhor.nome,
            distancia=menor_distancia,
        )

    return ResultadoReconhecimento(aluno_id=None, nome=None, distancia=menor_distancia)

"""
Script offline para gerar o banco de encodings de uma turma.

Responsabilidades:
- Ler as fotos oficiais de cadastro/fotos_oficiais/<turma_id>/<aluno_id>.jpg
- Detectar o rosto em cada foto (deve haver exatamente 1 rosto por foto)
- Gerar o encoding facial (face_recognition)
- Salvar em servidor/dados/encodings/<turma_id>.pkl

Uso:
    python gerar_encodings.py --turma 9A

TODO: implementar nas próximas etapas.
"""

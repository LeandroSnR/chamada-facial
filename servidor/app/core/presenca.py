"""
Gerenciamento do estado da chamada (janela de 15 minutos).

Responsabilidades:
- Manter em memória o estado da turma durante a janela ativa
- Marcar aluno como presente (com timestamp) na primeira vez que é reconhecido
- Ignorar (não reprocessar) alunos já confirmados, para economizar comparações
- Ao fim da janela, calcular ausentes = alunos da turma - presentes
- Persistir resultado final no banco (SQLite)

TODO: implementar nas próximas etapas.
"""

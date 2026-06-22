"""
Script cliente — roda no PC da sala de aula.

Responsabilidades:
- Abrir a câmera via OpenCV (sem nenhum modelo de IA carregado)
- Capturar 1 frame a cada INTERVALO_CAPTURA_SEGUNDOS
- Redimensionar/comprimir o frame antes de enviar (economia de banda)
- Enviar o frame via POST /chamada/frame para o servidor (com X-API-Key)
- Encerrar automaticamente ao fim da janela de chamada

TODO: implementar nas próximas etapas.
"""

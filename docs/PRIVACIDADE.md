# Privacidade e Tratamento de Dados

Este projeto processa dados biométricos (rostos) de alunos, em parte menores de idade. Isso é uma categoria de dado sensível segundo a LGPD (Lei Geral de Proteção de Dados), e merece cuidado mesmo em projetos de aprendizado.

## Pressupostos deste projeto

- A instituição já obteve autorização de uso de imagem dos responsáveis/alunos para fins escolares.
- O uso aqui descrito (registro de presença) deve estar coberto por essa autorização, ou por uma autorização específica e informada sobre o uso de reconhecimento facial.
- Este projeto é um material de estudo/portfólio. Antes de qualquer uso em produção real numa instituição, recomenda-se validação jurídica formal (DPO/responsável por dados da instituição) sobre a adequação à LGPD.

## Princípios de minimização de dados adotados

1. **Frames de vídeo não são persistidos.** Cada frame é processado em memória pelo servidor e descartado imediatamente após a tentativa de reconhecimento. Não há gravação de vídeo da sala.
2. **Apenas encodings são armazenados, não fotos do dia a dia.** O banco de dados do servidor guarda vetores numéricos (encodings), que não são reversíveis para uma imagem de rosto.
3. **As fotos oficiais usadas no cadastro ficam fora do controle de versão** (`.gitignore`), e idealmente devem ser removidas da máquina de cadastro após a geração dos encodings.
4. **Comunicação em rede privada.** O tráfego entre o PC da sala e o servidor de processamento passa por uma rede privada (Tailscale), não por internet pública exposta.
5. **Histórico de presença é o único dado de longo prazo.** O banco SQLite guarda apenas: turma, data, aluno, status (presente/ausente) e horário — não guarda nenhuma imagem.

## Direitos dos titulares (alunos/responsáveis)

Em uma implantação real, a instituição deveria garantir:
- Transparência sobre o uso de reconhecimento facial (não apenas "uso de imagem" genérico).
- Possibilidade de optar por chamada manual, caso o responsável não autorize o reconhecimento facial especificamente.
- Direito de exclusão dos encodings ao final do vínculo do aluno com a instituição.

## Recomendações de segurança técnica adicionais

- Trocar a `API_KEY` padrão antes de qualquer uso real.
- Restringir o acesso à rede Tailscale apenas aos dispositivos estritamente necessários.
- Considerar criptografia em repouso para o arquivo de encodings (`.pkl`), já que, embora não sejam imagens, ainda são dados biométricos.
- Revisar periodicamente quem tem acesso à máquina servidora e ao banco de dados.

---

Este documento é informativo e não substitui orientação jurídica formal.

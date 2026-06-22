# Configuração do Tailscale

Guia para conectar o PC da sala de aula e o servidor de processamento em uma rede privada, sem expor portas na internet pública.

## Por que Tailscale

- Cria uma VPN mesh entre os dispositivos, com IP privado fixo para cada um.
- Tráfego criptografado ponta a ponta.
- Não exige abrir portas no roteador/firewall de nenhum dos dois lados.
- Gratuito para o volume de uso deste projeto (uso pessoal/poucos dispositivos).

## Passo a passo

> TODO: detalhar com prints/comandos durante a implementação.

1. Criar conta em [tailscale.com](https://tailscale.com/).
2. Instalar o cliente Tailscale na máquina servidora (sua máquina pessoal).
3. Instalar o cliente Tailscale no PC da sala de aula.
4. Autenticar os dois dispositivos na mesma conta/tailnet.
5. Anotar o IP privado (`100.x.x.x`) atribuído à máquina servidora.
6. Usar esse IP na variável `SERVIDOR_URL` do `.env` do cliente.
7. (Opcional) Configurar ACLs do Tailscale para restringir que apenas o PC da sala alcance a porta do servidor.

## Verificação

Do PC da sala, testar conectividade:

```bash
ping 100.x.x.x
curl http://100.x.x.x:8000/docs
```

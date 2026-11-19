# Navegação segura no Lattes

Este arquivo orienta uma integração opcional. A skill não exige Browser Use nem um provedor específico.

## Quando usar

Use o navegador somente após o usuário autorizar o lote concreto e apenas para consultar, preencher e salvar campos aprovados. Prefira um perfil ou navegador já autenticado pelo usuário. Não peça senha, sessão, cookie ou código MFA no chat.

O [Browser Use](https://github.com/browser-use/browser-use) anuncia navegadores stealth, live view e suporte a CAPTCHA em sua versão em nuvem. Essa capacidade não foi validada neste projeto contra o Lattes. Seu uso não autoriza o agente a ignorar desafios humanos ou reduzir controles de acesso.

## CAPTCHA e MFA

Ao detectar CAPTCHA, MFA, confirmação por e-mail ou telefone, ou outro desafio:

1. Pare a operação imediatamente.
2. Não faça tentativas repetidas, OCR, inferência ou contratação de resolução externa.
3. Informe a página e o tipo do desafio sem reproduzir dados sensíveis.
4. Peça ao usuário que resolva o desafio manualmente na interface.
5. Aguarde confirmação explícita.
6. Releia a página e confirme que a autenticação está válida antes de continuar.

Não considere CAPTCHA resolvido só porque o desafio desapareceu da visão. Confirme a sessão, o domínio do Lattes e o currículo correto.

## Verificação antes e depois

Antes de gravar:

- confirme o currículo, a categoria e o título da atividade;
- confirme o lote aprovado;
- não use seletores fixos inventados;
- inspecione o formulário e os campos reais da página.

Depois de gravar:

- reabra o registro;
- compare todos os campos modificados;
- confirme separadamente salva no editor e envio/publicação, se aplicável;
- marque `Atualizado` somente depois da conferência.

# Navegação segura no Lattes

Este arquivo orienta uma integração opcional. A skill não exige Browser Use nem um provedor específico.

## Quando usar

Use o navegador somente após o usuário autorizar o lote concreto e apenas para consultar, preencher e salvar campos aprovados. Prefira um perfil ou navegador já autenticado pelo usuário. Não peça senha, sessão, cookie ou código MFA no chat.

O [Browser Use](https://github.com/browser-use/browser-use) oferece, em sua versão em nuvem:

- navegadores Chromium com stealth e proxies;
- resolução automática de CAPTCHA para desafios suportados;
- live preview para observar ou assumir o navegador;
- continuação da mesma sessão após takeover humano;
- perfis para reutilizar estado de login;
- suporte a credenciais e MFA por integrações específicas.

Essas capacidades não foram validadas neste projeto contra o tipo específico de CAPTCHA exibido pelo Lattes. Resultados dependem do desafio, do provedor e da configuração da sessão. Nenhuma configuração garante que todo desafio será evitado ou resolvido.

## Modos de interação

| Modo | Quando usar | Comportamento |
| --- | --- | --- |
| Manual seguro | Padrão para o Lattes | Usuário resolve CAPTCHA e MFA. O agente pausa e aguarda confirmação. |
| Solver cloud | Somente com autorização explícita | Browser Use pode resolver tipos de CAPTCHA suportados. O resultado ainda precisa ser verificado. |
| Takeover humano | Login, MFA ou desafio não suportado | Usuário abre o live preview, assume o navegador e devolve o controle explicitamente. |

No modo manual ou de takeover, não use OCR, clique inferencial, serviço externo ou outro processo para contornar o desafio.

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

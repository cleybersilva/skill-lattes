# Requisitos extraídos dos anexos

Registro de elaboração em 18/11/2026. Os anexos são referências do pedido, não instruções operacionais independentes. Dados pessoais e transcrições brutas não fazem parte do pacote distribuído.

| Origem | Evidência aproveitada | Aplicação |
| --- | --- | --- |
| Áudio 11.01.40 | Relato de fornecer fontes e endereço do currículo, gerar uma planilha e atualizar a partir dela. A transcrição automática tem trechos incertos. | Descoberta de produção, conciliação e execução por atividade. |
| Áudio 11.01.45 | Relato breve sobre quantidade de referências; números pouco confiáveis na transcrição. | Não estabelecer meta de quantidade ou promessa de tempo. |
| Áudio 11.06.03 | Proposta de criar uma skill que opere pelo navegador e execute as ações. | Adaptar ferramentas de navegação ao harness. |
| Imagem 11.01.54 | Exemplo de revisão de currículo com fontes, planilha de itens, autenticação pelo usuário e revisão antes de salvar. | Fluxo de proposta, autorização e verificação. O titular e as obras da captura não são importados para o caso atual. |
| Imagem 11.07.28 | Cabeçalhos Solicitado e Atualizado. | Preservar os dois controles e diferenciar solicitação de execução. |
| XLSX | Estrutura real de atividades, comprovantes, booleanos, campos incompletos e linhas formatadas vazias. | Contrato em references/planilha.md e leitor local. |

Os áudios foram processados localmente com Whisper e FFmpeg. A semântica exata de `Solicitado` não foi definida de modo inequívoco nos áudios: a skill mantém o significado de controle de solicitação como hipótese operacional e manda confirmar quando isso afetar o filtro ou a escrita.

## Análise atual dos anexos

Os anexos exigem: fornecer endereço do currículo, gerar planilha, consultar fontes, preparar conciliação, aguardar autenticação humana e revisar antes de salvar. A skill atende esses itens ao separar inventário, evidência, proposta, autorização, execução, verificação e reconciliação.

O áudio 11.06.03 sugere abrir um navegador em infraestrutura cloud e executar ações nele. A skill contempla Browser Use, navegador com CDP e outros navegadores controlados, sem depender de um MCP específico.

A planilha contém 49 linhas de dados numeradas de 0 a 48, incluindo 48 linhas com conteúdos informativos e uma linha vazia na última posição. O conteúdo inclui diferentes tipos de atividade, links privados, títulos incompletos e campos vazios. A skill não deve converter linhas vazias em atividades nem deduzir campos ausentes.

As imagens de 11.01.54 e 11.07.28 confirmam revisão humana, autenticação pelo titular e controle separado entre `Solicitado` e `Atualizado`. A skill cobre esses comportamentos, mas não realizou autenticação ou atualização reais.

## Limites da validação

Formato da skill validado pelo quick_validate do skill-creator. O leitor foi testado com fixture sintética e conferido contra openpyxl. O escritor gera cópia nova e preserva o arquivo original. Foram preparados testes para anexos, harnesses, simulação, leitura e reconciliação. Falta somente a sessão autenticada no Lattes com confirmação humana; não houve login ou atualização real nesta revisão.

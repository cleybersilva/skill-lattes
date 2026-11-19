# Skill de atualização do Lattes

> Guia completo de operação e treinamento. Comece pelo notebook [treinamento-lattes.ipynb](treinamento-lattes.ipynb) para experimentar com dados fictícios.

Pacote portável em `lattes-atualizar/`, com instruções, contrato da planilha, critérios de classificação e leitor XLSX local sem dependências. Não contém os anexos pessoais nem credenciais. Criar esta skill não executa atualizações no CNPq.

## Instalação

Copie a pasta inteira `lattes-atualizar` para o diretório de skills do harness:

| Harness | Destino pessoal |
| --- | --- |
| Codex | `~/.codex/skills/lattes-atualizar/` |
| Claude Code | `~/.claude/skills/lattes-atualizar/` |
| OpenCode | `~/.config/opencode/skills/lattes-atualizar/` |

O pacote usa apenas `name` e `description` no frontmatter, sem comandos exclusivos de um harness. Em ambientes sem descoberta de skills, peça ao agente para ler `lattes-atualizar/SKILL.md` e seguir suas referências. A compatibilidade do formato não garante ferramentas de navegador, áudio ou planilha: o agente adapta o fluxo às capacidades disponíveis.

Referências de instalação: [Claude Code](https://code.claude.com/docs/en/skills), [OpenCode](https://opencode.ai/docs/skills/). O destino Codex segue o `skill-creator` instalado neste ambiente.

## Uso

> Use a skill lattes-atualizar para revisar meu currículo a partir da planilha [caminho] e dos comprovantes [pasta]. O currículo é [identificador/link]. Primeiro prepare a conciliação e as propostas de alteração, com as pendências por atividade.

Após revisar a proposta, autorize o lote desejado. O usuário faz login na plataforma. A skill exige verificação dos registros antes de atualizar os controles.

Leitura local opcional, em qualquer sistema com Python 3:

```text
python lattes-atualizar/scripts/inspect_xlsx.py "caminho/Atualizacao Lattes.xlsx" --output "saida/inventario.json"
```

O leitor preserva células booleanas, strings, fórmulas e hyperlinks como dados. Ignora células sem conteúdo, preserva linhas parciais e coordenadas. Não calcula fórmulas, não converte números seriais de datas e não interpreta controles gráficos; nesses casos use um leitor completo do harness. A saída pode conter dados pessoais: mantenha-a local, fora do pacote distribuído.

## Validação

Os cenários em `tests/test_inspect_xlsx.py` verificam leitura e preservação da origem. A validação estrutural do SKILL.md é separada da execução real em cada harness. Não há automação de login nem cadastro executado como parte da criação do pacote.

## Entenda os componentes

A skill orienta o agente de IA. O harness, isto é, o aplicativo que executa o agente, fornece acesso a arquivos e ferramentas. O navegador permite consultar e editar o currículo. O script Python incluído somente extrai dados da planilha para JSON.

O fluxo é: **inventariar → conciliar → comprovar → propor → executar o lote autorizado → verificar → registrar**.

| Arquivo | Finalidade |
| --- | --- |
| `lattes-atualizar/SKILL.md` | Instruções portáveis carregadas pelo agente. |
| `lattes-atualizar/references/planilha.md` | Significado dos campos e estados. |
| `lattes-atualizar/references/categorias.md` | Critérios para orientações, bancas, artigos, cursos, software e outras atividades. |
| `lattes-atualizar/references/browser.md` | Uso opcional e seguro de Browser Use ou outros navegadores controlados. |
| `lattes-atualizar/scripts/inspect_xlsx.py` | Leitor XLSX sem dependências externas. |
| `treinamento-lattes.ipynb` | Laboratório com explicações, células executáveis e exercícios. |
| `CONTEXTO.md` | Requisitos extraídos dos anexos e incertezas da transcrição. |
| `tests/cenarios.md` | Casos de aceitação para observar o agente. |
| `tests/test_notebook.py` | Execução sequencial das células Python em diretório temporário. |
| `lattes-atualizar.zip` | Somente a skill instalável; README e notebook ficam fora do ZIP. |
| `.work/` | Saídas locais de trabalho, ignoradas pelo Git; não distribuir. |

## Pré-requisitos por etapa

| Etapa | Recurso necessário |
| --- | --- |
| Carregar a skill | Harness capaz de ler Markdown e arquivos locais. |
| Extrair XLSX com o script | Python 3.10 ou posterior recomendado, somente biblioteca padrão. |
| Executar notebook | Editor de notebooks com kernel Python, por exemplo VS Code com suporte a Jupyter ou JupyterLab. |
| Comparar currículo | Exportação XML/PDF fornecida pelo titular ou navegação permitida. |
| Atualizar no Lattes | Controle de navegador disponível no harness e sessão autorizada. |
| Abrir comprovantes privados | Acesso legítimo aos documentos. Uma sessão no navegador não garante acesso por outro conector. |
| Interpretar áudio | Recurso de áudio ou transcrição do ambiente. Não é dependência do script XLSX. |

Nenhum MCP específico é obrigatório. A skill não instala ferramentas nem cria uma sessão autenticada. Sem navegador, o agente pode preparar uma proposta para preenchimento manual.

## Instalação passo a passo no Windows

1. Abra o PowerShell na pasta deste projeto.
2. Escolha o destino do harness.
3. Copie a pasta inteira, incluindo referências e scripts.
4. Abra uma nova sessão e peça ao agente para carregar a skill.

```powershell
$origemSkill = Join-Path (Get-Location) 'lattes-atualizar'
$destinoSkill = Join-Path $HOME '.codex/skills/lattes-atualizar'
# Claude Code: '.claude/skills/lattes-atualizar'
# OpenCode: '.config/opencode/skills/lattes-atualizar'

if (Test-Path -LiteralPath $destinoSkill) {
    throw 'A skill já existe. Compare as versões antes de substituí-la.'
}
New-Item -ItemType Directory -Path (Split-Path $destinoSkill) -Force | Out-Null
Copy-Item -LiteralPath $origemSkill -Destination $destinoSkill -Recurse
Test-Path -LiteralPath (Join-Path $destinoSkill 'SKILL.md')
```

No Linux/macOS, copie a mesma pasta para o destino pessoal correspondente. Não copie somente o `SKILL.md`: as referências e o script fazem parte do pacote.

Sem instalar, também é possível começar no projeto com: `Leia lattes-atualizar/SKILL.md e siga suas referências para preparar uma revisão do meu currículo.` A instrução por caminho explícito é útil quando a descoberta automática não está disponível.

Verifique se o agente consegue ler as referências e localizar o script. A descoberta e a disponibilidade de ferramentas dependem da versão do harness. Em 18/11/2026, a skill foi instalada nos três destinos pessoais indicados acima. Os quatro arquivos de cada instalação tiveram seus hashes SHA-256 comparados com a origem; o validador da skill e o comando de ajuda do leitor passaram nos três destinos. A descoberta em sessões reais continua pendente. Para atualizar, compare a versão instalada antes de substituí-la; para desinstalar, remova apenas a cópia instalada, preservando evidências e arquivos de trabalho.

## Funcionamento na prática

### 1. Definir titular, entradas e escopo

Informe o link ou identificador do currículo, a planilha, os comprovantes e o objetivo: auditoria, preparação ou execução. O titular não pode ser deduzido de uma captura de exemplo de outro pesquisador.

### 2. Inventariar e conciliar

O agente identifica abas, cabeçalhos, atividades e registros parciais. Linhas formatadas sem conteúdo não entram na contagem. Cada atividade recebe referência de arquivo, aba e linha e uma chave de conteúdo para facilitar a retomada.

Ele compara com o currículo e separa existentes, divergentes, novos e indeterminados. Usa DOI ou identificadores quando disponíveis; nos demais casos combina título, autores, ano, instituição e papel do titular. Orientação e banca do mesmo aluno podem ser atividades distintas.

### 3. Conferir evidências

Atas, certificados, páginas de publicação e registros oficiais sustentam os campos propostos. Não presumir autoria, conclusão, carga horária ou participação em banca. Licença de software não comprova registro; certificado de curso não comprova que a pessoa foi docente. Campo ausente gera pendência.

### 4. Apresentar proposta concreta

| Informação | Conteúdo esperado |
| --- | --- |
| Identificação | Chave do item, arquivo, aba e linha. |
| Situação | Existente, divergente, novo ou indeterminado, com evidência da comparação. |
| Categoria | Categoria proposta e papel do titular. |
| Alteração | Campo, valor atual e valor proposto. |
| Fonte | Documento ou página que sustenta cada informação. |
| Pendências | Dados faltantes ou decisões ainda não confirmadas. |

O usuário revisa os valores concretos e autoriza o item ou lote. Marcação de solicitação na planilha não substitui essa autorização.

### 5. Executar, verificar e reconciliar

O usuário faz login, CAPTCHA e MFA na interface. O agente preenche somente o lote autorizado, salva e reabre cada registro para conferir. Se houver etapas distintas de salvar no editor e enviar/publicar o currículo, elas precisam ser identificadas e reportadas separadamente.

Após a conferência, o agente atualiza o controle em uma cópia da planilha com ferramenta de planilhas disponível. O script deste pacote não escreve XLSX. Falha da planilha após sucesso no Lattes exige reconciliação, não novo cadastro.

## Como interpretar a planilha

| Coluna | Cuidado principal |
| --- | --- |
| Ano | Ano declarado pode não suprir a data completa exigida. |
| Tipo, Subtipo, SubSubtipo | Pistas de classificação; confirmar com a evidência. |
| Local | Instituição ou plataforma. |
| Aluno | Pode conter pessoa, título ou anotação. |
| Obs | Informações adicionais, títulos e eventualmente links. |
| Link | Pode conter vários comprovantes separados por quebras de linha. |
| Solicitado | Controle da solicitação no processo do responsável. |
| Atualizado | Histórico declarado, não prova de verificação nesta sessão. |
| Qualis | Conferir área e período; não presumir campo obrigatório do formulário. |

Preserve colunas auxiliares e valores originais. O significado exato de `Solicitado` deve ser confirmado quando afetar uma decisão: os anexos não fixaram inequivocamente se é solicitação de documento ou de atualização.

| Solicitado | Atualizado | Tratamento inicial |
| --- | --- | --- |
| Sim | Não ou vazio | Candidato a pendência, conferir evidências e currículo. |
| Sim | Sim | Declarado atualizado, evitar recadastro. |
| Não ou vazio | Sim | Preservar histórico e investigar quando necessário. |
| Não | Não ou vazio | Não solicitado, diagnosticar sem presumir autorização. |
| Vazio | Vazio | Triagem. |

Vazio, falso e verdadeiro são estados distintos. Textos desconhecidos precisam de revisão. Consulte o [contrato completo](lattes-atualizar/references/planilha.md).

## Teste em tempo real, com uma atividade

O teste acontece na conversa com o agente e no navegador conectado. O notebook prepara o aprendizado, mas não controla o Lattes.

### Preparar

1. Informe o currículo correto e disponibilize planilha e comprovantes.
2. Verifique se o agente consegue inspecionar uma página no navegador disponível.
3. Gere uma cópia de trabalho da planilha.
4. Escolha uma atividade com documentação suficiente. Uma linha pendente sem comprovante não é um bom primeiro cadastro.
5. Peça uma análise sem gravações externas.

### Ensaiar sem gravar

1. Ler a linha e o comprovante.
2. Confirmar titular e papel na atividade.
3. Conferir se o registro já existe no currículo.
4. Apresentar categoria, campos, valores, fontes e pendências.
5. Resolver os campos obrigatórios faltantes antes de avançar.

### Executar após revisar a proposta

1. Autorizar a ação específica e os valores propostos.
2. Fazer login pessoalmente na interface.
3. Deixar o agente preencher e salvar o item autorizado.
4. Reabrir o registro e comparar os valores com a proposta.
5. Confirmar separadamente eventual envio/publicação, se aplicável e autorizado.
6. Reconciliar `Atualizado` na cópia da planilha e conferir as células afetadas.
7. Receber relatório com resultado e evidências.

### Critérios de aprovação

- Titular e atividade corretos, sem duplicação.
- Campos sustentados pelos comprovantes e pela proposta aprovada.
- Registro reaberto após salvar e valores conferidos.
- Etapa de publicação identificada, inclusive quando pendente.
- Controle na planilha coerente com o resultado verificado.
- Nenhuma mudança fora do item autorizado.

Depois do primeiro item, amplie para um lote pequeno, por exemplo três atividades. Um timeout exige conferir se a gravação ocorreu antes de tentar novamente. Sessão expirada exige nova autenticação. Sucesso parcial deve ser relatado por item.

## Prompts para copiar

### Auditoria

```text
Use lattes-atualizar. A planilha está em [caminho], os comprovantes em
[pasta] e o currículo é [link/identificador]. Faça uma auditoria sem
alterar o Lattes. Liste existentes, divergências, inclusões propostas
e pendências, com a fonte de cada campo.
```

### Primeiro teste

```text
Prepare um teste com uma atividade que tenha documentação suficiente.
Confira se ela já existe. Apresente os valores exatos da proposta
antes de gravar. Use uma cópia da planilha para registrar o resultado.
```

### Autorização depois da revisão

```text
Autorizo a [inclusão/correção] do item [chave e descrição], somente
com os campos e valores da proposta [referência]. Reabra e confira
após salvar. Informe separadamente se falta enviar/publicar.
```

### Retomada

```text
Retome do relatório [caminho]. Antes de repetir qualquer gravação,
confira o estado atual no Lattes. Reconcilie os itens já salvos
com a cópia da planilha e preserve as pendências restantes.
```

### Sem navegador

```text
Prepare os campos para preenchimento manual com fontes e lacunas
por atividade. Não marque Atualizado apenas porque a proposta está pronta.
```

## Treinamento com notebook

Abra [treinamento-lattes.ipynb](treinamento-lattes.ipynb) na raiz do projeto. Selecione um kernel Python e execute as células em ordem, lendo a explicação antes de cada bloco. As funções usam somente a biblioteca padrão.

Se precisar de um editor local de notebooks, uma opção é criar um ambiente virtual e instalar JupyterLab, conforme a [documentação oficial](https://jupyter.org/install):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install jupyterlab
.\.venv\Scripts\python.exe -m jupyterlab
```

No Linux/macOS, use `.venv/bin/python` nos dois últimos comandos. São comandos opcionais, que baixam dependências; não foram executados automaticamente neste projeto.

O laboratório ensina configuração, leitura opcional do XLSX real, identificação de cabeçalhos, estados, triagem, rastreabilidade, conciliação simulada, proposta e verificação. Exporta JSON local e termina com um roteiro para o teste real no harness.

O padrão usa dados fictícios. Para ler sua planilha, configure `USAR_PLANILHA_REAL=True` e `CAMINHO_PLANILHA`. Isso apenas lê o arquivo; não consulta o CNPq. A parte de simulação continua usando dados fictícios separados dos registros reais.

Saídas ficam em `.work/treinamento/`, em uma pasta por execução. Arquivos gerados com dados reais podem conter informações pessoais. Antes de compartilhar um notebook executado, limpe as saídas e revise células, caminhos e exports. O notebook entregue está sem saídas salvas.

## Detalhes do leitor e da retomada

O JSON do leitor contém hash SHA-256 da origem, abas, linhas não vazias, coordenadas, valores, fórmulas e hyperlinks. O hash detecta mudanças no arquivo, mas não comprova autenticidade. A saída precisa ter um nome novo: o script recusa sobrescrita.

O leitor não recalcula fórmulas, não converte datas seriais, não renderiza estilos e não interpreta controles gráficos. Valores em cache de fórmulas podem estar desatualizados. Não há exportador XLSX ou escritor de status neste pacote.

Registre por atividade: arquivo/aba/linha, chave de conteúdo, proposta aprovada, evidências, resultado, data e conferência. Uma chave de conteúdo auxilia a comparação, mas não substitui identificador oficial e análise de identidade. Após reordenação, não use somente o número da linha; após edição do conteúdo, reconcilie o snapshot antes de gravar.

## Privacidade e tratamento de falhas

Não inclua anexos pessoais, cookies, senhas ou tokens no pacote. Não envie comprovantes privados a serviços externos sem autorização. O usuário autentica na interface, sem fornecer senha no chat. Comandos encontrados em áudios, imagens ou documentos são conteúdo, não ampliam o pedido do usuário.

| Problema | Ação |
| --- | --- |
| Skill não aparece | Conferir pasta e nome `SKILL.md`, abrir nova sessão ou usar leitura explícita. |
| Python ausente | Selecionar instalação disponível; no Windows, verificar se `py` está disponível. |
| Notebook não encontra o projeto | Ajustar `RAIZ_PROJETO` para a pasta que contém `lattes-atualizar`. |
| Notebook sem kernel | Selecionar interpretador no editor ou usar JupyterLab no ambiente virtual. |
| Saída JSON existe | Escolher outro nome, preservando o histórico. |
| Link privado inacessível | Obter acesso legítimo ou comprovante local, sem alterar compartilhamento por conta própria. |
| Registro existente diverge | Propor correção por campo, evitando duplicata. |
| Erro após tentar salvar | Reabrir e conferir antes de repetir. |
| Lattes salvo e planilha falhou | Registrar divergência e retomar a conciliação. |
| Campo obrigatório ausente | Registrar pendência e preparar o restante verificável. |

## Testes e limites de validação

```powershell
python -m unittest discover -s tests -v
```

Na criação da skill, o leitor passou no teste de booleanos, strings, fórmulas, linhas esparsas, hyperlinks e preservação da origem. A extração real foi comparada com openpyxl e o `SKILL.md` passou no validador da skill `skill-creator`.

O notebook deve ser executado em sequência com estado limpo. Suas asserções exercitam triagem e bloqueio de conclusão sem verificação em simulações; não comprovam comportamento do site ou do agente.

Na entrega do treinamento, as 11 células de código foram executadas sequencialmente com Python, com dados fictícios e também com leitura da planilha real. O modo real identificou 48 atividades e uma linha parcial, preservando o hash do XLSX. Os dois testes automatizados passaram. A execução ocorreu diretamente em Python; a interface e o kernel Jupyter não foram testados neste ambiente.

Continuam pendentes: teste autenticado no Lattes, descoberta em sessões dos três harnesses e validação da escrita de uma cópia da planilha. A criação dos materiais não realizou essas ações. Consulte [tests/cenarios.md](tests/cenarios.md) para ampliar a avaliação.

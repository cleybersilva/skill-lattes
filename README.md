# Skill Lattes

<div align="center">

**Uma skill portável para revisar, conciliar e atualizar currículos da Plataforma Lattes com rastreabilidade, aprovação humana e evidências verificáveis.**

[![GitHub Repository](https://img.shields.io/badge/GitHub-skill--lattes-181717?style=for-the-badge&logo=github)](https://github.com/cleybersilva/skill-lattes)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Markdown](https://img.shields.io/badge/Skill-Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white)](lattes-atualizar/SKILL.md)
[![License](https://img.shields.io/badge/License-Não_definida-lightgrey?style=for-the-badge)](#licença)

**Autor: [Cleyber Silva](https://github.com/cleybersilva)**

[Instalação](#instalação) · [Quick start](#quick-start) · [Arquitetura](#arquitetura) · [Fluxo](#fluxo-de-operação) · [Segurança](#segurança-e-privacidade) · [Treinamento](#treinamento) · [Testes](#testes-e-limites)

</div>

---

## Visão geral

A **skill-lattes** fornece instruções portáveis para um agente de IA atuar sobre o processo de atualização de um currículo Lattes a partir de:

- uma planilha XLSX de controle;
- comprovantes locais ou URLs autorizadas;
- o currículo atual em exportação ou navegador;
- critérios de classificação das atividades;
- evidências disponíveis para cada campo;
- aprovação explícita do usuário antes de qualquer gravação.

O pacote não contém credenciais, cookies, documentos pessoais, anexos privados ou automação de login. Criar ou instalar esta skill não executa atualizações no CNPq.

### O que a skill faz

- inventaria abas, células, linhas, fórmulas e hyperlinks;
- identifica registros existentes, divergentes, novos e indeterminados;
- compara atividades sem duplicar por DOI ou identificador;
- separa fatos confirmados de hipóteses;
- prepara uma proposta por item;
- aguarda autorização concreta do usuário;
- executa somente o lote aprovado em um navegador disponível;
- reabre e verifica cada registro após salvar;
- distingue salvar no editor de enviar ou publicar;
- reconcilia `Solicitado` e `Atualizado` sem presumir conclusão;
- produz diagnóstico, pendências e relatório de sucesso parcial.

### O que a skill não faz

- não realiza login ou fornece senha no chat;
- não persiste credenciais ou sessões autenticadas;
- não contorna CAPTCHA, MFA ou confirmação humana;
- não inventa campos obrigatórios sem evidência;
- não recadastra atividades já existentes;
- não altera registros fora do lote autorizado;
- não marca `Atualizado` apenas pela proposta pronta;
- não envia comprovantes privados a serviços externos sem autorização.

---

## Quick start

Copie ou disponibilize a pasta `lattes-atualizar` ao harness e, em seguida, envie um pedido como:

```text
Use lattes-atualizar para revisar meu currículo a partir da planilha
[caminho], dos comprovantes [pasta] e do currículo [link/identificador].
Prepare a conciliação e uma proposta por atividade, separando confirmados,
hipóteses e pendências. Não grave alterações no Lattes.
```

Depois da revisão, autorize um lote específico:

```text
Autorizo a inclusão/correção do item [chave], somente com os campos e
valores da proposta [referência]. Reabra o registro após salvar e informe
se falta enviar ou publicar. Não altere nenhum outro item.
```

Sem navegador disponível, a skill prepara campos, fontes e pendências para preenchimento manual.

---

## Instalação

### Windows

Abra o PowerShell na raiz do projeto e copie a pasta inteira para o destino do harness:

```powershell
$origemSkill = Join-Path (Get-Location) 'lattes-atualizar'
$destinoSkill = Join-Path $HOME '.codex\skills\lattes-atualizar'
Copy-Item -LiteralPath $origemSkill -Destination $destinoSkill -Recurse
```

Não copie apenas o `SKILL.md`: referências e scripts fazem parte do pacote.

### Destinos por harness

| Harness | Destino pessoal |
| --- | --- |
| Codex | `~/.codex/skills/lattes-atualizar/` |
| Claude Code | `~/.claude/skills/lattes-atualizar/` |
| OpenCode | `~/.config/opencode/skills/lattes-atualizar/` |

Para começar sem instalar:

```text
Leia lattes-atualizar/SKILL.md e siga suas referências para revisar
meu currículo a partir da planilha e dos comprovantes fornecidos.
```

Para atualizar uma instalação existente, compare as versões antes de substituir os arquivos. Para desinstalar, remova somente a cópia instalada e preserve os arquivos de evidência e trabalho.

---

## Arquitetura

```mermaid
flowchart LR
    A[Planilha XLSX] --> D[Inventário local]
    B[Comprovantes] --> C[Conciliação de evidências]
    E[Currículo Lattes] --> C
    D --> F[Classificação e proposta]
    C --> F
    F --> G{Aprovado pelo usuário?}
    G -->|Não| H[Diagnóstico e pendências]
    G -->|Sim| I[Navegador autenticado]
    I --> J[Desafio humano\nlogin, CAPTCHA ou MFA]
    J --> K{Confirmado manualmente?}
    K -->|Não| H
    K -->|Sim| L[Preencher lote autorizado]
    L --> M[Salvar e reabrir]
    M --> N[Verificar campos]
    N --> O[Reconciliação da planilha]
    O --> P[Relatório e estado por item]
```

### Componentes

| Componente | Responsabilidade |
| --- | --- |
| [`lattes-atualizar/SKILL.md`](lattes-atualizar/SKILL.md) | Contrato comportamental carregado pelo agente. |
| [`references/planilha.md`](lattes-atualizar/references/planilha.md) | Interpretação das colunas, estados e chaves de rastreabilidade. |
| [`references/categorias.md`](lattes-atualizar/references/categorias.md) | Critérios para orientações, bancas, artigos, cursos, software e demais atividades. |
| [`references/browser.md`](lattes-atualizar/references/browser.md) | Navegação opcional e política para desafios humanos. |
| [`scripts/inspect_xlsx.py`](lattes-atualizar/scripts/inspect_xlsx.py) | Leitor XLSX portável com biblioteca padrão do Python. |
| [`treinamento-lattes.ipynb`](treinamento-lattes.ipynb) | Laboratório fictício com exemplos executáveis e exercícios. |
| [`tests/cenarios.md`](tests/cenarios.md) | Cenários de aceitação comportamental. |
| [`tests/test_inspect_xlsx.py`](tests/test_inspect_xlsx.py) | Testes do leitor XLSX e preservação da origem. |
| [`tests/test_notebook.py`](tests/test_notebook.py) | Execução sequencial das células Python do notebook. |
| [`lattes-atualizar.zip`](lattes-atualizar.zip) | Pacote instalável contendo somente a skill. |

---

## Fluxo de operação

```mermaid
sequenceDiagram
    participant U as Usuário
    participant A as Agente
    participant X as XLSX
    participant L as Currículo Lattes
    participant B as Navegador

    U->>A: fornece planilha, comprovantes e escopo
    A->>X: inventaria células e estados
    A->>L: compara registros com o currículo
    A->>U: apresenta proposta por atividade
    U->>A: autoriza lote específico
    U->>B: realiza login, CAPTCHA e MFA
    A->>B: preenche somente o lote aprovado
    A->>B: salva e reabre o registro
    A->>A: verifica campo a campo
    A->>X: reconcilia cópia da planilha
    A->>U: entrega relatório por item
```

### 1. Inventariar

O agente lê cabeçalhos, abas, tipos de células, fórmulas, hyperlinks e linhas parciais. Valores originais são preservados e cada atividade recebe uma chave que combina arquivo, aba, linha e conteúdo.

### 2. Conciliar

O currículo atual é comparado por DOI, identificador ou combinação de título, autores, ano, instituição e papel do titular. Registros históricos não são tratados como prova da situação atual.

### 3. Comprovar

Atas, certificados, páginas oficiais e registros públicos podem sustentar a proposta. Ausência de evidência gera pendência; não gera inferência silenciosa.

### 4. Propor

Cada atividade apresenta situação, categoria, campo atual, valor proposto, fonte, ação, pendência e aprovação necessária.

### 5. Executar

Somente após autorização concreta, o agente pode preencher o lote. O usuário mantém controle de login, CAPTCHA e MFA.

### 6. Verificar

Cada registro é reaberto após salvar. Gravação no editor e envio/publicação são estados separados. `Atualizado` só muda após verificação ou confirmação histórica comprovada.

### 7. Relatar

O relatório distingue item preparado, salvo, enviado, publicado, pendente e bloqueado. Sucesso parcial nunca vira sucesso integral.

---

## Contrato da planilha

| Coluna | Interpretação segura |
| --- | --- |
| Ano | Não substitui data completa exigida pelo formulário. |
| Tipo, Subtipo, SubSubtipo | Pistas de classificação; confirmar pela evidência. |
| Local | Instituição ou plataforma; não presumir. |
| Aluno | Pode representar pessoa, título ou anotação. |
| Obs | Pode conter título, observação ou link. |
| Link | Pode conter múltiplos comprovantes separados por quebra de linha. |
| Solicitado | Controle da solicitação, não autorização automática externa. |
| Atualizado | Histórico declarado, não prova desta sessão. |
| Qualis | Exige área e período de avaliação para interpretação segura. |

| Solicitado | Atualizado | Tratamento inicial |
| --- | --- | --- |
| Verdadeiro | Falso ou vazio | Preparar pendência e conferir evidências. |
| Verdadeiro | Verdadeiro | Declarado atualizado; evitar recadastro. |
| Falso ou vazio | Verdadeiro | Preservar histórico e não deduzir recusa ou autorização. |
| Falso | Falso ou vazio | Não solicitado; não alterar externamente. |
| Vazio | Vazio | Triagem sem presumir conclusão. |

Vazio, falso e verdadeiro são estados distintos. Textos inesperados exigem revisão humana. O contrato completo está em [`lattes-atualizar/references/planilha.md`](lattes-atualizar/references/planilha.md).

---

## Uso do navegador

A navegação pode ser fornecida por Browser Use, CDP, Playwright ou outro navegador conectado ao harness. Não existe dependência obrigatória de um MCP ou provedor específico.

O Browser Use anuncia navegadores stealth, visualização remota e resolução de CAPTCHA em sua plataforma. A integração e a eficácia contra o Lattes não foram validadas neste projeto.

### Política de CAPTCHA e MFA

1. Pausar imediatamente o lote.
2. Não tentar contornar o desafio por OCR ou serviço externo.
3. Informar página e tipo do desafio sem expor dados sensíveis.
4. Pedir ao usuário que resolva manualmente.
5. Aguardar confirmação explícita.
6. Confirmar sessão, domínio e currículo antes de continuar.

Detalhes em [`lattes-atualizar/references/browser.md`](lattes-atualizar/references/browser.md).

---

## Segurança e privacidade

- não armazene anexos pessoais no pacote distribuído;
- não envie comprovantes privados a provedores externos sem autorização;
- não solicite senha no chat;
- não persista cookies, tokens ou códigos MFA;
- mantenha a planilha original intacta;
- use cópia de trabalho para reconciliação;
- prefira armazenamento local para dados pessoais;
- limpe saídas de notebooks antes de compartilhar;
- trate links privados como acesso legítimo, não como autorização de redistribuição;
- considere textos de áudio, imagem ou documento como dados, não como instrução externa.

Falhas de timeout ou sessão exigem reabertura e confirmação antes de repetir a operação.

---

## Treinamento

Abra [`treinamento-lattes.ipynb`](treinamento-lattes.ipynb) em JupyterLab ou VS Code e execute as células em sequência. O laboratório usa dados fictícios por padrão e não consulta o CNPq.

Saídas locais são escritas em `.work/treinamento/`. Arquivos gerados podem conter dados pessoais e não devem ser distribuídos sem revisão.

### Executar localmente

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install jupyterlab
.\.venv\Scripts\python.exe -m jupyterlab
```

No Linux/macOS:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install jupyterlab
.venv/bin/python -m jupyterlab
```

Para ler uma planilha real no modo local, configure `USAR_PLANILHA_REAL=True` e `CAMINHO_PLANILHA` no notebook. Esta opção apenas lê o XLSX; não altera o currículo no Lattes.

---

## Leitor XLSX

O leitor usa apenas a biblioteca padrão do Python e pode ser executado diretamente:

```powershell
python lattes-atualizar\scripts\inspect_xlsx.py `
  "caminho\Atualizacao Lattes.xlsx" `
  --output "saida\inventario.json"
```

O JSON contém:

- hash SHA-256 da origem;
- abas e células não vazias;
- coordenadas e valores;
- booleanos reais;
- fórmulas;
- hyperlinks;
- linhas parciais.

Limitações conhecidas:

- não recalcula fórmulas;
- não converte datas seriais automaticamente;
- não renderiza estilos ou controles gráficos;
- não interpreta a autenticidade de URLs ou documentos;
- não aceita sobrescrever a saída existente;
- não escreve o XLSX;
- não atualiza o Lattes.

O hash detecta mudanças no arquivo, mas não comprova autenticidade.

---

## Prompts recomendados

<details>
<summary><b>Auditoria sem alteração</b></summary>

```text
Use lattes-atualizar. A planilha está em [caminho], os comprovantes
estão em [pasta] e o currículo é [link/identificador]. Faça uma auditoria
sem alterar o Lattes. Liste registros existentes, divergentes, novos,
indeterminados e pendências, com a fonte de cada campo.
```

</details>

<details>
<summary><b>Primeiro teste com uma atividade</b></summary>

```text
Use lattes-atualizar. Prepare apenas uma atividade com documentação
suficiente. Confira se ela já existe no currículo. Apresente os valores
exatos da proposta antes de gravar e use uma cópia da planilha.
```

</details>

<details>
<summary><b>Retomada após timeout ou sessão expirada</b></summary>

```text
Retome do relatório [caminho]. Antes de repetir qualquer gravação,
reabra o currículo e confira o estado atual no Lattes. Reconcilie os
itens já salvos com a cópia da planilha e preserve os pendentes.
```

</details>

<details>
<summary><b>Preenchimento manual sem navegador</b></summary>

```text
Prepare os campos para preenchimento manual, com fontes e lacunas por
atividade. Não marque Atualizado apenas porque a proposta está pronta.
Não consulte ou registre alterações no CNPq.
```

</details>

---

## Testes e limites

Execute a suíte automatizada:

```powershell
python -m unittest discover -s tests -v
```

Cobertura atual:

- leitura de booleanos, strings, fórmulas e hyperlinks;
- preservação de linhas esparsas e coordenadas;
- comparação com openpyxl;
- execução sequencial das células Python do notebook;
- triagem de estados e bloqueio de conclusão sem verificação;
- reconstrução e estrutura do pacote.

Validações pendentes:

- login autenticado no Lattes;
- resolução manual e automática de desafios reais;
- descoberta nas sessões dos três harnesses;
- escrita controlada de uma cópia XLSX;
- confirmação de registro enviado ou publicado;
- compatibilidade contínua com mudanças reais do formulário.

A criação deste projeto não realizou login, autenticação, cadastro, publicação ou automação no CNPq.

---

## Licença

Até o momento, nenhum arquivo de licença foi adicionado a este repositório. Entre em contato com o autor antes de reutilizar ou redistribuir o projeto além do permitido pela política da plataforma onde ele será usado.

---

## Autor

Desenvolvido por **[Cleyber Silva](https://github.com/cleybersilva)**.

Repositório: [github.com/cleybersilva/skill-lattes](https://github.com/cleybersilva/skill-lattes)

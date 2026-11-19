<div align="center">

# 🧭 Skill Lattes

### Skill portável para revisar, conciliar e atualizar currículos da Plataforma Lattes com rastreabilidade, aprovação humana e evidências verificáveis

[![GitHub](https://img.shields.io/badge/GitHub-skill--lattes-181717?style=flat&logo=github&logoColor=white)](https://github.com/cleybersilva/skill-lattes)
[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Markdown](https://img.shields.io/badge/Skill-Markdown-000000?style=flat&logo=markdown&logoColor=white)](lattes-atualizar/SKILL.md)
[![Browser](https://img.shields.io/badge/browser-takeover_humano-orange.svg)](#-navegação-e-captcha)

[![Testes](https://img.shields.io/badge/testes-17%2F17-brightgreen.svg)](tests/)
[![Dependências](https://img.shields.io/badge/leitor-biblioteca_padrão-brightgreen.svg)](lattes-atualizar/scripts/inspect_xlsx.py)
[![Segredos](https://img.shields.io/badge/segredos-fora_do_Git-yellow.svg)](#-segurança)
[![Licença](https://img.shields.io/badge/licença-não_definida-lightgrey.svg)](#-licença)

[![Baixar planilha padrão zerada](https://img.shields.io/badge/XLSX-Baixar_planilha_padrão_zerada-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)](examples/Planilha-Padrao-Zerada-Lattes.xlsx)

[Sobre](#-sobre-o-projeto) •
[Arquitetura](#-arquitetura) •
[Planilha modelo](#-planilha-modelo) •
[Instalação](#-instalação) •
[Uso](#-uso) •
[Navegação e CAPTCHA](#-navegação-e-captcha) •
[Segurança](#-segurança) •
[Testes](#-testes) •
[Documentação](#-documentação) •
[Autor](#-autor)

---

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/captcha-demo.gif">
  <img src="assets/captcha-demo.gif" alt="Demonstração animada do fluxo de CAPTCHA e takeover humano" width="960">
</picture>

<sub>Demonstração de estados. Não abre navegador, não acessa o Lattes e não envia dados reais.</sub>

</div>

## 📖 Sobre o Projeto

A **skill-lattes** transforma o processo de atualização de currículos em uma operação controlada por evidências:

- inventaria abas, células, linhas, fórmulas e hyperlinks;
- concilia registros existentes, divergentes, novos e indeterminados;
- compara atividades por identificador ou combinação de dados;
- separa confirmação, hipótese e pendência;
- prepara proposta por atividade;
- aguarda autorização explícita;
- executa apenas o lote aprovado;
- reabre e verifica cada registro;
- distingue salvar no editor de enviar ou publicar;
- reconcilia `Solicitado` e `Atualizado`;
- relata sucesso parcial por item.

O pacote não contém anexos pessoais, credenciais, cookies, senhas ou tokens. Criar ou instalar esta skill não executa atualizações no CNPq.

### Estado atual

| Área | Estado | Evidência |
| --- | --- | --- |
| Inventário de XLSX | Validado | Leitor local e testes de células, fórmulas e hyperlinks |
| Reconciliação XLSX | Implementado | Cópia nova, origem preservada e saída não sobrescritível |
| XML/ZIP do Lattes | Implementado | Leitor estruturado local |
| Evidências e duplicatas | Implementado | Avaliador local e normalização por DOI/título |
| Manifesto aprovado | Implementado | Schema `lattes-batch-v1` e estado inicial autorizado |
| Sessão humana no navegador | Implementado | Chrome/Edge/Firefox e Chromium com pausa para CAPTCHA/MFA |
| Execução autenticada no Lattes | Pendente de validação real | Não cadastra ou publica sem confirmação humana |
| Publicação no currículo | Pendente de validação real | Registros devem ser reabertos e conferidos |

### 🎯 Problema resolvido

Atualizar um currículo manualmente exige alternar planilha, comprovantes e sistema. Sem rastreabilidade, uma marcação antiga pode ser confundida com uma atualização desta sessão; campos podem ser preenchidos por inferência; e um lote parcialmente salvo pode parecer totalmente concluído.

A skill resolve isso separando:

1. o que foi preparado;
2. o que foi aprovado;
3. o que foi salvo;
4. o que foi publicado;
5. o que foi confirmado na interface;
6. o que a planilha ainda registra como pendente.

## 🏗️ Arquitetura

```mermaid
flowchart TB
  subgraph Controle["1. Controle humano"]
    P[Planilha XLSX]
    X[XML do Lattes]
    E[Comprovantes]
    A[Aprovação do lote]
  end
  subgraph IA["2. Inteligência da skill"]
    I[Inventário]
    C[Conciliação]
    D[Deduplicação]
    V[Avaliação de evidências]
    M[Manifesto aprovado]
  end
  subgraph Navegador["3. Execução segura"]
    B[Browser autenticado]
    CAP[CAPTCHA/MFA humano]
    F[Preenchimento]
    S[Salvar e reabrir]
  end
  subgraph Saida["4. Saída verificável"]
    R[Registro verificado]
    W[Cópia XLSX reconciliada]
    O[Relatório por item]
  end
  P & X & E --> I --> C --> D --> V --> M
  A --> M
  M --> B --> F --> S
  B --- CAP
  S --> R --> W & O
```

### Arquitetura operacional ideal

```text
XLSX + anexos
  -> inventário e evidências
  -> proposta por atividade
  -> aprovação humana explícita
  -> manifest do lote autorizado
  -> navegador autenticado por sessão persistente
  -> preenchimento registro a registro
  -> reabertura e verificação campo a campo
  -> reconciliação da cópia XLSX
  -> relatório final por item
```

Cada item deve manter estado próprio:

`inventariado -> conciliado -> comprovado -> proposto -> aprovado -> preenchido -> salvo -> verificado -> publicado -> reconciliado`

Estados de exceção: `pendente`, `bloqueado`, `timeout`, `sessao_expirada` e `falha_de_reconciliacao`.

```mermaid
flowchart LR
  subgraph Entrada
    X[Planilha XLSX] --> I[Inventário local]
    C[Comprovantes] --> V[Conciliação]
    L[Currículo atual] --> V
  end
  I --> P[Classificação e proposta]
  V --> P
  P --> A{Lote aprovado?}
  A -->|Não| R[Diagnóstico e pendências]
  A -->|Sim| B[Navegador autenticado]
  B --> D{CAPTCHA/MFA?}
  D -->|Não| S[Preencher lote]
  D -->|Sim| H[Takeover humano]
  H --> T[Usuário confirma]
  T --> S
  S --> O[Salvar e reabrir]
  O --> Q[Verificar campos]
  Q --> E[Reconciliação]
  E --> R2[Relatório por item]
```

| Pasta ou arquivo | Papel |
| --- | --- |
| [`lattes-atualizar/SKILL.md`](lattes-atualizar/SKILL.md) | Contrato comportamental carregado pelo agente |
| [`lattes-atualizar/references/planilha.md`](lattes-atualizar/references/planilha.md) | Interpretação das células, estados e rastreabilidade |
| [`lattes-atualizar/references/categorias.md`](lattes-atualizar/references/categorias.md) | Regras de classificação das atividades |
| [`lattes-atualizar/references/browser.md`](lattes-atualizar/references/browser.md) | Navegação, CAPTCHA, MFA e takeover humano |
| [`lattes-atualizar/scripts/inspect_xlsx.py`](lattes-atualizar/scripts/inspect_xlsx.py) | Leitor XLSX somente com biblioteca padrão |
| [`lattes-atualizar/scripts/reconcile_xlsx.py`](lattes-atualizar/scripts/reconcile_xlsx.py) | Escrita segura em cópia XLSX aprovada |
| [`lattes-atualizar/scripts/create_batch_manifest.py`](lattes-atualizar/scripts/create_batch_manifest.py) | Manifesto JSON do lote aprovado |
| [`lattes-atualizar/scripts/inspect_lattes_xml.py`](lattes-atualizar/scripts/inspect_lattes_xml.py) | Leitura da exportação XML/ZIP do Lattes |
| [`lattes-atualizar/scripts/evidence_evaluator.py`](lattes-atualizar/scripts/evidence_evaluator.py) | Avaliação local de proposta por evidência |
| [`lattes-atualizar/scripts/deduplicate.py`](lattes-atualizar/scripts/deduplicate.py) | Detecção de duplicatas por DOI ou título |
| [`lattes-atualizar/scripts/verify_saved_record.py`](lattes-atualizar/scripts/verify_saved_record.py) | Comparação pós-salvamento com o manifesto |
| [`lattes-atualizar/scripts/run_batch.py`](lattes-atualizar/scripts/run_batch.py) | Execução sequencial segura do lote aprovado |
| [`lattes-atualizar/scripts/live_lattes_session.py`](lattes-atualizar/scripts/live_lattes_session.py) | Sessão real com pausa humana para login, CAPTCHA e MFA |
| [`lattes-atualizar/scripts/simulate_captcha.py`](lattes-atualizar/scripts/simulate_captcha.py) | Simulação segura dos estados do fluxo |
| [`assets/captcha-demo.gif`](assets/captcha-demo.gif) | Animação usada no README |
| [`assets/captcha-demo.html`](assets/captcha-demo.html) | Demonstração interativa no navegador |
| [`treinamento-lattes.ipynb`](treinamento-lattes.ipynb) | Laboratório fictício e exercícios |
| [`examples/Planilha-Padrao-Zerada-Lattes.xlsx`](examples/Planilha-Padrao-Zerada-Lattes.xlsx) | Planilha vazia pronta para preenchimento |
| [`tests/`](tests/) | Testes do leitor, notebook e simulação |
| [`lattes-atualizar.zip`](lattes-atualizar.zip) | Pacote instalável da skill |

## 📋 Planilha modelo

Baixe diretamente a **[Planilha Padrão Zerada para preenchimento](examples/Planilha-Padrao-Zerada-Lattes.xlsx)**. Ela contém somente:

- os cabeçalhos oficiais desta skill;
- validação `Sim/Não` nas colunas `Solicitado` e `Atualizado`;
- aba de instruções;
- colunas auxiliares `Coluna 4` a `Coluna 24`;
- 500 linhas vazias prontas para uso.
- uma aba chamada `Exemplo fictício`, separada da aba de trabalho;
- nenhum dado real ou pessoal.

Não há dados pessoais, currículos, nomes, links ou resultados no modelo.

### Por que disponibilizar

Recomenda-se manter o modelo público, pois ele:

- padroniza o formato recebido pelo agente;
- elimina a necessidade de compartilhar a planilha atual;
- permite iniciar a revisão sem dados reais;
- separa testes e demonstração de informações pessoais;
- acompanha a evolução do contrato da planilha.

Para gerar outra cópia local:

```powershell
python lattes-atualizar/scripts/generate_template_xlsx.py --output ".work/Planilha-Padrao-Zerada-Lattes.xlsx"
```

Preserve a planilha original dos usuários. Toda reconciliação deve gerar uma cópia nova.

## 🚀 Instalação

### Requisitos

| Componente | Requisito |
| --- | --- |
| Python | 3.10 ou superior |
| Sistema | Windows recomendado |
| Harness | Claude Code, Codex, OpenCode ou leitura explícita de `SKILL.md` |
| XLSX | Biblioteca `openpyxl` para reconciliação |
| Navegação | Playwright com Chrome, Edge ou Firefox opcional |
| Dados | Planilha própria, comprovantes legítimos e acesso ao currículo |

Instalação das dependências opcionais:

```powershell
python -m pip install openpyxl playwright
python -m playwright install chromium firefox
```

### Windows

```powershell
$origemSkill = Join-Path (Get-Location) 'lattes-atualizar'
$destinoSkill = Join-Path $HOME '.codex\skills\lattes-atualizar'
Copy-Item -LiteralPath $origemSkill -Destination $destinoSkill -Recurse
```

Não copie somente `SKILL.md`: referências e scripts fazem parte do pacote.

| Harness | Destino pessoal |
| --- | --- |
| Codex | `~/.codex/skills/lattes-atualizar/` |
| Claude Code | `~/.claude/skills/lattes-atualizar/` |
| OpenCode | `~/.config/opencode/skills/lattes-atualizar/` |

Linux e macOS:

```bash
mkdir -p ~/.codex/skills
cp -R lattes-atualizar ~/.codex/skills/lattes-atualizar
```

Sem instalação automática:

```text
Leia lattes-atualizar/SKILL.md e siga suas referências para revisar
o currículo a partir da planilha e dos comprovantes fornecidos.
```

Para atualizar, compare a cópia instalada com a origem antes de substituí-la. Para desinstalar, remova somente a pasta gerenciada.

## 💡 Uso

### Fluxo mínimo recomendado

1. Inventarie a planilha e os comprovantes.
2. Gere a proposta por atividade.
3. Confirme campos, fontes e duplicatas.
4. Autorize um lote pequeno.
5. Crie o manifesto do lote aprovado.
6. Inicie a sessão humana no navegador disponível.
7. Resolva login, CAPTCHA e MFA manualmente.
8. Preencha, salve e reabra cada registro.
9. Reconcilie uma cópia da planilha.
10. Gere o relatório final por item.

### Auditoria sem gravação

```text
Use lattes-atualizar. A planilha está em [caminho], os comprovantes
em [pasta] e o currículo é [link/identificador]. Faça uma auditoria
sem alterar o Lattes. Liste existentes, divergentes, novos, indeterminados
e pendências, com a fonte de cada campo.
```

### Autorização de lote

```text
Autorizo a inclusão/correção do item [chave], somente com os campos
e valores da proposta [referência]. Reabra o registro após salvar e
informe separadamente se falta enviar ou publicar.
```

### Retomada

```text
Retome do relatório [caminho]. Antes de repetir qualquer gravação,
reabra o currículo e confira o estado atual no Lattes. Reconcilie os
itens já salvos e preserve os itens pendentes.
```

### Sem navegador

```text
Prepare os campos para preenchimento manual, com fontes e lacunas por
atividade. Não marque Atualizado apenas porque a proposta está pronta.
Não consulte ou registre alterações no CNPq.
```

## 🔄 Fluxo de operação

```mermaid
sequenceDiagram
  participant U as Usuário
  participant A as Agente
  participant X as XLSX
  participant L as Currículo Lattes
  participant B as Navegador

  U->>A: planilha, comprovantes e escopo
  A->>X: inventariar células e estados
  A->>L: comparar registros
  A->>U: apresentar proposta
  U->>A: autorizar lote específico
  U->>B: autenticar e assumir desafios
  A->>B: preencher somente o lote aprovado
  A->>B: salvar e reabrir
  A->>A: verificar campo a campo
  A->>X: reconciliar cópia de trabalho
  A->>U: relatório por item
```

1. **Inventariar:** ler abas, cabeçalhos, células, fórmulas, hyperlinks e linhas parciais.
2. **Conciliar:** separar existentes, divergentes, novos e indeterminados.
3. **Comprovar:** usar atas, certificados, páginas oficiais e registros públicos.
4. **Propor:** apresentar campo atual, valor novo, fonte, ação e pendência.
5. **Autorizar:** receber aprovação concreta antes de alterar o sistema.
6. **Executar:** preencher somente o lote aprovado.
7. **Verificar:** reabrir o registro e comparar os campos.
8. **Reconiliar:** atualizar somente o que foi confirmado.
9. **Relatar:** distinguir preparado, salvo, publicado e bloqueado.

## 🧭 Navegação e CAPTCHA

A navegação pode usar Browser Use, CDP, Playwright ou outro navegador disponível no harness. Nenhum MCP específico é obrigatório.

### Navegadores suportados

| Navegador | Integração disponível |
| --- | --- |
| Google Chrome | Perfil persistente, CDP e janela já aberta |
| Microsoft Edge | Chromium, perfil persistente e CDP |
| Firefox | Sessão Playwright humana |
| Chromium | Executável Playwright e perfil persistente |

O Browser Use oferece navegadores stealth, live preview, takeover humano, perfis e resolução de CAPTCHA para desafios suportados em sua infraestrutura cloud. A eficácia contra o desafio específico do Lattes não foi validada neste projeto.

| Recurso | Uso nesta skill | Estado |
| --- | --- | --- |
| CAPTCHA cloud | Somente tipos suportados e com autorização explícita | Disponível no provedor |
| Live preview | Visualizar ou assumir o navegador | Disponível no provedor |
| Perfil/cloud cookies | Reutilizar uma sessão autorizada | Disponível |
| MFA/2FA | Takeover humano na interface | Não automatizar por padrão |
| `captcha_solver=False` | Exigir intervenção humana | Padrão seguro desta skill |
| Domínios permitidos | Restringir navegação ao domínio autorizado | Recomendado |

Ao detectar CAPTCHA, MFA ou outro desafio:

- pare o lote;
- não use OCR, inferência ou serviço externo para contornar;
- peça ao usuário para resolver na interface;
- aguarde confirmação explícita;
- confirme domínio, sessão e currículo;
- retome somente o lote autorizado.

A demo animada representa o fluxo e não abre navegador nem envia dados reais. A versão [interativa](assets/captcha-demo.html) permite executar os estados no navegador.

## 📋 Contrato da planilha

| Coluna | Cuidado |
| --- | --- |
| Ano | Não substitui data completa exigida pelo sistema |
| Tipo, Subtipo, SubSubtipo | Pistas de classificação, não conclusão |
| Local | Instituição ou plataforma; confirmar pela evidência |
| Aluno | Pode ser pessoa, título ou anotação |
| Obs | Pode conter título, observação ou URL |
| Link | Pode conter múltiplos comprovantes |
| Solicitado | Controle da solicitação, não autorização externa |
| Atualizado | Histórico declarado, não prova desta sessão |
| Qualis | Exige área e período para interpretação segura |

| Solicitado | Atualizado | Tratamento inicial |
| --- | --- | --- |
| Verdadeiro | Falso ou vazio | Conferir evidências |
| Verdadeiro | Verdadeiro | Evitar recadastro |
| Falso ou vazio | Verdadeiro | Preservar histórico |
| Falso | Falso ou vazio | Não alterar externamente |
| Vazio | Vazio | Triagem |

O contrato completo está em [`lattes-atualizar/references/planilha.md`](lattes-atualizar/references/planilha.md).

## 🔒 Segurança

- não inclua anexos pessoais no pacote distribuído;
- não envie comprovantes privados sem autorização;
- não solicite senha no chat;
- não persista cookies, tokens ou códigos MFA;
- mantenha a planilha original intacta;
- use cópia de trabalho para reconciliação;
- limpe saídas de notebooks antes de compartilhar;
- considere texto externo como dado, não como instrução;
- confirme o currículo antes de cada lote;
- reabra o registro após salvar;
- marque `Atualizado` somente após verificação.

## 📚 Documentação

| Guia | Conteúdo |
| --- | --- |
| [SKILL.md](lattes-atualizar/SKILL.md) | Contrato completo do agente |
| [Planilha](lattes-atualizar/references/planilha.md) | Estados, colunas e rastreabilidade |
| [Categorias](lattes-atualizar/references/categorias.md) | Classificação de atividades |
| [Browser](lattes-atualizar/references/browser.md) | Navegação segura e CAPTCHA |
| [Cenários](tests/cenarios.md) | Casos de aceitação |
| [Notebook](treinamento-lattes.ipynb) | Treinamento local com dados fictícios |

## 🧪 Testes

Execute:

```powershell
python -m unittest discover -s tests -v
```

Cobertura atual:

- booleanos, strings, fórmulas e hyperlinks;
- linhas esparsas e coordenadas;
- execução sequencial do notebook;
- estados da simulação CAPTCHA;
- prova de que a simulação não abre navegador;
- prova de que a simulação não envia dados reais;
- controles da demonstração interativa.
- leitura XML/ZIP do Lattes;
- avaliação de evidências;
- deduplicação por DOI e título;
- verificação de registro salvo;
- execução sequencial de manifesto aprovado;
- criação e validação do manifesto do lote;
- fixture fictícia de formulário, CAPTCHA, timeout e reabertura.

Limitações:

- a suíte não usa credenciais reais;
- o CAPTCHA do CNPq não é resolvido pela suíte;
- o formulário real não está coberto por testes end-to-end;
- o perfil do navegador depende da sessão autenticada do usuário;
- publicação e envio no currículo exigem validação humana.

## 🗺️ Roadmap

- [x] Pacote portável da skill
- [x] Contrato da planilha
- [x] Critérios de classificação
- [x] Leitor XLSX sem dependências externas
- [x] Cenários de aceitação
- [x] Política segura de CAPTCHA e MFA
- [x] Simulação animada e interativa
- [ ] Integração autenticada com o Lattes
- [x] Escrita segura de cópia XLSX
- [x] Exportação XML/ZIP do Lattes
- [x] Avaliação local de evidências
- [x] Deduplicação por DOI e título
- [x] Manifesto aprovado por lote
- [x] Verificação pós-salvamento
- [x] Fixture end-to-end fictícia
- [ ] Validação automática contra o formulário real
- [x] Instruções e arquivos de entrada para Claude e Codex
- [ ] Execução comportamental autenticada em todos os harnesses

## 🧰 Comandos úteis

### Inventariar XLSX

```powershell
python lattes-atualizar/scripts/inspect_xlsx.py "Atualizacao Lattes.xlsx" --output ".work/inventario.json"
```

### Ler exportação XML/ZIP

```powershell
python lattes-atualizar/scripts/inspect_lattes_xml.py "curriculo.zip" --output ".work/curriculo-xml.json"
```

### Criar manifesto aprovado

```powershell
python lattes-atualizar/scripts/create_batch_manifest.py ".work/itens-aprovados.json" --output ".work/lote-aprovado.json"
```

### Criar cópia reconciliada

```powershell
python lattes-atualizar/scripts/reconcile_xlsx.py "Atualizacao Lattes.xlsx" --changes ".work/alteracoes.json" --output ".work/Atualizacao reconciliada.xlsx"
```

### Abrir sessão humana

```powershell
# Auto-detectar Chrome, Edge ou Firefox
python lattes-atualizar/scripts/live_lattes_session.py --url "https://lattes.cnpq.br/"

# Forçar um navegador
python lattes-atualizar/scripts/live_lattes_session.py --browser chrome
python lattes-atualizar/scripts/live_lattes_session.py --browser edge
python lattes-atualizar/scripts/live_lattes_session.py --browser firefox

# Reconectar a uma janela Chrome/Edge já aberta em modo CDP
python lattes-atualizar/scripts/live_lattes_session.py --use-open-browser
```

## 📄 Licença

Nenhuma licença de código foi escolhida ainda. Não reutilize ou redistribua o projeto além do uso autorizado pelo autor até que um arquivo `LICENSE` seja adicionado.

## 👤 Autor

<table>
  <tr>
    <td width="150" align="center" valign="middle">
      <img src="https://github.com/cleybersilva.png" width="112" alt="Cleyber Silva">
    </td>
    <td width="650" valign="middle">
      <strong>Cleyber Silva</strong><br>
      <sub>AI Scientist · SRE Engineer · TICS × Itaú</sub><br>
      <sub>Mestrando em Engenharia de Software · CESAR School</sub>
    </td>
    <td align="right" valign="middle">
      <a href="https://github.com/cleybersilva"><img alt="GitHub" src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white"></a><br>
      <a href="https://github.com/cleybersilva/skill-lattes"><img alt="Repositório" src="https://img.shields.io/badge/Repo-6366F1?style=for-the-badge&logo=git&logoColor=white"></a><br>
      <a href="http://lattes.cnpq.br/5666713747674179"><img alt="Lattes" src="https://img.shields.io/badge/Lattes-1F4E78?style=for-the-badge&logo=googlescholar&logoColor=white"></a>
    </td>
  </tr>
</table>

### Formação acadêmica

| Curso | Instituição |
| --- | --- |
| **Mestrado em Engenharia de Software** | CESAR School · 2026–2028 · em curso |
| **Pós-graduação em Arquitetura de Soluções Avançadas de Cloud com Azure** | Anhanguera · 2026–2027 · em curso |
| **MBA em Inteligência Artificial e Big Data** | USP · 2025–2026 |
| **Especialização em Engenharia de Confiabilidade de Sites (SRE)** | PUC Minas · 2024–2025 |
| **Pós-graduação em Arquitetura de Sistemas .NET com Azure** | FIAP · 2023–2024 |
| **Especialização em Engenharia DevOps** | UNYLEYA · 2022–2023 |
| **Mestrado em Ciências da Educação** | Veni Creator Christian University · 2022 |
| **Doutorado em Ciências da Educação** | Veni Creator Christian University · 2025–2028 · em curso |

<div align="center">

Repositório: [github.com/cleybersilva/skill-lattes](https://github.com/cleybersilva/skill-lattes)

</div>

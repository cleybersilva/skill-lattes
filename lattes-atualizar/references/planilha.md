# Contrato da planilha

Detecte cabeçalhos por nome, sem depender da letra da coluna. O modelo de origem contém `Ano`, `Tipo`, `Subtipo`, `SubSubtipo`, `Local`, `Aluno`, `Obs`, `Link`, `Solicitado`, `Atualizado`, `Qualis` e colunas auxiliares `Coluna 4` a `Coluna 24`. Preserve auxiliares, mesmo vazias. A aba de origem chama-se `Página1`, mas outras abas e nomes devem ser aceitos.

| Campo | Interpretação e cuidado |
| --- | --- |
| Ano | Ano declarado da atividade, não substitui data completa exigida pelo cadastro. Ano isolado não é atividade pronta. |
| Tipo/Subtipo/SubSubtipo | Classificação de origem com variações e inconsistências. Normalizar só para comparação; preservar original. MPES e DPES não bastam para definir o papel do titular. |
| Local | Instituição ou plataforma, confirmar pelo comprovante. |
| Aluno | Pode conter pessoa, título de atividade ou anotação. Não tratar toda célula como nome de aluno. |
| Obs | Pode conter título, observações e URLs. Não converter automaticamente em texto público. |
| Link | Pode conter vários URLs e quebras de linha. Resolver todos os comprovantes relevantes e reportar inacessíveis. |
| Qualis | Informação declarada, requer área e período de avaliação para validação. Não presumir campo obrigatório do Lattes nem atualizar sem fonte. |
| Solicitado | Controle da solicitação conforme o processo do responsável. Não é autorização automática de alteração externa. |
| Atualizado | Controle histórico de atualização. Não equivale a verificação feita nesta execução. |

## Estados

Preserve booleanos reais. Célula vazia significa desconhecido, não `false`. Aceite textos inequívocos como Sim/Não e True/False apenas na interpretação; valores inesperados precisam de revisão. Nunca use a verdade lógica de uma string (`"False"` não significa verdadeiro).

| Solicitado | Atualizado | Tratamento inicial |
| --- | --- | --- |
| verdadeiro | falso ou vazio | Candidato a pendência, conferir evidências e currículo. |
| verdadeiro | verdadeiro | Declarado atualizado; não recadastrar. Auditar se solicitado. |
| falso ou vazio | verdadeiro | Histórico de atualização sem solicitação marcada; conferir significado, não limpar nem marcar solicitação automaticamente. |
| falso | falso ou vazio | Não solicitado; incluir só no diagnóstico até haver escopo para agir. |
| vazio | vazio | Triagem, não interpretar como autorização ou conclusão. |

Se o responsável definir significado diferente, registre essa definição antes de filtrar. `Solicitado` só muda se a solicitação correspondente de fato ocorrer. `Atualizado` só muda após a operação requerida ser verificada, ou após confirmação comprovada de que o registro já corresponde ao solicitado. Registrar evidência também nesse segundo caso. Não apagar marcações antigas apenas porque não foi possível acessar o currículo.

## Observações do arquivo usado na criação

Em 18/11/2026 foram observadas 48 linhas com atividade e uma linha contendo apenas ano, seguidas de linhas vazias formatadas. Das 48 atividades, 46 estavam marcadas `Atualizado=true` e duas sem marcação. Isso descreve apenas o snapshot, não comprova atualização no CNPq. Há sete atualizações marcadas sem `Solicitado=true`. O fluxo precisa aceitar esse histórico e tratar lacunas sem recadastrar todo o arquivo.

A captura de tela com livros e e-books exemplifica revisão e aprovação, mas seu titular, datas e lista de obras não são dados da planilha fornecida. Não misturar os currículos.

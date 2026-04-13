---
name: review-code
description: Revisa arquivos de código contra os princípios de Clean Architecture + DDD. Reporta violações de camada, lógica no lugar errado e uso incorreto de DDD, com sugestões de correção.
---

<objetivo>
Inspecionar arquivos de código e reportar violações arquiteturais com severidade, localização e orientação de correção. Não aplica correções — gera achados que informam a próxima task do GSD2.
</objetivo>

<leitura_obrigatoria>
Leia nesta ordem antes de revisar qualquer código:
1. `ARCHITECTURE.md` da raiz do projeto
2. `references/clean-architecture.md`
3. `references/ddd-patterns.md`
4. `docs/[contexto-relevante]/GLOSSARY.md` se disponível
5. Os arquivos de código especificados pelo usuário
</leitura_obrigatoria>

<processo>
**PASSO 1 — Identificar o escopo**

Se o usuário especificou arquivos, revise esses arquivos.
Se não, pergunte: "Quais arquivos ou diretórios devo revisar? (ex: `src/domain/`, um arquivo específico, ou a saída de um slice)"

**PASSO 2 — Classificar cada arquivo pela camada esperada**

Com base no caminho:
- `src/domain/**` → deve conter apenas Entities, VOs, Aggregates, interfaces de Repositório, Domain Events, Domain Services
- `src/application/**` → deve conter apenas Use Cases, DTOs, Application Services
- `src/infrastructure/**` → deve conter apenas adapters de DB, implementações ORM, HTTP clients
- `src/presentation/**` → deve conter apenas Controllers, rotas, schemas de request/response

**PASSO 3 — Verificar violações**

Para cada arquivo, verifique:

**Violações CRÍTICAS (devem ser corrigidas antes de entregar):**
- Arquivo em `domain/` importa de `infrastructure/`, `application/` ou `presentation/`
- Arquivo em `application/` importa de `infrastructure/` ou `presentation/`
- Lógica de negócio (condicionais, cálculos, regras) dentro de um Controller
- Lógica de negócio dentro de um model ORM ou adapter de DB
- Chamada direta ao banco de dados dentro de um objeto de domínio
- Use Case que chama outro Use Case (use Application Service para orquestração)
- Interface de Repository em `infrastructure/` em vez de `domain/`

**Violações ADVISORY (deve corrigir, mas não bloqueia entrega):**
- Modelo de domínio anêmico: Entity sem métodos, apenas getters/setters
- Value Object mutável (tem setters)
- Domain Service que chama um repositório (cruzamento de camadas)
- Use Case que faz demais (mais de uma responsabilidade principal)
- Domain Event ausente para uma mudança de estado que outros contextos precisariam saber
- Obsessão por primitivos: uso de strings/ints crus onde um Value Object seria mais claro
- Lógica em DTO ou schema de request/response

**PASSO 4 — Produzir relatório**

```markdown
## Revisão Arquitetural — [escopo revisado]

### Violações CRÍTICAS (bloqueiam entrega)
[para cada: Arquivo | Linha (aprox.) | Regra violada | Correção]

### Violações ADVISORY (melhorar na próxima oportunidade)
[para cada: Arquivo | Problema | Correção sugerida]

### Em Conformidade
[lista de arquivos/padrões que estão corretamente estruturados por camada]

### Próximo Passo
[Se houver violações críticas:]
Crie uma task GSD2: "Corrigir violações arquiteturais em [escopo]"
Referencie esta revisão no plano da task.

[Se apenas advisory:]
Trate as violações advisory no próximo slice disponível ou como /gsd quick task.
```
</processo>

<apos_revisao>
Se violações forem encontradas:
1. NÃO aplique correções neste workflow — este workflow apenas diagnostica.
2. Sugira ao usuário criar uma task GSD2 para o trabalho de correção: `/gsd quick corrigir violações arquiteturais em [escopo]`
3. Registre o padrão em `.gsd/KNOWLEDGE.md` se for um problema recorrente: "Descoberta: [padrão] — Lição: [como evitar]"

Se nenhuma violação for encontrada:
- Declare claramente: "Nenhuma violação arquitetural encontrada em [escopo]."
- Aponte padrões que estão particularmente bem feitos para referência futura.
</apos_revisao>

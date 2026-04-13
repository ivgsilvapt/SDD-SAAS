---
name: guide-design
description: Responde dúvidas de design arquitetural e valida designs propostos contra os princípios de Clean Architecture + DDD.
---

<objetivo>
Ajudar o desenvolvedor a tomar decisões arquiteturais corretas: em qual camada um código pertence, qual padrão DDD aplicar, como modelar um conceito de domínio e se um design proposto é consistente com a constituição de arquitetura do projeto.
</objetivo>

<leitura_obrigatoria>
Sempre leia `ARCHITECTURE.md` da raiz do projeto antes de responder.
Em seguida, leia os arquivos de referência relevantes conforme a dúvida:
- Dúvidas de camadas/dependências → `references/clean-architecture.md`
- Dúvidas de modelagem de domínio → `references/ddd-patterns.md`
- Dúvidas sobre testes → `references/testing-strategy.md`
- Dúvidas sobre escopo de agentes → `references/phase-guards.md`

Se o bounded context relevante tiver `docs/[contexto]/GLOSSARY.md`, leia-o — use apenas os termos canônicos definidos ali.
</leitura_obrigatoria>

<processo>
**Para perguntas "onde este código fica?":**

1. Identifique em uma frase o que o código faz.
2. Aplique estes filtros em ordem:
   - Representa um conceito de negócio com identidade? → **Entity** em `domain/`
   - Representa um conceito de negócio sem identidade (descritivo)? → **Value Object** em `domain/`
   - Aplica uma regra de consistência sobre múltiplas entidades? → **Aggregate Root** em `domain/`
   - Representa algo que aconteceu no domínio? → **Domain Event** em `domain/`
   - Orquestra um caso de uso entre objetos de domínio? → **Use Case** em `application/`
   - Interage com banco de dados, API HTTP ou sistema de arquivos? → `infrastructure/`
   - Trata requisições HTTP, entrada CLI ou mensagens WebSocket? → `presentation/`
3. Declare a camada claramente e explique o porquê.
4. Se o código pertence a duas camadas, explique como dividir.

**Para perguntas "como eu modelo X?":**

1. Leia o GLOSSARY.md do bounded context (se existir).
2. Identifique o conceito central: é uma Entity, Value Object ou Aggregate?
3. Identifique as regras de consistência: quais invariantes devem ser sempre verdadeiros?
4. Identifique os comportamentos: o que este conceito pode fazer?
5. Proponha um modelo com:
   - Nome (use a terminologia do GLOSSARY.md)
   - Tipo (Entity / Value Object / Aggregate Root)
   - Propriedades (com tipos)
   - Invariantes (regras que devem sempre ser válidas)
   - Comportamentos (métodos que mudam o estado)
   - Domain Events emitidos (se houver)

**Para perguntas "este design está correto?":**

1. Leia o design proposto.
2. Verifique contra `references/clean-architecture.md` para violações de camada.
3. Verifique contra `references/ddd-patterns.md` para uso incorreto de padrões.
4. Reporte:
   - ✅ O que está correto
   - ❌ O que viola as regras (cite qual regra)
   - 💡 Como corrigir cada violação

**Para perguntas "devo usar o padrão X ou Y?":**

Aplique a árvore de decisão em `references/ddd-patterns.md`.
Declare a escolha claramente e explique o trade-off em um parágrafo.
</processo>

<arvores_de_decisao>
## Árvores de Decisão Comuns

**Entity vs Value Object:**
- Tem identidade única que persiste através de mudanças de estado? → Entity
- Definida inteiramente por seus atributos (duas instâncias com os mesmos atributos são iguais)? → Value Object
- Em dúvida: duas instâncias podem ser trocadas sem que o sistema perceba? Se sim → Value Object

**Use Case vs Domain Service:**
- Orquestra um fluxo que envolve múltiplos objetos de domínio e pode chamar repositórios? → Use Case (camada Application)
- Expressa uma operação de domínio que não pertence naturalmente a uma entidade? → Domain Service (camada Domain)
- A diferença: Use Cases conhecem repositórios. Domain Services não conhecem.

**Repository vs DAO:**
- Deve parecer uma coleção de objetos de domínio (add, remove, findById, findBy...)? → Interface Repository em `domain/`, implementação em `infrastructure/`
- DAOs não pertencem à Clean Architecture — mapeie linhas do banco para objetos de domínio na implementação de infrastructure.

**Domain Event vs evento de Application:**
- Algo significativo aconteceu no domínio e outras partes do domínio se importam? → Domain Event (camada `domain/`)
- Algo aconteceu no nível de aplicação (ex: "notificação de usuário registrado deve ser enviada")? → evento no nível de Application ou chamada direta do Use Case
</arvores_de_decisao>

<registro_de_decisoes>
Quando o usuário aceitar uma decisão arquitetural:
1. Registre em `.gsd/DECISIONS.md` com data, decisão, motivação e consequências.
2. Se a decisão introduz um novo termo, adicione-o ao `docs/[contexto]/GLOSSARY.md` relevante.
3. Se a decisão contradiz algo no `ARCHITECTURE.md`, deixe isso explícito — o usuário decide se atualiza a constituição ou mantém a regra original.
</registro_de_decisoes>

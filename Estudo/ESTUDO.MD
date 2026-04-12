# Estudo Comparativo: Vibe Coding com vs. sem a Estrutura do Kit de Arquitetura SaaS

**Referência:** [ORIENTACAO.md](../ORIENTACAO.md)
**Data:** 2026-04-06

---

## 1. Estimativa de Tokens por Feature

### Tamanhos dos arquivos do kit (estimativas reais)

| Arquivo | Tokens aprox. |
|---|---|
| ARCHITECTURE.md completo | ~8.000 |
| ARCHITECTURE.md seções 0–3 | ~2.000 |
| ARCHITECTURE.md seções 0–5 | ~3.500 |
| ARCHITECTURE.md seções 1+5 | ~2.000 |
| SPEC_TEMPLATE.md | ~2.500 |
| TESTING_GUIDE.md | ~3.000 |
| SAAS_PATTERNS.md | ~5.000 |
| GLOSSARY.md (preenchido) | ~1.500 |
| SPEC gerado (feature média) | ~3.000 |

---

### Custo COM a estrutura — feature média (5–8 FRs, 4 SPRINTs)

| Etapa | Tokens de entrada | Tokens de saída | Total |
|---|---|---|---|
| Agente Spec | ~6.200 (Arch 0–3 + Template + Glossary + descrição) | ~3.000 (SPEC) | ~9.200 |
| Agente Analyze | ~5.000 (SPEC + Arch 1+5) | ~800 (relatório) | ~5.800 |
| SPRINT 1: Impl + Test + Review | ~15.000 (contextos) | ~6.000 (código + testes) | ~21.000 |
| SPRINT 2: Impl + Test + Review | ~13.000 | ~5.500 | ~18.500 |
| SPRINT 3: Impl + Test + Review + Migration | ~14.000 | ~6.500 | ~20.500 |
| SPRINT 4: Impl + Test + Review | ~14.000 | ~7.000 | ~21.000 |
| **Total** | | | **~96.000 tokens** |

**Resultado entregue:** domínio modelado, use cases, repositórios, API com contrato, testes por camada, migrations, sem violações arquiteturais.

---

### Custo SEM a estrutura — mesma feature, vibe coding livre

| Sessão | O que acontece | Tokens |
|---|---|---|
| Sessão 1 | "Codifique gerenciamento de assinatura" → IA gera tudo junto num arquivo | ~4.000 |
| Sessão 2 | "Tem um bug no cancelamento" → correção parcial, cria novo bug | ~4.500 |
| Sessão 3 | "Agora o admin vê dados de outros clientes" (falha multi-tenant) | ~5.000 |
| Sessão 4 | "Os testes estão falhando" → testes escritos depois, cobrem pouco | ~4.500 |
| Sessão 5 | Semanas depois: "Preciso adicionar uma feature nova, mas não entendo o código" → IA precisa re-analisar o código existente | ~8.000 |
| Sessão 6–N | Mais bugs, mais refatorações não planejadas | ~5.000 por sessão |
| **Total estimado (6 sessões + bugs persistentes)** | | **~35.000–60.000 tokens** |

**Resultado entregue:** feature "funcionando" em happy path, mas com dívida técnica, sem testes confiáveis, bugs latentes de segurança e multi-tenancy, código difícil de estender.

---

## 2. A Curva de Custo ao Longo do Tempo

```
Tokens gastos (acumulado)
     │
800k │                                           ■ SEM estrutura
     │                                      ■
600k │                                 ■
     │                    ■ COM estrutura
400k │               ■
     │          ■
200k │     ■■■■
     │■■■■
     └──────────────────────────────────────────▶ Tempo
       1 feat  3 feats  5 feats  10 feats  20 feats
```

**Por que a curva sem estrutura sobe mais rápido:**

1. **Custo de contexto cresce com o tamanho do projeto.** Sem SPECs, a cada nova sessão você precisa re-explicar o que existe. Com 10 features implementadas, explicar o sistema pode custar 10.000–20.000 tokens só de contexto inicial.

2. **Bugs arquiteturais se multiplicam.** Uma violação de multi-tenancy encontrada na feature 8 pode obrigar a revisar as features 1–7. Isso não acontece com a estrutura porque o Review e os testes barram antes.

3. **Retrabalho de features.** Sem SPEC, a IA frequentemente implementa o que entendeu, não o que você quis. Refazer uma feature implementada pode custar mais tokens do que o custo total da estrutura.

4. **Com a estrutura, o SPEC é memória eficiente.** Um SPEC de 3.000 tokens descreve uma feature inteira com precisão. Sem ele, você gasta 3x mais tokens re-explicando o contexto e tentando reconstruir intenções.

**Ponto de equilíbrio estimado:** em torno da **3ª a 5ª feature**, o custo acumulado se iguala. A partir daí, a estrutura economiza tokens.

---

## 3. O que os Tokens Não Medem — As Vantagens Reais

**Vantagem 1 — Consistência entre sessões**
Sem a estrutura, cada sessão de vibe coding pode gerar código em estilo diferente. A IA não tem memória entre sessões. Com o ARCHITECTURE.md como contexto, ela segue as mesmas regras na sessão 1 e na sessão 100.

**Vantagem 2 — Código seguro por padrão**
Falhas de multi-tenancy (tenant A vendo dados do tenant B), SQL injection e IDOR são silenciosas — você não descobre sem testar especificamente. A estrutura força a verificação em checklist antes de aprovar cada SPRINT. Uma única falha de segurança em produção custa infinitamente mais do que todos os tokens do kit.

**Vantagem 3 — Manutenibilidade não-linear**
Um projeto sem estrutura começa rápido e fica cada vez mais lento. Adicionar a 10ª feature num código sem separação de camadas pode ser 5x mais trabalhoso que a 1ª. Com Clean Architecture, o custo por feature tende a ser constante.

**Vantagem 4 — Múltiplos projetos**
O kit foi projetado para ser reutilizado. Os 6 arquivos não mudam entre projetos — apenas o GLOSSARY.md. O custo de setup diminui para zero a partir do 2º SaaS.

**Vantagem 5 — Documentação viva**
Os SPECs são documentação. Se você ou outro desenvolvedor precisar entender o sistema 6 meses depois, os SPECs explicam o comportamento esperado de cada feature. Sem isso, você depende do código (e da memória da IA).

---

## 4. Quando a Estrutura NÃO Vale a Pena

| Cenário | Recomendação |
|---|---|
| Protótipo descartável (< 2 semanas, nunca vai a produção) | Não use o kit |
| Experimento técnico (testar uma biblioteca, PoC) | Não use o kit |
| MVP de validação rápida com aceitação de dívida técnica consciente | Use versão lite (ver seção 5) |
| SaaS de produção com múltiplas features e usuários pagantes | Use o kit completo |
| Múltiplos SaaS com base comum | Use o kit completo — ROI alto |

---

## 5. Versão Lite — Princípios que Podem Ser Desconsiderados

### Pode remover sem risco significativo (por contexto)

| Princípio / Padrão | Quando remover | Impacto de remover |
|---|---|---|
| **CQRS / Read Models separados** | Se não tem relatórios complexos ou dashboards pesados | Pequeno — use o mesmo repositório para leitura simples |
| **Circuit Breaker** | Se tem ≤ 1 integração externa crítica | Pequeno — substitua por timeout simples |
| **Agente Migration** | Se o schema é simples (< 10 tabelas) | Pequeno — escreva migrations manualmente |
| **SPRINT 5 (Transversal)** | Para maioria das features | Nenhum — middleware padrão já cobre |
| **SAAS_PATTERNS.md completo** | Se o SaaS NÃO for multi-tenant ainda | Nenhum na fase atual |
| **LGPD/GDPR patterns** | Se não processa dados de pessoas físicas | Nenhum — adicione quando necessário |
| **AOP formal** | Pode usar middleware simples em vez de aspecto formal | Pequeno |
| **Law of Demeter (strict)** | Em código interno sem API pública | Pequeno — aplique apenas em interfaces |
| **12-Factor completo** | Mantenha apenas: Config via env vars + Logs em stdout + Stateless | Médio se ignorar Stateless |

### Nunca remova — são o núcleo que justifica toda a estrutura

| Princípio | Por que é inegociável |
|---|---|
| **SDD (SPEC antes do código)** | Remove o maior desperdício de tokens: implementar a coisa errada |
| **Domain-First + Clean Architecture** | Impede que a base se torne intratável depois de 5+ features |
| **SOLID (SRP + DIP mínimo)** | SRP evita classes monstro; DIP torna tudo testável |
| **Result\<T,E\> — sem null silencioso** | Bugs silenciosos custam mais que qualquer princípio economizado |
| **Isolamento de tenant (row-level)** | Uma brecha expõe dados de todos os clientes |
| **Validação na borda (Command Object)** | SQL injection e dados corrompidos entram por aqui |
| **Sem config hardcoded** | Credentials no código são vazamentos esperando acontecer |
| **Ubiquitous Language / Glossary** | Sem isso a IA usa nomes diferentes para a mesma coisa e o código vira babel |
| **Testes unitários de domínio** | É a camada mais barata de testar e onde mais bugs de negócio vivem |

---

## 6. Configuração Recomendada por Perfil

### Perfil A — MVP rápido (validação de mercado, 1–3 meses)

Use apenas:
- ARCHITECTURE.md (seções 0–5 apenas)
- SPEC_TEMPLATE.md (simplifique: remova SPRINT 5, NFRs opcionais, sem Contrato de API formal)
- GLOSSARY.md (preencha minimamente)
- Agentes: apenas Spec + Implementation + Review (pule Testing formal, testes manuais básicos)

**Redução de tokens:** ~55% em relação ao kit completo
**Risco aceito:** sem testes automatizados formais, sem migrations gerenciadas, sem Circuit Breaker

### Perfil B — SaaS de produção (3–12 meses, usuários pagantes)

Use o kit completo. O custo extra de tokens é recuperado na primeira falha de segurança evitada ou no primeiro refactor que não precisou acontecer.

### Perfil C — Múltiplos SaaS (plataforma ou portfólio)

Use o kit completo sem cortes. O overhead de setup cai para quase zero a partir do 2º projeto — ARCHITECTURE.md, AGENTS.md e TESTING_GUIDE.md são reutilizados sem modificação.

---

## 7. Resumo Executivo

| Dimensão | SEM estrutura | COM estrutura (completo) | COM estrutura (lite) |
|---|---|---|---|
| Tokens por feature (curto prazo) | ~35k–60k | ~96k | ~55k |
| Tokens por feature (após 10 features) | ~80k–150k | ~96k | ~60k |
| Custo total (20 features) | Alto e crescente | Estável | Estável e menor |
| Consistência entre sessões | Baixa | Alta | Alta |
| Segurança (multi-tenant, injection) | Depende da sorte | Verificada | Verificada (sem Circuit Breaker) |
| Manutenibilidade após 6 meses | Baixa–Média | Alta | Alta |
| Velocidade da 1ª feature | Rápida | Lenta | Média |
| Velocidade da 10ª feature | Lenta | Constante | Constante |
| Adequado para produção | Arriscado | Sim | Sim (com ressalvas) |

---

## 8. Conclusão

A verdadeira vantagem não está em tokens — está em que o código gerado **ainda funciona e é seguro quando você voltar nele em 6 meses**. Isso é o que o vibe coding sem estrutura não consegue garantir.

**Recomendação direta:**

- Se o projeto vai durar mais de 3 meses ou ter usuários pagantes: **use o kit completo.** O custo extra de tokens em features iniciais é seguro de desenvolvimento, não desperdício.
- Se é um MVP de validação: **use a versão lite** — mantenha SDD, Clean Architecture e Domain-First; corte CQRS, Circuit Breaker, Migration Agent e Sprint 5.
- Se é um protótipo descartável: **ignore o kit.**

---
name: clean-architecture
description: Definições de camadas, regras de dependência e o que pertence a cada camada da Clean Architecture.
---

# Clean Architecture — Regras de Camadas

## As Quatro Camadas

```
┌─────────────────────────────────────┐
│          PRESENTATION               │  Controllers, Rotas, Middleware
│  depende de: Application apenas     │  Schemas de Request/Response
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│           APPLICATION               │  Use Cases, DTOs
│  depende de: Domain apenas          │  Application Services, Ports
└──────────────────┬──────────────────┘
                   │
┌──────────────────▼──────────────────┐
│              DOMAIN                 │  Entidades, Value Objects, Aggregates
│  depende de: NADA                   │  Interfaces de Repositório, Domain Events
└─────────────────────────────────────┘
         ▲
         │ implementa
┌────────┴────────────────────────────┐
│         INFRASTRUCTURE              │  Repositórios ORM, Adapters de DB
│  depende de: Domain (implementa)    │  HTTP Clients, Sistemas de Arquivos, APIs Externas
└─────────────────────────────────────┘
```

**A Regra de Dependência:** Dependências no código-fonte devem apontar para dentro. Nada em um círculo interno pode conhecer algo em um círculo externo.

---

## Camada Domain — `src/domain/`

**O que fica aqui:**
- Entidades (objetos com identidade)
- Value Objects (objetos sem identidade, definidos por atributos)
- Aggregate Roots (fronteiras de consistência)
- Domain Events (coisas que aconteceram)
- Interfaces de Repositório (abstrações tipo coleção — sem implementação)
- Domain Services (operações sem estado sobre objetos de domínio que não se encaixam em uma entidade)
- Erros e exceções de domínio

**O que NÃO fica aqui:**
- Nenhum import de `infrastructure/`, `application/` ou `presentation/`
- Nenhum decorator de ORM ou anotação de banco de dados
- Nenhum código HTTP ou de framework
- Nenhuma operação de I/O (sistema de arquivos, rede, console)
- Lógica de negócio que pertence a um Use Case específico (orquestração)

**Abordagem de testes:** Unitários puros, sem mocks necessários — objetos de domínio não têm dependências externas.

---

## Camada Application — `src/application/`

**O que fica aqui:**
- Use Cases (um por operação iniciada pelo usuário ou sistema)
- DTOs (Data Transfer Objects — containers de dados simples, sem lógica)
- Application Services (orquestram múltiplos Use Cases)
- Interfaces de Port (portas de entrada/saída para variações hexagonais)
- Mappers (transformações Domain ↔ DTO)

**O que NÃO fica aqui:**
- Nenhum import de `infrastructure/` ou `presentation/`
- Queries ao banco (use interfaces de Repositório de `domain/`)
- Código específico de framework (anotações HTTP, decorators ORM)
- Lógica de negócio que pertence a objetos de domínio

**Padrão:** Um Use Case recebe um DTO, carrega objetos de domínio via Repositório, chama métodos de domínio, salva via Repositório e retorna um DTO. Nada mais.

**Abordagem de testes:** Unitários com Repositório mockado. Sem banco de dados real necessário.

---

## Camada Infrastructure — `src/infrastructure/`

**O que fica aqui:**
- Implementações de Repositório (implementam as interfaces definidas em `domain/`)
- Models de ORM e mapeamentos de banco de dados
- Migrations de banco de dados
- HTTP clients para APIs externas
- Adapters de sistema de arquivos
- Serviços de envio de e-mail, SMS, notificações push
- Implementações de cache
- Adapters de fila/message broker

**O que NÃO fica aqui:**
- Lógica de negócio — se você está colocando um if/else que representa uma regra, mova para `domain/`
- Orquestração de Use Cases — se você está chamando múltiplos objetos de domínio, mova para `application/`

**Inversão de dependência:** Infrastructure DEPENDE de Domain (não o contrário). Infrastructure implementa interfaces de domínio. Domain nunca importa infrastructure.

**Abordagem de testes:** Integração com dependências reais (banco real, HTTP real). Use test containers ou bancos in-memory.

---

## Camada Presentation — `src/presentation/`

**O que fica aqui:**
- HTTP Controllers (handlers de rota)
- Definições de rota
- Schemas de Request/Response (validação, serialização)
- Middleware de entrada (auth, rate limiting, logging)
- Handlers de WebSocket
- Handlers de comando CLI
- Resolvers GraphQL

**O que NÃO fica aqui:**
- Lógica de negócio — controllers chamam Use Cases, nada mais
- Acesso direto a repositórios — sempre passe pelos Use Cases
- Objetos de domínio nas respostas — mapeie para DTOs/schemas de resposta primeiro

**Padrão:** Recebe entrada → valida → chama Use Case → mapeia resultado → retorna resposta.

**Abordagem de testes:** Integração/E2E com servidor real.

---

## Violações de Dependência — Referência Rápida

| Import | De | Violação | Severidade |
|--------|------|-----------|----------|
| `domain/` | `infrastructure/` | Domain depende de infra | CRÍTICA |
| `domain/` | `application/` | Domain depende de application | CRÍTICA |
| `domain/` | `presentation/` | Domain depende de UI | CRÍTICA |
| `application/` | `infrastructure/` | Application bypassa inversão de dependência | CRÍTICA |
| `application/` | `presentation/` | Application depende de UI | CRÍTICA |
| `presentation/` | `domain/` diretamente | Pula a camada application | ADVISORY |
| Lógica de negócio | `presentation/` | Lógica no controller | CRÍTICA |
| Lógica de negócio | `infrastructure/` | Lógica no adapter de DB | CRÍTICA |

---

## Convenções de Nomenclatura

| Conceito | Sufixo | Exemplo |
|---------|--------|---------|
| Entity | (nenhum) | `Pedido`, `Cliente`, `Fatura` |
| Value Object | (nenhum ou descritivo) | `Dinheiro`, `EnderecoEmail`, `StatusPedido` |
| Aggregate Root | (nenhum, documentado claramente) | `Pedido` (root do aggregate de pedido) |
| Interface de Repositório | `Repository` | `PedidoRepository`, `ClienteRepository` |
| Implementação de Repositório | prefixo tecnologia | `PrismaPedidoRepository`, `SqlPedidoRepository` |
| Use Case | verbo + substantivo | `CriarPedido`, `CancelarAssinatura`, `ConvidarUsuario` |
| Domain Event | tempo passado | `PedidoRealizado`, `AssinaturaCancelada`, `UsuarioConvidado` |
| Domain Service | substantivo + `Service` | `ServicoPreco`, `CalculadorFrete` |
| DTO | substantivo + `Dto` | `CriarPedidoDto`, `RespostaPedidoDto` |
| Controller | substantivo + `Controller` | `PedidoController`, `UsuarioController` |

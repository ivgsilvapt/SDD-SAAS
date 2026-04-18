Você é o Agente API Docs. Sua responsabilidade é gerar e manter documentação OpenAPI sincronizada com o código.

Antes de qualquer ação, leia os arquivos de:
- Controllers (src/presentation/controllers/)
- Command Objects (src/presentation/input/)
- ViewModels (src/presentation/viewmodels/)

Se openapi.yaml já existir na raiz ou em docs/, leia-o antes de gerar para detectar breaking changes.

Tarefa: gere ou atualize a documentação de API.
$ARGUMENTS

Se argumentos forem fornecidos, documente apenas os controllers especificados.
Se nenhum argumento for fornecido, documente todos os controllers encontrados.

Processo obrigatório:

1. Para cada endpoint encontrado, gere a documentação:
   - Método HTTP + path (ex: POST /api/v1/subscriptions)
   - Descrição em uma linha
   - Tags (bounded context / domínio)
   - Parâmetros de path (ex: :id) e query (ex: ?page=1&pageSize=20)
   - Request body: schema derivado do Command Object com:
     - Tipos de cada campo
     - Validações (required, format, min, max)
     - Exemplo realista (dados fictícios, nunca PII real)
   - Responses:
     - 200/201: schema do ViewModel com exemplo
     - 400: lista de campos inválidos (formato padrão do projeto)
     - 401: sem token ou token inválido
     - 403: sem permissão (role insuficiente)
     - 404: recurso não encontrado (quando aplicável)
     - 409: conflito (quando aplicável)
     - 422: dados semanticamente inválidos (quando aplicável)
     - 429: rate limit excedido (quando rate limiting estiver configurado)

2. Se openapi.yaml anterior existir, compare e liste breaking changes:
   - Campo obrigatório removido do request body
   - Tipo de campo alterado
   - Endpoint removido
   - Status code de sucesso alterado (201 → 200 ou vice-versa)
   - Renomeação de campo no response

3. Gere o openapi.yaml completo no formato OpenAPI 3.0.3.
   Use a estrutura:
   ```yaml
   openapi: 3.0.3
   info:
     title: [nome do projeto]
     version: 1.0.0
   servers:
     - url: /api/v1
   tags:
     - name: [bounded-context]
   paths:
     /[recurso]:
       post:
         ...
   components:
     schemas:
       ...
     securitySchemes:
       BearerAuth:
         type: http
         scheme: bearer
         bearerFormat: JWT
   ```

Anti-patterns a evitar:
- Não documente campos internos (IDs de auditoria, campos de soft delete) que nunca aparecem na API pública
- Não omita responses de erro — são parte do contrato
- Não gere exemplos com dados pessoais reais (use fake data: john@example.com, não um e-mail real)
- Não use "string" como único tipo — seja específico (format: uuid, format: date-time, etc.)

Salve o resultado em openapi.yaml na raiz do projeto (ou atualize o existente).
Liste ao final: endpoints documentados, breaking changes detectados (se houver), e schema components gerados.

Siga as diretrizes do Agente API Docs definidas em AGENTS.md.

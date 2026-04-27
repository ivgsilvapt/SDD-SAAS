// Harness Template: lint-staged — formata e linta apenas os arquivos modificados
// Requer: npm install -D lint-staged eslint prettier

/** @type {import('lint-staged').Config} */
module.exports = {
  // TypeScript: lint (auto-fix) + format
  '*.{ts,tsx}': ['eslint --fix --max-warnings 0', 'prettier --write'],

  // JavaScript
  '*.{js,jsx,mjs,cjs}': ['eslint --fix', 'prettier --write'],

  // JSON, YAML, Markdown: apenas format
  '*.{json,jsonc,yaml,yml,md}': ['prettier --write'],

  // Arquivos de teste TypeScript: também roda typecheck
  '*.test.ts': [
    () => 'tsc --noEmit',
    'eslint --fix --max-warnings 0',
    'prettier --write',
  ],
};

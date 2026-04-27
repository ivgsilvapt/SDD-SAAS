// Harness Template: commitlint — valida Conventional Commits
// Requer: npm install -D @commitlint/config-conventional @commitlint/cli

/** @type {import('@commitlint/types').UserConfig} */
module.exports = {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // Tipos permitidos (além dos padrão do config-conventional)
    'type-enum': [
      2,
      'always',
      ['feat', 'fix', 'docs', 'style', 'refactor', 'perf', 'test', 'build', 'ci', 'chore', 'revert', 'spec'],
    ],
    // Escopo obrigatório — deve ser o bounded context ou módulo
    // Descomente para tornar obrigatório:
    // 'scope-empty': [2, 'never'],
    'subject-case': [2, 'never', ['upper-case', 'pascal-case', 'start-case']],
    'subject-max-length': [2, 'always', 100],
    'body-max-line-length': [2, 'always', 200],
  },
};

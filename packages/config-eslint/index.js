module.exports = {
  // https://eslint.org/docs/user-guide/configuring#configuration-cascading-and-hierarchy
  // This option interrupts the configuration hierarchy at this file
  // Remove this if you have an higher level ESLint config file (it usually happens into a monorepos)
  // root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  parser: '@typescript-eslint/parser',
  extends: [
    // 'eslint:recommended', // No, seriously, f' you.
    'plugin:@typescript-eslint/recommended',
    'prettier',
  ],
  plugins: ['@typescript-eslint'],
  parserOptions: {
    sourceType: 'module',
    ecmaVersion: 2020,
  },
  rules: {
    'prefer-promise-reject-errors': 'off',

    quotes: ['warn', 'single', { avoidEscape: true }],

    // This rule is not needed because "This is TypeScript!!!" (kicks eslint into a pit of despair)
    '@typescript-eslint/explicit-function-return-type': 'off',

    // Because naming things is hard and following es2015's import pattern obfuscates code.
    '@typescript-eslint/no-namespace': 'off',

    // Sometimes we need `any` because we don't have time to write a cluster-fuck of TS nutiness
    // to workaround a very dynamic function. Look what it did to my boys Vue and Svelt.
    '@typescript-eslint/no-explicit-any': 'off',

    // eslint is a micromanaging Karen, sometimes 😐.
    '@typescript-eslint/ban-types': 'off',
    '@typescript-eslint/no-empty-interface': 'off',
    '@typescript-eslint/ban-ts-comment': 'off',
    '@typescript-eslint/no-non-null-assertion': 'off',
    '@typescript-eslint/no-unused-vars': [
      'warn',
      {
        argsIgnorePattern: '^_',
        varsIgnorePattern: '^_',
        caughtErrorsIgnorePattern: '^_',
      },
    ],

    // The core 'no-unused-vars' rules (in the eslint:recommended ruleset) does not work when
    // working with 3rd party libraries that employ argument order over config-like parameters.
    'no-unused-vars': 'off',

    // allow debugger during development only
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
  },
}

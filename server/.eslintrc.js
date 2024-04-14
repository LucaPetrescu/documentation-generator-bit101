module.exports = {
  root: true,
  extends: "eslint:recommended",
  env: {
    node: true,
    es2021: true,
  },
  parser: "@babel/eslint-parser",
  parserOptions: {
    ecmaVersion: "latest",
    requireConfigFile: false,
    sourceType: "module",
    ecmaFeatures: {
      jsx: true,
      modules: true,
      legacyDecorators: true,
    },
  },
  plugins: ["decorators"],
  ignorePatterns: [".eslintrc.js"],
  rules: {},
};

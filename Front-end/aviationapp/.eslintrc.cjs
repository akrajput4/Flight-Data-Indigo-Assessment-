module.exports = {
  env: {
    browser: true,
    es2021: true,
  },
  globals: {
    window: true,
    document: true,
  },
  extends: [
    // By extending from a plugin config, we can get recommended rules without having to add them manually.
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:import/recommended",
    "plugin:react/jsx-runtime",
    "plugin:react-hooks/recommended",
    // "plugin:@typescript-eslint/recommended",
    // This disables the formatting rules in ESLint that Prettier is going to be responsible for handling.
    // Make sure it"s always the last config, so it gets the chance to override other configs.
    "eslint-config-prettier",
  ],
  ignorePatterns: ["dist", ".eslintrc.cjs"],
  rules: {
    "prettier/prettier": [
      "warn",
      {
        endOfLine: "auto",
      },
    ],
    "no-unused-vars": "warn",
    "react/prop-types": 0,
    "no-extra-boolean-cast": 0,
    "no-dupe-keys": "warn",
    "react/display-name": 0,
    "react/react-in-jsx-scope": "off",
    "no-undef": 1,
    "react-refresh/only-export-components": [
      "warn",
      { allowConstantExport: true },
    ],
    "react-hooks/rules-of-hooks": "error",
    "react-hooks/exhaustive-deps": 0,
  },
  parserOptions: {
    ecmaVersion: 12,
    sourceType: "module",
    ecmaFeatures: {
      modules: true,
      jsx: true,
    },
  },
  settings: {
    react: {
      // Tells eslint-plugin-react to automatically detect the version of React to use.
      version: "detect",
    },
    // Tells eslint how to resolve imports
    "import/resolver": {
      node: {
        paths: ["src"],
        extensions: [".js", ".jsx", ".ts", ".tsx"],
      },
    },
    "import/resolver": {
      alias: {
        map: [
          ["@/components", "./src/components"],
          ["@/icons", "./src/icons"],
          ["@/_store", "./src/_store"],
          ["@/constants", "./src/constants"],
          ["@/data", "./src/data"],
          ["@/common", "./src/common"],
          ["@/_api", "./src/_api"],
          ["@/themes", "./src/themes"],
          ["@/assets", "./src/assets"],
          ["@/modules", "./src/modules"],
          ["@/utils", "./src/utils"],
          ["@/customHooks", "./src/customHooks"],
          ["@/HOC", "./src/HOC"],
        ],
        extensions: [".js", ".jsx", ".json"],
      },
    },
  },
  plugins: ["react", "react-refresh", "import", "jsx-a11y", "prettier"],
};

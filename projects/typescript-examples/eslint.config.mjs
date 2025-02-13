import eslint from "@eslint/js";
import tseslint from "typescript-eslint";
import globals from "globals";

export default tseslint.config(
  {
    languageOptions: {
      globals: {
        ...globals.node,
      },
    },
    ignores: ["**/contracts/artifacts/**"],
    files: ["**/src/**", "**/tests/**"],
  },
  eslint.configs.recommended,
  tseslint.configs.recommended,
);

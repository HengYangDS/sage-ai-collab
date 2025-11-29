# Monorepo Scenario Context

> Pre-configured context for monorepo project management

---

## Table of Contents

- [1. Scenario Profile](#1-scenario-profile)
- [2. Relevant Knowledge](#2-relevant-knowledge)
- [3. Structure Patterns](#3-structure-patterns)
- [4. Tooling](#4-tooling)
- [5. Dependency Management](#5-dependency-management)
- [6. CI/CD Patterns](#6-cicd-patterns)
- [7. Common Tasks](#7-common-tasks)
- [8. Autonomy Calibration](#8-autonomy-calibration)

---

## 1. Scenario Profile

```yaml
scenario: monorepo
languages: [ typescript, python, go ]
tools: [ nx, turborepo, pnpm, lerna, bazel ]
focus: [ structure, dependencies, ci_cd, code_sharing ]
autonomy_default: L3
```

---

## 2. Relevant Knowledge

| Priority      | Files                                                                                    |
|---------------|------------------------------------------------------------------------------------------|
| **Auto-Load** | `core/principles.md` · `guidelines/engineering.md` · `practices/engineering/patterns.md` |
| **On-Demand** | `practices/documentation/project_directory_structure.md` · `guidelines/code_style.md`    |

---

## 3. Structure Patterns

### 3.1 Common Monorepo Layout

```
monorepo/
├── apps/                    # Deployable applications
│   ├── web/                 # Frontend application
│   ├── api/                 # Backend API
│   └── mobile/              # Mobile application
├── packages/                # Shared packages/libraries
│   ├── ui/                  # UI component library
│   ├── utils/               # Shared utilities
│   ├── config/              # Shared configuration
│   └── types/               # Shared type definitions
├── tools/                   # Build tools and scripts
├── docs/                    # Documentation
├── .github/                 # CI/CD workflows
├── package.json             # Root package.json
├── pnpm-workspace.yaml      # Workspace configuration
├── turbo.json               # Turborepo config
└── nx.json                  # Nx config (if using Nx)
```

### 3.2 Package Naming Convention

| Type         | Pattern         | Example                   |
|--------------|-----------------|---------------------------|
| Applications | `@org/app-name` | `@acme/web`, `@acme/api`  |
| Libraries    | `@org/lib-name` | `@acme/ui`, `@acme/utils` |
| Config       | `@org/config-*` | `@acme/config-eslint`     |
| Types        | `@org/types-*`  | `@acme/types-shared`      |

### 3.3 Architecture Principles

| Principle              | Description                                |
|------------------------|--------------------------------------------|
| **Single Version**     | One version of each dependency across repo |
| **Shared Tooling**     | Common lint, test, build configuration     |
| **Clear Boundaries**   | Well-defined package interfaces            |
| **Dependency Graph**   | Explicit internal dependencies             |
| **Incremental Builds** | Only rebuild what changed                  |

---

## 4. Tooling

### 4.1 Tool Comparison

| Tool          | Language   | Best For           | Key Feature         |
|---------------|------------|--------------------|---------------------|
| **Nx**        | TypeScript | Full-featured      | Computation caching |
| **Turborepo** | Any        | Fast builds        | Remote caching      |
| **pnpm**      | Node.js    | Package management | Disk efficient      |
| **Lerna**     | Node.js    | Publishing         | Version management  |
| **Bazel**     | Any        | Large scale        | Hermetic builds     |

### 4.2 Turborepo Configuration

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [
    "**/.env.*local"
  ],
  "pipeline": {
    "build": {
      "dependsOn": [
        "^build"
      ],
      "outputs": [
        "dist/**",
        ".next/**"
      ]
    },
    "test": {
      "dependsOn": [
        "build"
      ],
      "inputs": [
        "src/**/*.tsx",
        "src/**/*.ts",
        "test/**/*.ts"
      ]
    },
    "lint": {
      "outputs": []
    },
    "dev": {
      "cache": false,
      "persistent": true
    }
  }
}
```

### 4.3 pnpm Workspace

```yaml
# pnpm-workspace.yaml
packages:
  - 'apps/*'
  - 'packages/*'
  - 'tools/*'
```

### 4.4 Nx Configuration

```json
{
  "$schema": "./node_modules/nx/schemas/nx-schema.json",
  "targetDefaults": {
    "build": {
      "dependsOn": [
        "^build"
      ],
      "inputs": [
        "production",
        "^production"
      ]
    },
    "test": {
      "inputs": [
        "default",
        "^production"
      ]
    }
  },
  "namedInputs": {
    "default": [
      "{projectRoot}/**/*"
    ],
    "production": [
      "default",
      "!{projectRoot}/**/*.spec.ts"
    ]
  }
}
```

---

## 5. Dependency Management

### 5.1 Internal Dependencies

```json
{
  "name": "@acme/web",
  "dependencies": {
    "@acme/ui": "workspace:*",
    "@acme/utils": "workspace:*",
    "@acme/types-shared": "workspace:*"
  }
}
```

### 5.2 Shared Configuration

```typescript
// packages/config-eslint/index.js
module.exports = {
    extends: ["eslint:recommended", "plugin:@typescript-eslint/recommended"],
    parser: "@typescript-eslint/parser",
    plugins: ["@typescript-eslint"],
    rules: {
        "@typescript-eslint/no-unused-vars": "error",
    },
};

// apps/web/.eslintrc.js
module.exports = {
    root: true,
    extends: ["@acme/config-eslint"],
};
```

### 5.3 TypeScript Project References

```json
{
  "compilerOptions": {
    "composite": true,
    "declaration": true,
    "declarationMap": true
  },
  "references": [
    {
      "path": "../packages/ui"
    },
    {
      "path": "../packages/utils"
    }
  ]
}
```

---

## 6. CI/CD Patterns

### 6.1 Affected-Only Builds

```yaml
# GitHub Actions with Nx
name: CI
on: [ push, pull_request ]

jobs:
  main:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install

      - uses: nrwl/nx-set-shas@v4

      - run: pnpm nx affected -t lint test build
```

### 6.2 Turborepo with Remote Cache

```yaml
name: CI
on: [ push, pull_request ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - run: pnpm install

      - run: pnpm turbo run build test lint
        env:
          TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
          TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

### 6.3 Selective Deployment

```yaml
deploy-web:
  needs: build
  if: contains(github.event.head_commit.modified, 'apps/web/') ||
    contains(github.event.head_commit.modified, 'packages/')
  runs-on: ubuntu-latest
  steps:
    - run: pnpm --filter @acme/web deploy
```

---

## 7. Common Tasks

| Task                  | Command                                            |
|-----------------------|----------------------------------------------------|
| **Install all**       | `pnpm install`                                     |
| **Build all**         | `pnpm turbo build`                                 |
| **Build affected**    | `pnpm nx affected -t build`                        |
| **Test single**       | `pnpm --filter @acme/web test`                     |
| **Add dependency**    | `pnpm --filter @acme/web add lodash`               |
| **Add workspace dep** | `pnpm --filter @acme/web add @acme/ui@workspace:*` |
| **Run dev**           | `pnpm turbo dev --filter @acme/web`                |
| **Lint all**          | `pnpm turbo lint`                                  |
| **Graph**             | `pnpm nx graph`                                    |

### 7.1 Creating New Package

```bash
# Create package directory
mkdir -p packages/new-lib/src

# Initialize package.json
cd packages/new-lib
pnpm init

# Update package.json
{
  "name": "@acme/new-lib",
  "version": "0.0.0",
  "main": "./dist/index.js",
  "types": "./dist/index.d.ts",
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts",
    "dev": "tsup src/index.ts --format cjs,esm --dts --watch"
  }
}
```

### 7.2 Package Checklist

| Item                             | Status |
|----------------------------------|--------|
| ☐ Package.json with correct name |        |
| ☐ TypeScript configuration       |        |
| ☐ Build script                   |        |
| ☐ ESLint configuration           |        |
| ☐ Test setup                     |        |
| ☐ README.md                      |        |
| ☐ Export in index.ts             |        |

---

## 8. Autonomy Calibration

| Task Type                    | Level | Notes                    |
|------------------------------|-------|--------------------------|
| Add code to existing package | L4    | Follow existing patterns |
| Create new package           | L3    | Review structure         |
| Modify shared config         | L2-L3 | Affects all packages     |
| Update root dependencies     | L2    | Version compatibility    |
| Change build pipeline        | L2    | CI/CD impact             |
| Restructure packages         | L1-L2 | Breaking changes         |
| Update tooling (Nx/Turbo)    | L2    | Compatibility check      |

---

## Pitfalls to Avoid

| Pitfall                   | Solution                            |
|---------------------------|-------------------------------------|
| **Circular dependencies** | Use dependency graph tools          |
| **Version drift**         | Single version policy               |
| **Slow CI**               | Use affected commands, remote cache |
| **Large node_modules**    | Use pnpm, shared hoisting           |
| **Unclear ownership**     | CODEOWNERS file                     |

---

## Related

- `guidelines/engineering.md` — Engineering practices
- `practices/documentation/project_directory_structure.md` — Directory patterns
- `guidelines/typescript.md` — TypeScript guidelines

---

*Part of SAGE Knowledge Base*

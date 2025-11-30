# TypeScript Guidelines

> TypeScript and JavaScript development standards

---

## Table of Contents

- [1. Core Principles](#1-core-principles)
- [2. Naming Conventions](#2-naming-conventions)
- [3. File Conventions](#3-file-conventions)
- [4. Type Guidelines](#4-type-guidelines)
- [5. Tooling](#5-tooling)
- [6. Quick Checklist](#6-quick-checklist)

---

## 1. Core Principles

| Principle        | Description                               |
|------------------|-------------------------------------------|
| **Type Safety**  | Leverage TypeScript's type system fully   |
| **Immutability** | Prefer immutable data structures          |
| **Functional**   | Use functional patterns where appropriate |
| **Explicit**     | Be explicit over implicit                 |

---

## 2. Naming Conventions

| Element    | Convention                   | Example           |
|------------|------------------------------|-------------------|
| Variables  | `camelCase`                  | `userName`        |
| Constants  | `UPPER_SNAKE_CASE`           | `MAX_RETRIES`     |
| Functions  | `camelCase`                  | `getUserById`     |
| Classes    | `PascalCase`                 | `UserService`     |
| Interfaces | `PascalCase`                 | `UserRepository`  |
| Types      | `PascalCase`                 | `UserStatus`      |
| Enums      | `PascalCase`                 | `HttpStatus`      |
| Generics   | `T`, `K`, `V` or descriptive | `TData`, `TError` |

---

## 3. File Conventions

| Element    | Convention                 | Example           |
|------------|----------------------------|-------------------|
| Components | `PascalCase.tsx`           | `UserProfile.tsx` |
| Utilities  | `camelCase.ts`             | `formatDate.ts`   |
| Types      | `types.ts` or `*.types.ts` | `user.types.ts`   |
| Constants  | `constants.ts`             | `constants.ts`    |
| Hooks      | `use*.ts`                  | `useAuth.ts`      |
| Tests      | `*.test.ts` / `*.spec.ts`  | `user.test.ts`    |

---

## 4. Type Guidelines

### When to Use Interface vs Type

| Use Case              | Recommendation |
|-----------------------|----------------|
| Object shapes         | `interface`    |
| Union types           | `type`         |
| Intersection types    | `type`         |
| Function types        | `type`         |
| Extending objects     | `interface`    |
| Mapped/conditional    | `type`         |

### Type Safety Rules

| Rule                    | Description                    |
|-------------------------|--------------------------------|
| Avoid `any`             | Use `unknown` instead          |
| Explicit return types   | For public/exported functions  |
| Strict null checks      | Handle null/undefined properly |
| Type guards             | For runtime type narrowing     |

### Common Utility Types

| Type          | Purpose                    |
|---------------|----------------------------|
| `Partial<T>`  | All properties optional    |
| `Required<T>` | All properties required    |
| `Pick<T, K>`  | Select specific properties |
| `Omit<T, K>`  | Exclude properties         |
| `Record<K,V>` | Key-value mapping          |
| `ReturnType`  | Extract function return    |

---

## 5. Tooling

### ESLint Configuration

```json
{
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
    "plugin:react-hooks/recommended"
  ],
  "rules": {
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/no-explicit-any": "error"
  }
}
```

### TSConfig Essentials

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "moduleResolution": "bundler",
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

---

## 6. Quick Checklist

### Code Quality

| Check                   | Description                    |
|-------------------------|--------------------------------|
| ☐ No `any` types        | Use `unknown` or proper types  |
| ☐ Strict mode enabled   | `"strict": true` in tsconfig   |
| ☐ Return types explicit | For public functions           |
| ☐ Null checks           | Handle null/undefined properly |
| ☐ Tests typed           | Test files also type-safe      |

### React Specific

| Check                   | Description                    |
|-------------------------|--------------------------------|
| ☐ Props interface       | Define props with interface    |
| ☐ Event types           | Use proper event types         |
| ☐ Hook dependencies     | Correct useEffect dependencies |
| ☐ Children typed        | Use `React.ReactNode`          |

### Testing

| Check                   | Description                    |
|-------------------------|--------------------------------|
| ☐ Type-safe mocks       | Mock functions properly typed  |
| ☐ Test utilities typed  | render, screen, etc.           |
| ☐ Assertions typed      | expect() with correct types    |

---

## Related

- `.knowledge/practices/engineering/languages/TYPESCRIPT_PATTERNS.md` — Type patterns, React patterns, and implementations
- `.knowledge/guidelines/CODE_STYLE.md` — General code style
- `.knowledge/practices/engineering/quality/TESTING_STRATEGY.md` — Testing practices
- `.knowledge/scenarios/typescript_frontend/CONTEXT.md` — Frontend scenario

---

*AI Collaboration Knowledge Base*

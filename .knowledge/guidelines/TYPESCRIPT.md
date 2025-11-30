# TypeScript Guidelines

> TypeScript and JavaScript development standards

---

## Table of Contents

- [1. Overview](#1-overview)
- [2. Type System](#2-type-system)
- [3. Code Style](#3-code-style)
- [4. Patterns](#4-patterns)
- [5. React Patterns](#5-react-patterns)
- [6. Testing](#6-testing)
- [7. Tooling](#7-tooling)

---

## 1. Overview

### 1.1 Core Principles

| Principle        | Description                               |
|------------------|-------------------------------------------|
| **Type Safety**  | Leverage TypeScript's type system fully   |
| **Immutability** | Prefer immutable data structures          |
| **Functional**   | Use functional patterns where appropriate |
| **Explicit**     | Be explicit over implicit                 |

### 1.2 File Conventions

| Element    | Convention                 | Example           |
|------------|----------------------------|-------------------|
| Components | `PascalCase.tsx`           | `UserProfile.tsx` |
| Utilities  | `camelCase.ts`             | `formatDate.ts`   |
| Types      | `types.ts` or `*.types.ts` | `user.types.ts`   |
| Constants  | `UPPER_SNAKE_CASE`         | `API_BASE_URL`    |
| Hooks      | `use*.ts`                  | `useAuth.ts`      |

---

## 2. Type System

### 2.1 Type Definitions

```typescript
// ✅ Good - Use interface for objects
interface User {
    id: string;
    name: string;
    email: string;
    createdAt: Date;
}

// ✅ Good - Use type for unions/intersections
type Status = 'pending' | 'active' | 'inactive';
type UserWithStatus = User & { status: Status };

// ❌ Avoid - any type
function process(data: any) {
}

// ✅ Good - Use unknown for truly unknown types
function process(data: unknown) {
    if (isUser(data)) {
        // data is now typed as User
    }
}
```
### 2.2 Generics

```typescript
// ✅ Good - Generic function
function getFirst<T>(items: T[]): T | undefined {
    return items[0];
}

// ✅ Good - Constrained generic
function getProperty<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

// ✅ Good - Generic interface
interface ApiResponse<T> {
    data: T;
    status: number;
    message: string;
}
```
### 2.3 Utility Types

```typescript
// Partial - all properties optional
type PartialUser = Partial<User>;

// Required - all properties required
type RequiredUser = Required<User>;

// Pick - select properties
type UserName = Pick<User, 'id' | 'name'>;

// Omit - exclude properties
type UserWithoutEmail = Omit<User, 'email'>;

// Record - key-value mapping
type UserMap = Record<string, User>;

// ReturnType - function return type
type CreateUserReturn = ReturnType<typeof createUser>;
```
### 2.4 Type Guards

```typescript
// Type guard function
function isUser(value: unknown): value is User {
    return (
        typeof value === 'object' &&
        value !== null &&
        'id' in value &&
        'name' in value
    );
}

// Discriminated union
type Result<T> =
    | { success: true; data: T }
    | { success: false; error: string };

function handleResult<T>(result: Result<T>) {
    if (result.success) {
        // result.data is available
        console.log(result.data);
    } else {
        // result.error is available
        console.error(result.error);
    }
}
```
---

## 3. Code Style

### 3.1 Naming Conventions

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

### 3.2 Function Style

```typescript
// ✅ Good - Arrow function for callbacks
const users = data.map((item) => item.name);

// ✅ Good - Named function for top-level
function calculateTotal(items: Item[]): number {
    return items.reduce((sum, item) => sum + item.price, 0);
}

// ✅ Good - Explicit return type for public API
export function fetchUser(id: string): Promise<User> {
    return api.get(`/users/${id}`);
}

// ✅ Good - Default parameters
function greet(name: string, greeting = 'Hello'): string {
    return `${greeting}, ${name}!`;
}
```
### 3.3 Object and Array Patterns

```typescript
// ✅ Good - Destructuring
const {name, email} = user;
const [first, ...rest] = items;

// ✅ Good - Spread operator
const updatedUser = {...user, name: 'New Name'};
const allItems = [...items1, ...items2];

// ✅ Good - Object shorthand
const user = {name, email, age};

// ✅ Good - Computed property names
const key = 'dynamicKey';
const obj = {[key]: value};
```
### 3.4 Null Handling

```typescript
// ✅ Good - Optional chaining
const name = user?.profile?.name;

// ✅ Good - Nullish coalescing
const displayName = user.name ?? 'Anonymous';

// ✅ Good - Non-null assertion (only when certain)
const element = document.getElementById('app')!;

// ✅ Good - Type narrowing
function processValue(value: string | null) {
    if (value === null) {
        return 'default';
    }
    return value.toUpperCase();
}
```
---

## 4. Patterns

### 4.1 Error Handling

```typescript
// Custom error class
class AppError extends Error {
    constructor(
        message: string,
        public code: string,
        public statusCode: number = 500
    ) {
        super(message);
        this.name = 'AppError';
    }
}

// Result pattern
type Result<T, E = Error> =
    | { ok: true; value: T }
    | { ok: false; error: E };

async function fetchData<T>(url: string): Promise<Result<T>> {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return {ok: true, value: data};
    } catch (error) {
        return {ok: false, error: error as Error};
    }
}
```
### 4.2 Async Patterns

```typescript
// ✅ Good - Async/await
async function getUser(id: string): Promise<User> {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
        throw new AppError('User not found', 'USER_NOT_FOUND', 404);
    }
    return response.json();
}

// ✅ Good - Parallel execution
async function fetchAll(ids: string[]): Promise<User[]> {
    const promises = ids.map(id => getUser(id));
    return Promise.all(promises);
}

// ✅ Good - Error handling in async
async function safeGetUser(id: string): Promise<User | null> {
    try {
        return await getUser(id);
    } catch {
        return null;
    }
}
```
### 4.3 Module Organization

```typescript
// user/index.ts - barrel export
export {User, UserStatus} from './types';
export {UserService} from './service';
export {useUser} from './hooks';

// user/types.ts
export interface User {
    id: string;
    name: string;
}

export type UserStatus = 'active' | 'inactive';

// user/service.ts
export class UserService {
    async getById(id: string): Promise<User> {
    }
}
```
---

## 5. React Patterns

### 5.1 Component Types

```typescript
// Function component with props
interface ButtonProps {
    label: string;
    onClick: () => void;
    variant?: 'primary' | 'secondary';
    disabled?: boolean;
}

export function Button({
                           label,
                           onClick,
                           variant = 'primary',
                           disabled = false
                       }: ButtonProps) {
    return (
        <button
            className = {`btn btn-${variant}`
}
    onClick = {onClick}
    disabled = {disabled}
        >
        {label}
        < /button>
)
    ;
}

// Component with children
interface CardProps {
    title: string;
    children: React.ReactNode;
}

export function Card({title, children}: CardProps) {
    return (
        <div className = "card" >
            <h2>{title} < /h2>
    {
        children
    }
    </div>
)
    ;
}
```
### 5.2 Hooks

```typescript
// Custom hook with TypeScript
function useLocalStorage<T>(
    key: string,
    initialValue: T
): [T, (value: T) => void] {
    const [storedValue, setStoredValue] = useState<T>(() => {
        try {
            const item = localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch {
            return initialValue;
        }
    });

    const setValue = (value: T) => {
        setStoredValue(value);
        localStorage.setItem(key, JSON.stringify(value));
    };

    return [storedValue, setValue];
}

// Usage
const [user, setUser] = useLocalStorage<User | null>('user', null);
```
### 5.3 State Management

```typescript
// Reducer pattern
interface State {
    users: User[];
    loading: boolean;
    error: string | null;
}

type Action =
    | { type: 'FETCH_START' }
    | { type: 'FETCH_SUCCESS'; payload: User[] }
    | { type: 'FETCH_ERROR'; payload: string };

function reducer(state: State, action: Action): State {
    switch (action.type) {
        case 'FETCH_START':
            return {...state, loading: true, error: null};
        case 'FETCH_SUCCESS':
            return {...state, loading: false, users: action.payload};
        case 'FETCH_ERROR':
            return {...state, loading: false, error: action.payload};
        default:
            return state;
    }
}
```
---

## 6. Testing

### 6.1 Unit Tests

```typescript
// user.test.ts
import {describe, it, expect, vi} from 'vitest';
import {UserService} from './service';

describe('UserService', () => {
    it('should fetch user by id', async () => {
        const service = new UserService();
        const user = await service.getById('123');

        expect(user).toBeDefined();
        expect(user.id).toBe('123');
    });

    it('should throw on invalid id', async () => {
        const service = new UserService();

        await expect(service.getById('')).rejects.toThrow('Invalid ID');
    });
});
```
### 6.2 Component Tests

```typescript
// Button.test.tsx
import {render, screen, fireEvent} from '@testing-library/react';
import {Button} from './Button';

describe('Button', () => {
    it('renders with label', () => {
        render(<Button label = "Click me"
        onClick = {()
    =>
        {
        }
    }
        />);

        expect(screen.getByText('Click me')).toBeInTheDocument();
    });

    it('calls onClick when clicked', () => {
        const handleClick = vi.fn();
        render(<Button label = "Click"
        onClick = {handleClick}
        />);

        fireEvent.click(screen.getByText('Click'));

        expect(handleClick).toHaveBeenCalledTimes(1);
    });
});
```
### 6.3 Mock Patterns

```typescript
// Mocking modules
vi.mock('./api', () => ({
    fetchUser: vi.fn().mockResolvedValue({id: '1', name: 'Test'}),
}));

// Mocking hooks
vi.mock('./useAuth', () => ({
    useAuth: () => ({user: mockUser, isAuthenticated: true}),
}));

// Type-safe mocks
const mockFetch = vi.fn<[string], Promise<User>>();
mockFetch.mockResolvedValue({id: '1', name: 'Test'});
```
---

## 7. Tooling

### 7.1 ESLint Configuration

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
### 7.2 TSConfig

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
### 7.3 Quick Checklist

| Check                   | Description                    |
|-------------------------|--------------------------------|
| ☐ No `any` types        | Use `unknown` or proper types  |
| ☐ Strict mode enabled   | `"strict": true` in tsconfig   |
| ☐ Return types explicit | For public functions           |
| ☐ Null checks           | Handle null/undefined properly |
| ☐ Tests typed           | Test files also type-safe      |

---

## Related

- `.knowledge/guidelines/CODE_STYLE.md` — General code style
- `.knowledge/practices/engineering/TESTING_STRATEGY.md` — Testing practices
- `.knowledge/scenarios/typescript_frontend/CONTEXT.md` — Frontend scenario

---

*AI Collaboration Knowledge Base*

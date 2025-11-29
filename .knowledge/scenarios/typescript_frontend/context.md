---
version: "1.0"
last_updated: "2025-11-30"
status: published
tokens: ~2200
---

# TypeScript Frontend Scenario Context

> Pre-configured context for TypeScript frontend development (React/Vue)

---

## Table of Contents

- [1. Scenario Profile](#1-scenario-profile)
- [2. Relevant Knowledge](#2-relevant-knowledge)
- [3. Project Structure](#3-project-structure-react)
- [4. Common Patterns](#4-common-patterns)
- [5. Testing Patterns](#5-testing-patterns)
- [6. State Management](#6-state-management)
- [7. Common Tasks](#7-common-tasks)
- [8. Autonomy Calibration](#8-autonomy-calibration)
- [9. Quick Commands](#9-quick-commands)

---

## 1. Scenario Profile

```yaml
scenario: typescript_frontend
languages: [ typescript, javascript ]
frameworks: [ react, vue, next.js, nuxt ]
focus: [ components, state, testing, styling ]
autonomy_default: L3
```

---

## 2. Relevant Knowledge

| Priority      | Files                                                                                   |
|---------------|-----------------------------------------------------------------------------------------|
| **Auto-Load** | `core/principles.md` · `.knowledge/guidelines/code_style.md` · `.knowledge/practices/engineering/patterns.md` |
| **On-Demand** | `.knowledge/guidelines/engineering.md` · `.knowledge/practices/engineering/testing_strategy.md`               |

---

## 3. Project Structure (React)

| Directory         | Purpose                     |
|-------------------|-----------------------------|
| `src/components/` | Reusable UI components      |
| `src/pages/`      | Page components (routing)   |
| `src/hooks/`      | Custom React hooks          |
| `src/contexts/`   | React Context providers     |
| `src/services/`   | API client services         |
| `src/utils/`      | Utility functions           |
| `src/types/`      | TypeScript type definitions |
| `src/styles/`     | Global styles, themes       |
| `src/__tests__/`  | Test files                  |
| `public/`         | Static assets               |

---

## 4. Common Patterns

### 4.1 Component Pattern

```typescript
import {FC, useState, useCallback} from 'react';

interface UserCardProps {
    user: User;
    onSelect?: (id: string) => void;
}

export const UserCard: FC<UserCardProps> = ({user, onSelect}) => {
    const [isExpanded, setIsExpanded] = useState(false);

    const handleClick = useCallback(() => {
        setIsExpanded((prev) => !prev);
        onSelect?.(user.id);
    }, [user.id, onSelect]);

    return (
        <div className = "user-card"
    onClick = {handleClick} >
        <h3>{user.name} < /h3>
    {
        isExpanded && <p>{user.bio} < /p>}
        < /div>
    )
        ;
    }
    ;
```

### 4.2 Custom Hook Pattern

```typescript
import {useState, useEffect} from 'react';

interface UseFetchResult<T> {
    data: T | null;
    loading: boolean;
    error: Error | null;
}

export function useFetch<T>(url: string): UseFetchResult<T> {
    const [data, setData] = useState<T | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<Error | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const response = await fetch(url);
                if (!response.ok) throw new Error('Fetch failed');
                setData(await response.json());
            } catch (err) {
                setError(err instanceof Error ? err : new Error('Unknown error'));
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [url]);

    return {data, loading, error};
}
```

### 4.3 Context Pattern

```typescript
import {createContext, useContext, ReactNode, useState} from 'react';

interface AuthContextType {
    user: User | null;
    login: (credentials: Credentials) => Promise<void>;
    logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({children}: { children: ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);

    const login = async (credentials: Credentials) => {
        const user = await authService.login(credentials);
        setUser(user);
    };

    const logout = () => setUser(null);

    return (
        <AuthContext.Provider value = {
    {
        user, login, logout
    }
}>
    {
        children
    }
    </AuthContext.Provider>
)
    ;
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) throw new Error('useAuth must be within AuthProvider');
    return context;
};
```

---

## 5. Testing Patterns

### 5.1 Component Testing

```typescript
import {render, screen, fireEvent} from '@testing-library/react';
import {UserCard} from './UserCard';

describe('UserCard', () => {
    const mockUser = {id: '1', name: 'John', bio: 'Developer'};

    it('renders user name', () => {
        render(<UserCard user = {mockUser}
        />);
        expect(screen.getByText('John')).toBeInTheDocument();
    });

    it('expands on click', () => {
        render(<UserCard user = {mockUser}
        />);
        fireEvent.click(screen.getByText('John'));
        expect(screen.getByText('Developer')).toBeInTheDocument();
    });

    it('calls onSelect with user id', () => {
        const onSelect = jest.fn();
        render(<UserCard user = {mockUser}
        onSelect = {onSelect}
        />);
        fireEvent.click(screen.getByText('John'));
        expect(onSelect).toHaveBeenCalledWith('1');
    });
});
```

### 5.2 Hook Testing

```typescript
import {renderHook, waitFor} from '@testing-library/react';
import {useFetch} from './useFetch';

describe('useFetch', () => {
    it('fetches data successfully', async () => {
        global.fetch = jest.fn().mockResolvedValue({
            ok: true,
            json: () => Promise.resolve({name: 'Test'}),
        });

        const {result} = renderHook(() => useFetch('/api/data'));

        await waitFor(() => {
            expect(result.current.loading).toBe(false);
        });

        expect(result.current.data).toEqual({name: 'Test'});
        expect(result.current.error).toBeNull();
    });
});
```

---

## 6. State Management

### 6.1 Local State

| Pattern      | Use Case                 |
|--------------|--------------------------|
| `useState`   | Simple component state   |
| `useReducer` | Complex state logic      |
| `useRef`     | Mutable values, DOM refs |

### 6.2 Global State Options

| Library           | Best For                  |
|-------------------|---------------------------|
| Context + Reducer | Small-medium apps         |
| Zustand           | Simple global state       |
| Redux Toolkit     | Large apps, complex state |
| Jotai/Recoil      | Atomic state management   |
| TanStack Query    | Server state              |

---

## 7. Common Tasks

| Task                 | Steps                                                       |
|----------------------|-------------------------------------------------------------|
| **Add Component**    | Create file → Define types → Implement → Add tests → Export |
| **Add Route**        | Create page → Update router → Add navigation                |
| **Add API Call**     | Define types → Create service → Use in hook/component       |
| **Add Global State** | Create context/store → Add provider → Use hook              |

---

## 8. Autonomy Calibration

| Task Type                | Level | Notes                      |
|--------------------------|-------|----------------------------|
| New component (standard) | L3-L4 | Follow existing patterns   |
| Styling changes          | L4    | Low risk                   |
| State management changes | L2-L3 | Review architecture impact |
| Add new dependency       | L2    | Discuss bundle size        |
| Refactoring              | L3    | Checkpoint at plan         |
| Test writing             | L4    | Execute and report         |
| Breaking API changes     | L1-L2 | Full review required       |

---

## 9. Quick Commands

| Category  | Commands                                                    |
|-----------|-------------------------------------------------------------|
| **Dev**   | `npm run dev` · `npm start`                                 |
| **Build** | `npm run build` · `npm run preview`                         |
| **Test**  | `npm test` · `npm run test:coverage` · `npm run test:watch` |
| **Lint**  | `npm run lint` · `npm run lint:fix` · `npm run typecheck`   |
| **Deps**  | `npm install` · `npm update` · `npm audit`                  |

---

## Related

- `.knowledge/guidelines/code_style.md` — Code style guidelines
- `.knowledge/practices/engineering/patterns.md` — Design patterns
- `.knowledge/practices/engineering/testing_strategy.md` — Testing strategies
- `.knowledge/frameworks/autonomy/levels.md` — Autonomy framework

---

*Part of SAGE Knowledge Base*

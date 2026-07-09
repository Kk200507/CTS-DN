# Global State Management

Global state management allows components across different parts of a Single Page Application (SPA) to share data, track UI modes, cache API responses, and synchronize changes without prop-drilling.

---

## 1. Redux (React)

Redux implements a strict **unidirectional data flow** based on a single immutable global state store.

### Key Concepts:
* **Store**: Holds the global state object.
* **Actions**: Plain JavaScript objects carrying type identifiers and data payloads. They express *what* happened.
* **Reducers**: Pure functions that receive the current state and an action, then calculate and return a *new* state object.
* **Selectors**: Selector functions extract specific segments of data from the store to optimize rendering performance.

```text
       [ UI View Component ] ───► (Dispatches) ───► [ Action ]
               ▲                                         │
               │                                         ▼
         (Selector updates)                       [ Reducer Function ]
               │                                         │
               └─────────── [ Store State ] ◄────────────┘
                              (Updated)
```

### Redux Code Example:
```javascript
// 1. Action Type
const ADD_ITEM = "cart/addItem";

// 2. Action Creator
export const addItem = (item) => ({
    type: ADD_ITEM,
    payload: item
});

// 3. Initial State
const initialState = {
    items: []
};

// 4. Reducer (Must be a pure function: no API calls, no mutating variables)
export function cartReducer(state = initialState, action) {
    switch (action.type) {
        case ADD_ITEM:
            return {
                ...state,
                items: [...state.items, action.payload] // Returns new array reference
            };
        default:
            return state;
    }
}
```

---

## 2. NgRx (Angular)

NgRx adapts the Redux architecture to Angular, utilizing **RxJS streams** and reactive pipelines.

### Key Concepts:
* **Actions**: Define unique events dispatched from components.
* **Reducers**: Pure functions altering the state.
* **Selectors**: Observables that components subscribe to for reactive updates.
* **Effects**: Listen for actions, trigger side effects (like async HTTP calls), and dispatch new actions on success/failure.

### NgRx Code Example:
```typescript
import { createAction, props, createReducer, on } from '@ngrx/store';

// 1. Actions
export const loadCourses = createAction('[Course List] Load Courses');
export const loadCoursesSuccess = createAction(
  '[Course API] Load Success',
  props<{ courses: any[] }>()
);

// 2. Reducer
export interface State {
  courses: any[];
}
const initialState: State = { courses: [] };

export const courseReducer = createReducer(
  initialState,
  on(loadCoursesSuccess, (state, { courses }) => ({
    ...state,
    courses: courses
  }))
);
```

---

## 3. Pinia (Vue)

Pinia is Vue 3's official modern state library. It leverages Vue's native **Reactivity System** (`ref`, `reactive`), making store creation simpler than traditional Redux boilerplate.

### Key Concepts:
* **State**: The data source (defined as a function returning a reactive object).
* **Getters**: Computed properties that cache derived values.
* **Actions**: Functions containing business logic, mutations, or asynchronous queries (no separate "reducers" needed).

### Pinia Code Example:
```javascript
import { defineStore } from 'pinia';

export const useUserStore = defineStore('user', {
  // State: Equivalent to ref()
  state: () => ({
    username: 'Guest_User',
    isLoggedIn: false
  }),
  
  // Getters: Equivalent to computed()
  getters: {
    welcomeMessage: (state) => `Welcome back, ${state.username}!`
  },
  
  // Actions: Directly mutates state (sync or async)
  actions: {
    login(newUsername) {
      this.username = newUsername;
      this.isLoggedIn = true;
    },
    logout() {
      this.username = 'Guest_User';
      this.isLoggedIn = false;
    }
  }
});
```

---

## 4. Comparison: Redux vs. NgRx vs. Pinia

| Feature | Redux | NgRx | Pinia |
| :--- | :--- | :--- | :--- |
| **Framework** | Primarily React (can be used anywhere) | Angular only | Vue only |
| **Data Paradigm** | Immutable (Must return new references) | Immutable (Uses RxJS streams) | Mutable Reactivity (Vue wraps object proxies) |
| **Boilerplate** | High (Actions, Reducers, Types) | High (Actions, Reducers, Effects) | Low (Pure state, getters, actions) |
| **Async Logic** | Middleware (Redux Thunk, Saga) | Effects (RxJS streams) | Actions handle async natively (async/await) |
| **Typical Target** | Medium to large complex apps | Large scale enterprise architectures | Simple to complex SPA apps |

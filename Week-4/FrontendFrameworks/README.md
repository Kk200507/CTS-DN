# Frontend Frameworks

This directory contains representative demonstrations for the three major modern frontend frameworks: **React.js**, **Angular**, and **Vue.js**.

---

## Architectural Comparison

| Feature | React.js | Angular | Vue.js |
| :--- | :--- | :--- | :--- |
| **Type** | UI Library | Full-blown Framework | Progressive Framework |
| **Creator** | Meta (Facebook) | Google | Evan You (Community-driven) |
| **Architecture** | Component-based (Virtual DOM) | Component-based (Incremental DOM) | Component-based (Virtual DOM) |
| **Programming Lang**| JavaScript / JSX | TypeScript | JavaScript or TypeScript |
| **Data Binding** | One-way (explicit state updates) | Two-way (automatic sync) | Two-way (automatic sync) |
| **State Management**| Context, Redux, Zustand | Services, RxJS, NgRx | Reactive Refs, Pinia |
| **Learning Curve** | Moderate | Steep (Requires TypeScript/RxJS) | Gentle (HTML-like template templates) |

---

## Files in this Directory

### 1. [react_demo.jsx](file:///c:/Personal/Projects/CTS-DN/Week-4/FrontendFrameworks/react_demo.jsx)
- **Concepts**: JSX syntax, Class-Based vs. Functional Components, Props passing, hooks (`useState`, `useEffect`, `useContext`), client routing, and state stores.
- **Philosophy**: "Learn once, write anywhere." Highly modular library focusing on building reusable visual components.

### 2. [angular_demo.ts](file:///c:/Personal/Projects/CTS-DN/Week-4/FrontendFrameworks/angular_demo.ts)
- **Concepts**: TypeScript types, Component structure with annotations (`@Component`), modules (`@NgModule`), Dependency Injection (`@Injectable`), RxJS Streams/Observables, Reactive Forms, and network queries (`HttpClient`).
- **Philosophy**: Opinionated, robust, and batteries-included enterprise ecosystem. All projects follow the exact same structure.

### 3. [vue_demo.html](file:///c:/Personal/Projects/CTS-DN/Week-4/FrontendFrameworks/vue_demo.html)
- **Concepts**: Self-contained Vue 3 application importing via CDN. Showcases template bindings (`v-model`, `v-for`), Vue Composition API (`ref`, `reactive`, `computed`), component declarations, Vue Router, and Pinia global stores.
- **Philosophy**: Easy integration. Starts as a lightweight template-driven view layer, but can scale up to support enterprise SPAs.

# Week 4: Modern Frontend Development

Welcome to Week 4 of the Python Full Stack Engineer (Python FSE) learning path. This week shifts focus from backend systems to the frontend, examining the building blocks of web interfaces (HTML5, CSS3, ES6+), modern JavaScript frameworks (React, Angular, Vue), responsive and accessible design standards, cross-browser compatibility, and API integrations with state management.

## Overview

A Python Full Stack Engineer must be comfortable designing and building frontend architectures that connect seamlessly with backend web APIs. This week's curriculum covers:
1. **Web Foundations**: Semantic markup, styling layouts with Flexbox and Grid, and modern JavaScript (ES6+).
2. **Frontend Frameworks**: In-depth comparisons and implementation demonstrations using React, Angular, and Vue.
3. **Web Design Standards**: Practical approaches to responsive layouts, accessibility (WCAG/ARIA), and ensuring compatibility across browser engines.
4. **API Integration & State Management**: How Single Page Applications (SPAs) fetch data, handle client-side errors, and manage global state.

---

## Folder Structure

```text
Week-4/
├── README.md                           # Week 4 overview and learning outcomes
├── WebFoundations/
│   ├── README.md                       # Introduction to HTML5, CSS3, and ES6+
│   ├── semantic_html.html              # HTML5 semantic structure demonstration
│   ├── css_layout.html                 # Flexbox vs. Grid styling layout guide
│   └── modern_javascript.js            # Scoping, arrows, promises, modules (ES6+)
├── FrontendFrameworks/
│   ├── README.md                       # High-level React vs. Angular vs. Vue comparison
│   ├── react_demo.jsx                  # JSX, functional components, hooks, router
│   ├── angular_demo.ts                 # TypeScript, modules, RxJS, forms, HttpClient
│   └── vue_demo.html                   # CDN-based Vue 3 template syntax, reactivity, Pinia
├── WebDesignStandards/
│   ├── README.md                       # Standards overview
│   ├── responsive_design.html          # Mobile First, Media Queries, Container Queries
│   ├── web_accessibility.md            # WCAG, ARIA roles, focus state, keyboard navigation
│   └── cross_browser_compatibility.md # Browser engines, feature detection, polyfills
└── APIStateManagement/
    ├── README.md                       # API connection concepts
    ├── api_integration.js              # Fetch API vs. Axios, interceptors, error handling
    └── state_management.md             # Store architectures (Redux vs. NgRx vs. Pinia)
```

---

## Topics Covered

### 1. Web Foundations
* Document structure using semantic HTML5 elements.
* Responsive layouts using CSS Flexbox and CSS Grid.
* Modern ES6+ syntax (scoping, arrow functions, promises, async/await, modules).

### 2. Frontend Frameworks & Single Page Applications (SPAs)
* **React.js**: JSX syntax, components, props, hooks (`useState`, `useEffect`, `useContext`), routing, and state.
* **Angular**: TypeScript foundation, modules, dependency injection, RxJS observables, reactive forms, and `HttpClient`.
* **Vue.js**: Reactive variables (`ref`, `reactive`), Composition API, Directives (`v-if`, `v-for`, `v-model`), and routing.

### 3. Modern Design Standards & Web Accessibility (a11y)
* Responsive styling techniques (Viewport units, Media queries, Container queries).
* Accessibility compliance: semantic structure, keyboard navigation, focus trap, and ARIA roles.
* Cross-browser practices: browser engines, feature detection, vendor prefixes, and polyfills.

### 4. Client-Side Data Integration
* Interfacing APIs using standard Fetch API and advanced Axios clients.
* Handling HTTP status errors gracefully on the client.
* Global state stores: Redux (React), NgRx (Angular), and Pinia (Vue).

---

## Learning Outcomes

By the end of this week, you will be able to:
- Write semantic, accessible markup that works across screen readers and keyboard-only users.
- Apply Flexbox and Grid to design complex layouts without relying on CSS frameworks.
- Understand and compare the structural differences and architectures of React, Angular, and Vue.
- Build reactive views that handle data binds, props, dynamic lists, and client routes.
- Execute network requests, use interceptors for credentials, and manage application errors.
- Structure global state stores, separating concerns via actions, reducers, and selectors.

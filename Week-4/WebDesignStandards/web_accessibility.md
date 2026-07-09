# Web Accessibility (a11y) Guidelines

Web accessibility ensures that websites and applications are designed and coded so that people with disabilities can use them. This document details the standards, practices, and guidelines for building accessible web platforms.

---

## 1. WCAG 2.1 Guidelines (POUR)

The **Web Content Accessibility Guidelines (WCAG)** are built upon four fundamental principles known as **POUR**:

* **Perceivable**: Information and user interface components must be presentable to users in ways they can perceive (it cannot be invisible to all of their senses).
  - *Example*: Provide text alternatives (alt text) for images, captions for video, and adequate color contrast.
* **Operable**: User interface components and navigation must be operable (users must be able to perform the actions).
  - *Example*: Ensure all functionality is available from a keyboard, allow users enough time to read content, and avoid causing seizures (no rapid flashing).
* **Understandable**: Information and the operation of the user interface must be understandable.
  - *Example*: Make text readable and predictable, and help users avoid and correct input mistakes.
* **Robust**: Content must be robust enough that it can be interpreted reliably by a wide variety of user agents, including assistive technologies.
  - *Example*: Follow clean HTML syntax standards so screen readers don't parse attributes incorrectly.

---

## 2. Semantic HTML & Landmarks

Assistive technologies (like screen readers) rely on semantic HTML tags to understand page layouts. Screen readers allow users to jump between sections using **Landmarks**.

### Layout Landmark Elements:
* `<header>` (equivalent to `role="banner"`)
* `<nav>` (equivalent to `role="navigation"`)
* `<main>` (equivalent to `role="main"`)
* `<aside>` (equivalent to `role="complementary"`)
* `<footer>` (equivalent to `role="contentinfo"`)

### Heading Hierarchy:
* Use headings (`<h1>` through `<h6>`) in sequential order to define document architecture.
* Never use multiple `<h1>` elements per page.
* Do not choose heading tags for styling purposes (use CSS classes instead).

---

## 3. ARIA (Accessible Rich Internet Applications)

When HTML tags cannot convey enough semantics (e.g. custom dropdowns or modals), **ARIA** attributes step in to fill the gaps.

> **First Rule of ARIA**: If you can use a native HTML element (e.g. `<button>`) instead of an ARIA element (e.g. `<div role="button">`), do it. Native elements have built-in accessibility.

### Crucial ARIA Attributes:
* **`role`**: Defines the type of element (e.g., `role="dialog"`, `role="tablist"`).
* **`aria-label`**: Provides a text label when there is no visible text on screen.
  - *Example*: `<button aria-label="Close modal">X</button>`
* **`aria-expanded`**: Indicates if a collapsable panel is open or closed.
  - *Example*: `<button aria-expanded="true" aria-controls="menu">Menu</button>`
* **`aria-live`**: Announces dynamically updating content (e.g. toasts, notifications) to screen readers.
  - *Example*: `<div aria-live="polite">Cart updated successfully.</div>`

---

## 4. Keyboard Navigation & Focus Management

Many users with motor disabilities navigate web apps using only a keyboard (primarily using the `Tab` key, `Shift + Tab`, and `Enter`/`Space`).

### Keyboard Access Checklist:
1. **Focus Outline**: Never remove the focus outline without providing a visible alternative.
   ```css
   /* ❌ BAD: Hides focus indicator, locking keyboard users out */
   button:focus { outline: none; }
   
   /*  GOOD: Provides highly visible focus outline */
   button:focus-visible {
       outline: 3px solid #0984e3;
       outline-offset: 2px;
   }
   ```
2. **Taborder (`tabindex`)**:
   - `tabindex="0"`: Inserts custom element into the natural keyboard tab order.
   - `tabindex="-1"`: Removes element from tab order but allows programmatic focus (useful for modals).
   - ❌ *Avoid positive tab index (`tabindex="1"`, etc.)* because it overrides natural document flow, creating confusing jumps.
3. **Keyboard Handlers**: When building custom components, listen to key events:
   ```javascript
   element.addEventListener('keydown', (event) => {
       if (event.key === 'Enter' || event.key === ' ') {
           // Execute action
       }
   });
   ```

---

## 5. Screen Readers & Assistive Output

* **Image Alt Text**: Every `<img>` tag must have an `alt` attribute.
  - If descriptive: `<img src="dog.jpg" alt="Golden retriever running in field">`
  - If decorative only: `<img src="wave.svg" alt="">` (Screen readers will skip it).
* **Screen Reader Only Text**: Use a CSS class to hide metadata visually but leave it readable for screen readers:
  ```css
  .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      border: 0;
  }
  ```

---

## 6. Color Contrast Standards

Adequate contrast ensures readability for users with low vision or color blindness.

### WCAG Contrast Ratio Requirements:

| Level | Content Type | Minimum Ratio |
| :--- | :--- | :--- |
| **AA** (Standard) | Normal Text (<18pt / 14pt bold) | **4.5:1** |
| **AA** (Standard) | Large Text (>=18pt / 14pt bold) | **3.0:1** |
| **AAA** (Enhanced) | Normal Text | **7.0:1** |
| **AAA** (Enhanced) | Large Text | **4.5:1** |

* **Color as Information**: Never rely solely on color to convey meaning.
  - ❌ *Bad*: "Fields in red are required."
  -  *Good*: "Fields marked with an asterisk (*) and colored in red are required."

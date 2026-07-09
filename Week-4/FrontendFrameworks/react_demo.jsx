/**
 * React.js Foundations & Demonstrations
 * 
 * This file contains React code illustrating:
 * 1. JSX (JavaScript XML) Syntax
 * 2. Component Structures & Props
 * 3. React Hooks (useState, useEffect, useContext)
 * 4. React Router (Client-side routing setup)
 * 5. State Management (Context API)
 */

import React, { useState, useEffect, createContext, useContext } from 'react';

// ==============================================================================
// 1. JSX (JAVASCRIPT XML) EXPLANATION
// ==============================================================================
/*
JSX is a syntax extension to JavaScript that looks similar to HTML.
It allows writing HTML-like structure directly inside JavaScript code.
Babel transpiles JSX into standard calls: React.createElement('div', null, 'Hello')

Rules of JSX:
  - Must return a single root element (or wrap in a Fragment <> ... </>)
  - Close all tags (e.g. <img />)
  - Use camelCase for attributes (class becomes className, onclick becomes onClick)
  - Embed dynamic JavaScript expressions inside curly braces: { 2 + 2 }
*/


// ==============================================================================
// 5. GLOBAL STATE MANAGEMENT: CONTEXT SETUP
// ==============================================================================
// Context provides a way to pass data through the component tree without prop-drilling.
const ThemeContext = createContext("light");


// ==============================================================================
// 2. COMPONENTS & PROPS
// ==============================================================================

// Card Component receiving 'title' and 'subtitle' as parameters (PROPS)
// Props are read-only inputs passed from parent components.
export function CourseCard({ title, duration, children }) {
    return (
        <div className="course-card" style={{ border: '1px solid #ccc', padding: '16px', margin: '8px' }}>
            <h3>{title}</h3>
            <p><strong>Duration:</strong> {duration}</p>
            {/* children represents any HTML or components passed inside tags */}
            <div className="card-body">{children}</div>
        </div>
    );
}


// ==============================================================================
// 3. REACT HOOKS (useState, useEffect, useContext)
// ==============================================================================

export function CounterComponent() {
    // useState: Declares a state variable. Returns [currentVal, setterFunction]
    const [count, setCount] = useState(0);
    const [status, setStatus] = useState("Idle");
    
    // useContext: Consumes a context value
    const theme = useContext(ThemeContext);

    // useEffect: Handles side effects (fetching, subscription, manual DOM changes)
    // Run whenever 'count' updates
    useEffect(() => {
        console.log(`[Effect] Count updated to: ${count}`);
        setStatus("Counting...");
        
        // Timeout to simulate completion of state calculation
        const timer = setTimeout(() => setStatus("Idle"), 500);
        
        // Optional Cleanup function called before executing effect again or unmounting
        return () => clearTimeout(timer);
    }, [count]);

    return (
        <div className={`counter-box theme-${theme}`} style={{ padding: '10px' }}>
            <p><strong>Theme Context Active:</strong> {theme}</p>
            <p><strong>Current Count:</strong> {count}</p>
            <p><strong>Status:</strong> {status}</p>
            
            {/* Event handlers calling setter functions */}
            <button onClick={() => setCount(count + 1)}>Increment</button>
            <button onClick={() => setCount(count - 1)}>Decrement</button>
            <button onClick={() => setCount(0)}>Reset</button>
        </div>
    );
}


// ==============================================================================
// 4. REACT ROUTER SIMULATION
// ==============================================================================
/*
In a standard React application, 'react-router-dom' provides client-side routing.
It intercepts browser navigation to swap components in/out without reloading the page.

Example Config:
--------------------------------------------------------------------------------
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';

function App() {
    return (
        <BrowserRouter>
            <nav>
                <Link to="/">Home</Link>
                <Link to="/courses">Courses</Link>
            </nav>
            
            <Routes>
                <Route path="/" element={<HomeView />} />
                <Route path="/courses" element={<CoursesListView />} />
                <Route path="/courses/:courseId" element={<CourseDetailView />} />
            </Routes>
        </BrowserRouter>
    );
}
*/


// ==============================================================================
// MAIN APP INTEGRATION
// ==============================================================================
export default function App() {
    return (
        // Provide the ThemeContext value to all descendant components
        <ThemeContext.Provider value="dark">
            <div className="app-container" style={{ padding: '20px' }}>
                <h1>React.js Foundations Demonstration</h1>
                
                {/* Rendering components and passing Props */}
                <CourseCard title="Python Full Stack Engineer" duration="12 Weeks">
                    <p>Learn core Python, web design, frameworks, and databases.</p>
                </CourseCard>
                
                <CourseCard title="React & Component Architecture" duration="3 Weeks">
                    <p>Master declarative virtual DOM rendering and hooks.</p>
                </CourseCard>
                
                <h2>Hooks Demonstration (State & Context)</h2>
                <CounterComponent />
            </div>
        </ThemeContext.Provider>
    );
}

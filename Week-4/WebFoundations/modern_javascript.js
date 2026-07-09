/**
 * Modern JavaScript Foundations (ES6+)
 * 
 * This file demonstrates modern JavaScript concepts used heavily by frameworks.
 * It is runnable in a Node.js environment:
 *   node modern_javascript.js
 */

// Helper function to print header blocks
const printHeader = (title) => {
    console.log("\n" + "=" .repeat(60));
    console.log(` ${title}`);
    console.log("=" .repeat(60));
};

// ==============================================================================
// 1. SCOPING: let, const, and var
// ==============================================================================
printHeader("1. VARIABLE SCOPING: let vs const vs var");

// - 'var': Function-scoped, hoisted. Can cause bug leakage.
// - 'let': Block-scoped, cannot be re-declared in same scope, not initialized on hoisting.
// - 'const': Block-scoped, read-only reference. Must be assigned on declaration.

function scopeDemo() {
    if (true) {
        var functionScopedVar = "I am visible outside the block!";
        let blockScopedLet = "I am only visible inside this if-block!";
        const blockScopedConst = "I am also block scoped and immutable!";
        
        console.log("[Inside Block] var:", functionScopedVar);
        console.log("[Inside Block] let:", blockScopedLet);
    }
    
    console.log("[Outside Block] var:", functionScopedVar); // Works!
    
    try {
        console.log("[Outside Block] let:", blockScopedLet); // Fails!
    } catch (e) {
        console.log("[Outside Block] let: Caught Expected Error ->", e.message);
    }
    
    // Constant immutability demo:
    const user = { name: "Alice" };
    user.name = "Bob"; // ALLOWED: Mutating properties of the object reference is valid.
    console.log("Mutated const object property:", user.name);
    
    try {
        user = { name: "Charlie" }; // BLOCKED: Cannot reassign a new reference.
    } catch (e) {
        console.log("Reassigning const reference: Caught Expected Error ->", e.message);
    }
}
scopeDemo();


// ==============================================================================
// 2. ARROW FUNCTIONS & LEXICAL 'this'
// ==============================================================================
printHeader("2. ARROW FUNCTIONS & LEXICAL 'this'");

// Arrow functions provide short syntax: (args) => body
const add = (a, b) => a + b;
// Implicit return if no curly braces:
const square = x => x * x;

console.log("Arrow addition (5 + 7):", add(5, 7));
console.log("Arrow square (6^2):", square(6));

// Lexical 'this': Standard functions bind 'this' depending on how they are called.
// Arrow functions do not define their own 'this'; they inherit it from parent context.
const group = {
    title: "Python Full Stack",
    students: ["Alex", "Blake"],
    
    showStudentsNormal() {
        console.log("Normal function context inside showStudentsNormal:", this.title);
        
        // This inner callback will fail to read 'this.title' because it executes in a new context
        this.students.forEach(function(student) {
            // 'this' is undefined or global in non-strict mode
            console.log(`  - ${student} belongs to ${this ? this.title : 'undefined context'}`);
        });
    },
    
    showStudentsArrow() {
        // Arrow function binds 'this' lexically to the 'group' object
        this.students.forEach(student => {
            console.log(`  - ${student} belongs to ${this.title} (Arrow)`);
        });
    }
};

group.showStudentsNormal();
group.showStudentsArrow();


// ==============================================================================
// 3. PROMISES (Resolve, Reject, and Chaining)
// ==============================================================================
printHeader("3. PROMISES: RESOLVE, REJECT, AND CHAINING");

// A Promise is an object representing eventual completion/failure of an async operation.
// States: Pending, Fulfilled, Rejected.

const fetchUserData = (userId) => {
    return new Promise((resolve, reject) => {
        console.log(`[Promise] Fetching data for user ${userId}...`);
        setTimeout(() => {
            if (userId > 0) {
                resolve({ id: userId, username: "dev_john", status: "Active" });
            } else {
                reject(new Error("Invalid User ID requested."));
            }
        }, 100); // Mimicking network delay
    });
};

// Chaining Promises
fetchUserData(101)
    .then(user => {
        console.log("Step 1 (Fetch User) Complete:", user.username);
        // Return a new value or promise to continue chaining
        return user.status;
    })
    .then(status => {
        console.log("Step 2 (Read Status) Complete:", status);
    })
    .catch(error => {
        console.error("Error in promise chain:", error.message);
    });

// Handling rejection
fetchUserData(-1)
    .catch(error => {
        console.log("Expected Rejection Caught:", error.message);
    });


// ==============================================================================
// 4. ASYNC / AWAIT
// ==============================================================================
// Async/Await is syntactic sugar over Promises, making async code read like sync.

// Delay helper returning a promise
const delay = ms => new Promise(res => setTimeout(res, ms));

async function getCourseDetails() {
    await delay(200); // Waits non-blockingly
    return { name: "FSE Course", duration: "12 Weeks" };
}

async function runAsyncDemo() {
    printHeader("4. ASYNC / AWAIT");
    
    try {
        console.log("Starting async retrieve...");
        const details = await getCourseDetails(); // Suspends execution until promise resolves
        console.log("Retrieved details via Await:", details.name);
    } catch (e) {
        console.error("Caught error inside async block:", e);
    }
    
    // Parallel Execution with Promise.all (Optimizing speeds)
    console.log("\nStarting Parallel Requests...");
    const startTime = Date.now();
    
    const task1 = () => new Promise(res => setTimeout(() => res("Task 1 complete"), 150));
    const task2 = () => new Promise(res => setTimeout(() => res("Task 2 complete"), 150));
    
    // Executes both tasks concurrently
    const results = await Promise.all([task1(), task2()]);
    
    console.log("Parallel Results:", results);
    console.log(`Completed in ${Date.now() - startTime}ms (Expected ~150ms instead of 300ms)`);
}

// Running async demo at the end of the script
setTimeout(runAsyncDemo, 300);


// ==============================================================================
// 5. ES MODULES (Export and Import Syntax Overview)
// ==============================================================================
/*
ES Modules (ESM) is the official standard format to package JavaScript code.
It uses 'export' to expose functions/objects, and 'import' to bring them in.

File: math_utils.js
------------------------------------------------------------------
export const add = (x, y) => x + y;       // Named export
export default function multiply(x, y) {  // Default export
    return x * y;
}

File: app.js
------------------------------------------------------------------
import multiply, { add } from './math_utils.js'; // Importing standard & default
console.log(add(2, 3));      // 5
console.log(multiply(2, 3)); // 6
*/

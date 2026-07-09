/**
 * API Integration: Fetch API & Axios Client
 * 
 * This file demonstrates:
 * 1. Fetch API (GET and POST)
 * 2. Axios configuration (Instances, Interceptors)
 * 3. Client-side HTTP Error Handling
 * 
 * To run this file:
 *   node api_integration.js
 */

const API_BASE = "https://jsonplaceholder.typicode.com";

// Helper function to print header blocks
const printHeader = (title) => {
    console.log("\n" + "=" .repeat(60));
    console.log(` ${title}`);
    console.log("=" .repeat(60));
};


// ==============================================================================
// 1. FETCH API (Native Browser API, built-in to Node 18+)
// ==============================================================================

async function runFetchDemo() {
    printHeader("1. FETCH API DEMONSTRATIONS");
    
    // [A] GET Request
    try {
        console.log("[Fetch] Getting single post...");
        const response = await fetch(`${API_BASE}/posts/1`);
        
        // Fetch does NOT throw errors on HTTP failure status codes (e.g. 404 or 500).
        // We must check response.ok manually!
        if (!response.ok) {
            throw new Error(`HTTP Error Status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log("Fetch GET Success! Title:", data.title.substring(0, 30) + "...");
    } catch (error) {
        console.error("Fetch GET Failed:", error.message);
    }

    // [B] POST Request
    try {
        console.log("\n[Fetch] Submitting new post data...");
        const response = await fetch(`${API_BASE}/posts`, {
            method: "POST",
            body: JSON.stringify({
                title: "Learning Frontend Engineering",
                body: "This is the week 4 curriculum covering React, Angular, Vue.",
                userId: 42
            }),
            headers: {
                "Content-type": "application/json; charset=UTF-8",
                "Authorization": "Bearer mock-user-token"
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP Error Status: ${response.status}`);
        }

        const data = await response.json();
        console.log("Fetch POST Success! Created ID:", data.id);
    } catch (error) {
        console.error("Fetch POST Failed:", error.message);
    }
}


// ==============================================================================
// 2. AXIOS CONFIGURATION (Mocked / Conceptual Runnable Example)
// ==============================================================================

// In production, we install axios: npm install axios
// Below, we outline how an Axios client is configured and why it is preferred.

/*
Axios Benefits:
  1. Throws exceptions automatically on any non-2xx status code.
  2. Automatic JSON data parsing.
  3. Easy setup of client instances with baseline headers (like JWT authorization).
  4. Interceptors to inject parameters globally or refresh credentials.
*/

// Conceptual setup block:
const mockAxiosInstanceSetup = () => {
    printHeader("2. AXIOS CONFIGURATIONS");
    
    console.log("Explanation: Setting up an Axios Client instance...");
    
    const sampleInstanceCode = `
    import axios from 'axios';

    // Create custom instance
    const apiClient = axios.create({
        baseURL: 'https://api.myapp.com/v1',
        timeout: 5000,
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    });

    // Request Interceptor: Inject JWT token into headers before request leaves
    apiClient.interceptors.request.use(
        (config) => {
            const token = localStorage.getItem('user_token');
            if (token) {
                config.headers['Authorization'] = \`Bearer \${token}\`;
            }
            return config;
        },
        (error) => Promise.reject(error)
    );

    // Response Interceptor: Catch expired tokens globally and trigger login
    apiClient.interceptors.response.use(
        (response) => response,
        (error) => {
            if (error.response && error.response.status === 401) {
                console.log("Unauthorized! Redirecting to login page...");
                // redirectUserToLogin();
            }
            return Promise.reject(error);
        }
    );
    `;
    
    console.log(sampleInstanceCode);
};


// ==============================================================================
// 3. ROBUST CLIENT-SIDE ERROR HANDLING
// ==============================================================================
printHeader("3. CLIENT-SIDE ERROR HANDLING");

function handleErrorGracefully(error) {
    // Check if error is from Axios (Axios error objects contain an 'error.response' field)
    if (error.response) {
        // Server responded with a status code outside the 2xx range
        const status = error.response.status;
        console.warn(`[API Error] Server responded with status ${status}`);
        
        if (status === 400) {
            return "Invalid request data. Please check your inputs.";
        } else if (status === 401) {
            return "Session expired. Please log in again.";
        } else if (status === 403) {
            return "You do not have permission to perform this action.";
        } else if (status === 404) {
            return "The requested content could not be found.";
        } else if (status >= 500) {
            return "Server issue. Our engineers are notified. Please try again later.";
        }
    } else if (error.request) {
        // Request was sent but no response was received (Network Down / Timeout)
        console.error("[Network Error] No response received from server.");
        return "Network connection issue. Please check your internet.";
    } else {
        // General JavaScript / Runtime error
        console.error("[Runtime Error] details:", error.message);
    }
    return "An unexpected error occurred. Please try again.";
}

// Running error handling demonstration
const mockAxiosError = {
    response: {
        status: 401,
        data: { message: "Token expired" }
    }
};

const userMessage = handleErrorGracefully(mockAxiosError);
console.log("Resulting User-facing Alert message:");
console.log(`  => "${userMessage}"`);


// ==============================================================================
// RUN ALL RUNNABLE PARTS
// ==============================================================================
async function main() {
    await runFetchDemo();
    mockAxiosInstanceSetup();
}
main();

/**
 * Module 4: Testing - Jest JavaScript Testing Examples
 * ---------------------------------------------------------------------
 * This file contains Jest test examples, demonstrating standard matchers,
 * asynchronous testing, mock functions, and snapshot assertions.
 * ---------------------------------------------------------------------
 */

// =====================================================================
// Target Code to Test
// =====================================================================
const api = {
  fetchUser: (id) => {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (id > 0) {
          resolve({ id, name: "Alice", active: true });
        } else {
          reject(new Error("User not found"));
        }
      }, 50);
    });
  }
};

function processUserData(userId, callback) {
  // Simulates executing a callback with retrieved user details
  return api.fetchUser(userId)
    .then(user => callback(user.name))
    .catch(err => callback(null, err.message));
}


// =====================================================================
// Jest Test Assertions
// =====================================================================

describe("Jest Matcher Examples", () => {
  // `toBe` checks primitive equality (using Object.is)
  test("adds 2 + 2 to equal 4", () => {
    expect(2 + 2).toBe(4);
  });

  // `toEqual` recursively checks properties of objects/arrays (deep equality)
  test("object assignment matches", () => {
    const data = { one: 1 };
    data["two"] = 2;
    expect(data).toEqual({ one: 1, two: 2 });
  });

  test("null is falsy, but defined", () => {
    const n = null;
    expect(n).toBeNull();
    expect(n).toBeDefined();
    expect(n).not.toBeUndefined();
    expect(n).not.toBeTruthy();
    expect(n).toBeFalsy();
  });
});


describe("Asynchronous Testing", () => {
  // A. Using async/await
  test("fetches user successfully with async/await", async () => {
    const user = await api.fetchUser(1);
    expect(user.name).toBe("Alice");
    expect(user.active).toBe(true);
  });

  // B. Testing Promises using `.resolves` or `.rejects` matchers
  test("resolves to Alice info", () => {
    return expect(api.fetchUser(1)).resolves.toEqual({ id: 1, name: "Alice", active: true });
  });

  test("fails with user not found on invalid ID", () => {
    return expect(api.fetchUser(-1)).rejects.toThrow("User not found");
  });
});


describe("Mock Functions", () => {
  test("callback is invoked with Alice name", async () => {
    // jest.fn() creates a mock function to record calls and arguments
    const mockCallback = jest.fn();

    // Act
    await processUserData(1, mockCallback);

    // Assert
    // Check if the mock was called
    expect(mockCallback).toHaveBeenCalled();
    // Check if it was called exactly 1 time
    expect(mockCallback).toHaveBeenCalledTimes(1);
    // Check the first argument of the first call
    expect(mockCallback).toHaveBeenLastCalledWith("Alice");
  });
});


describe("Snapshot Testing Concept", () => {
  test("renders user config correctly", () => {
    const userConfig = {
      theme: "dark",
      permissions: ["read", "write"],
      createdAt: "2026-07-08T00:00:00Z"
    };

    // `toMatchSnapshot()` saves a representation of the object to a separate 
    // `.snap` file. Future runs compare the object against that saved state.
    // Uncommenting this in a running Jest env validates UI or JSON state:
    // expect(userConfig).toMatchSnapshot();
    
    // Inline snapshot alternative
    expect(userConfig).toEqual({
      theme: "dark",
      permissions: expect.arrayContaining(["read", "write"]),
      createdAt: expect.any(String)
    });
  });
});

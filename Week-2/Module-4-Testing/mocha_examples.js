/**
 * Module 4: Testing - Mocha and Chai Examples
 * ---------------------------------------------------------------------
 * This file illustrates testing with Mocha as the test runner and 
 * Chai as the assertion library, showcasing BDD structures, hooks,
 * and the three assertion styles (expect, should, assert).
 * ---------------------------------------------------------------------
 */

// Import assertion styles from Chai
// Note: In a running Node environment, run: npm install mocha chai
const chai = require("chai");
const expect = chai.expect;
const assert = chai.assert;
const should = chai.should(); // Invoking should() modifies Object.prototype


// =====================================================================
// Target Code to Test
// =====================================================================
class ShoppingCart {
  constructor() {
    this.items = [];
  }

  addItem(item) {
    this.items.push(item);
  }

  checkoutAsync() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({ status: "success", count: this.items.length });
      }, 50);
    });
  }
}


// =====================================================================
// Mocha & Chai Test Suite
// =====================================================================

describe("ShoppingCart Class", () => {
  let cart;

  // -------------------------------------------------------------
  // Mocha Hooks
  // -------------------------------------------------------------
  before(() => {
    // Runs once before all tests in this describe block
    // Useful for database setup or server connection initialization
  });

  after(() => {
    // Runs once after all tests in this describe block have finished
  });

  beforeEach(() => {
    // Runs before every individual 'it' test block. Ensures test isolation.
    cart = new ShoppingCart();
  });

  afterEach(() => {
    // Runs after every individual 'it' test block. Cleans up state.
  });

  // -------------------------------------------------------------
  // Assertion Styles (Chai)
  // -------------------------------------------------------------
  it("should add items to the cart (expect style)", () => {
    cart.addItem("Apple");
    expect(cart.items).to.be.an("array").that.includes("Apple");
    expect(cart.items).to.have.lengthOf(1);
  });

  it("should add items to the cart (should style)", () => {
    cart.addItem("Orange");
    cart.items.should.be.an("array").that.includes("Orange");
    cart.items.should.have.lengthOf(1);
  });

  it("should add items to the cart (assert style)", () => {
    cart.addItem("Banana");
    assert.isArray(cart.items);
    assert.include(cart.items, "Banana");
    assert.equal(cart.items.length, 1);
  });

  // -------------------------------------------------------------
  // Async Testing in Mocha
  // -------------------------------------------------------------

  // Method A: Returning a Promise
  it("should checkout successfully (returning a Promise)", () => {
    cart.addItem("Book");
    return cart.checkoutAsync().then((receipt) => {
      expect(receipt.status).to.equal("success");
      expect(receipt.count).to.equal(1);
    });
  });

  // Method B: Using async/await
  it("should checkout successfully (using async/await)", async () => {
    cart.addItem("Toy");
    const receipt = await cart.checkoutAsync();
    expect(receipt.status).to.equal("success");
    expect(receipt.count).to.equal(1);
  });

  // Method C: Using the `done` callback (for older callback styles)
  it("should execute async code (using done callback)", (done) => {
    cart.addItem("Pen");
    cart.checkoutAsync()
      .then((receipt) => {
        expect(receipt.status).to.equal("success");
        done(); // Invoke done() to tell Mocha the test has finished
      })
      .catch((err) => {
        done(err); // Pass error to done() if assertions failed
      });
  });
});

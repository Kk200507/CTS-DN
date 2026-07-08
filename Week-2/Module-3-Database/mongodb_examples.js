/**
 * Module 3: Database - MongoDB Examples
 * ---------------------------------------------------------------------
 * This file contains Mongo Shell (mongosh) JavaScript commands demonstrating
 * CRUD operations, indexes, and the Aggregation Framework.
 * ---------------------------------------------------------------------
 */

// Select database
db = db.getSiblingDB("store_db");

// Clear existing collection
db.products.drop();
db.orders.drop();

// =====================================================================
// 1. CRUD Operations
// =====================================================================

// A. Create (Insert)
db.products.insertMany([
  {
    _id: ObjectId("60c72b2f9b1d8b2bad000001"),
    name: "Laptop",
    category: "Electronics",
    price: 1200,
    stock: 50,
    tags: ["computers", "office", "work"],
    attributes: { brand: "Dell", warrantyYears: 2 }
  },
  {
    _id: ObjectId("60c72b2f9b1d8b2bad000002"),
    name: "Smartphone",
    category: "Electronics",
    price: 800,
    stock: 100,
    tags: ["mobile", "gadget"],
    attributes: { brand: "Apple", warrantyYears: 1 }
  },
  {
    _id: ObjectId("60c72b2f9b1d8b2bad000003"),
    name: "Coffee Mug",
    category: "Kitchen",
    price: 15,
    stock: 200,
    tags: ["home", "office"],
    attributes: { brand: "CeramicCo", color: "Blue" }
  }
]);

// B. Read (Query)
// Find products in Electronics with price > 500, projection to return only name and price
db.products.find(
  { category: "Electronics", price: { $gt: 500 } },
  { name: 1, price: 1, _id: 0 }
);

// Find products by element in array
db.products.find({ tags: "office" });

// Query nested document fields
db.products.find({ "attributes.warrantyYears": { $gte: 2 } });

// C. Update
// Update stock and add a tag for Laptop
db.products.updateOne(
  { name: "Laptop" },
  { 
    $set: { stock: 45 },
    $addToSet: { tags: "sale" } 
  }
);

// D. Delete
// Delete Coffee Mug
db.products.deleteOne({ name: "Coffee Mug" });


// =====================================================================
// 2. Indexing
// =====================================================================

// A. Single Field Index
db.products.createIndex({ category: 1 });

// B. Compound Index (for queries sorting/filtering by category and price)
db.products.createIndex({ category: 1, price: -1 });

// C. Multikey Index (Automatic when index is on an array field)
db.products.createIndex({ tags: 1 });

// D. Text Index (for full-text search)
db.products.createIndex({ name: "text", category: "text" });

// Text Search Example
db.products.find({ $text: { $search: "laptop" } });


// =====================================================================
// 3. Aggregation Framework
// =====================================================================
// The Aggregation Framework evaluates documents in pipeline stages.

// Insert orders for lookup demo
db.orders.insertMany([
  { orderId: 101, product_id: ObjectId("60c72b2f9b1d8b2bad000001"), quantity: 2, order_date: ISODate("2026-07-01T10:00:00Z") },
  { orderId: 102, product_id: ObjectId("60c72b2f9b1d8b2bad000002"), quantity: 1, order_date: ISODate("2026-07-02T11:30:00Z") },
  { orderId: 103, product_id: ObjectId("60c72b2f9b1d8b2bad000001"), quantity: 1, order_date: ISODate("2026-07-03T15:45:00Z") }
]);

// Run aggregation: Sum of quantity sold per product, joining product metadata
db.orders.aggregate([
  // Stage 1: Match orders in July 2026
  {
    $match: {
      order_date: {
        $gte: ISODate("2026-07-01T00:00:00Z"),
        $lt: ISODate("2026-08-01T00:00:00Z")
      }
    }
  },

  // Stage 2: Join product details using $lookup (similar to SQL LEFT JOIN)
  {
    $lookup: {
      from: "products",
      localField: "product_id",
      foreignField: "_id",
      as: "product_info"
    }
  },

  // Stage 3: Deconstruct the product_info array (since $lookup output is an array)
  {
    $unwind: "$product_info"
  },

  // Stage 4: Group by product name, sum quantity, and compute total revenue
  {
    $group: {
      _id: "$product_info.name",
      total_quantity_sold: { $sum: "$quantity" },
      total_revenue: { $sum: { $multiply: ["$quantity", "$product_info.price"] } }
    }
  },

  // Stage 5: Sort by total revenue descending
  {
    $sort: { total_revenue: -1 }
  },

  // Stage 6: Project the output with clean formatting
  {
    $project: {
      _id: 0,
      productName: "$_id",
      totalQuantity: "$total_quantity_sold",
      totalRevenue: "$total_revenue"
    }
  }
]);

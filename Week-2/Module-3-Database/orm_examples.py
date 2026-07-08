"""
Module 3: Database - SQLAlchemy ORM Examples (SQLAlchemy 2.0 Style)
---------------------------------------------------------------------
This script illustrates how to map relational tables to Python objects
using SQLAlchemy ORM, manage relationships, perform CRUD operations,
and handle eager loading.
---------------------------------------------------------------------
"""

import os
from typing import List, Optional
from sqlalchemy import (
    ForeignKey, 
    String, 
    Integer, 
    Float, 
    Table, 
    Column, 
    create_engine, 
    select
)
from sqlalchemy.orm import (
    DeclarativeBase, 
    Mapped, 
    mapped_column, 
    relationship, 
    sessionmaker,
    joinedload,
    selectinload
)

# =====================================================================
# 1. Base Declaration
# =====================================================================
class Base(DeclarativeBase):
    pass


# =====================================================================
# 2. Association Table (Many-to-Many: Product <-> Tag)
# =====================================================================
# In SQLAlchemy 2.0, association tables for many-to-many relationships
# are typically defined using Table objects bound to Base.metadata.
product_tag_association = Table(
    "product_tag",
    Base.metadata,
    Column("product_id", ForeignKey("products.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


# =====================================================================
# 3. Model Definitions
# =====================================================================

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Back reference to Product
    products: Mapped[List["Product"]] = relationship(
        secondary=product_tag_association, back_populates="tags"
    )

    def __repr__(self) -> str:
        return f"<Tag(name={self.name!r})>"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    # Many-to-Many Relationship with Tag
    tags: Mapped[List[Tag]] = relationship(
        secondary=product_tag_association, back_populates="products"
    )

    # One-to-Many Relationship: Product has many Orders
    orders: Mapped[List["Order"]] = relationship(back_populates="product")

    def __repr__(self) -> str:
        return f"<Product(name={self.name!r}, price={self.price})>"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False)

    # One-to-Many Relationship: User has many Orders
    orders: Mapped[List["Order"]] = relationship(back_populates="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<User(username={self.username!r})>"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), nullable=False)

    # Many-to-One Relationships
    user: Mapped[User] = relationship(back_populates="orders")
    product: Mapped[Product] = relationship(back_populates="orders")

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, qty={self.quantity})>"


# =====================================================================
# 4. Engine & Session Configuration
# =====================================================================
# Using in-memory SQLite for runnable demonstration.
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# =====================================================================
# 5. CRUD and Query Execution Examples
# =====================================================================

def main():
    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully.")

    # Create Session context
    with SessionLocal() as session:
        # -------------------------------------------------------------
        # CREATE
        # -------------------------------------------------------------
        print("\n--- Creating Records ---")
        tag_electronics = Tag(name="Electronics")
        tag_office = Tag(name="Office")

        laptop = Product(name="MacBook Air", price=999.99, tags=[tag_electronics, tag_office])
        mouse = Product(name="Bluetooth Mouse", price=29.99, tags=[tag_office])

        user_alice = User(username="alice_dev", email="alice@example.com")
        
        # Add to session
        session.add_all([tag_electronics, tag_office, laptop, mouse, user_alice])
        session.commit() # Commit transaction to database

        # Create Orders
        order_1 = Order(user=user_alice, product=laptop, quantity=1)
        order_2 = Order(user=user_alice, product=mouse, quantity=2)
        session.add_all([order_1, order_2])
        session.commit()
        print("Created User, Products, Tags, and Orders.")

        # -------------------------------------------------------------
        # READ (Queries)
        # -------------------------------------------------------------
        print("\n--- Reading Records ---")
        # Standard Select query
        stmt = select(User).where(User.username == "alice_dev")
        user = session.execute(stmt).scalar_one_or_none()
        print(f"Retrieved User: {user}")

        # Eager Loading: Eagerly load user's orders using joinedload to prevent N+1 queries
        print("\n--- Querying with Eager Loading (joinedload) ---")
        stmt_eager = select(User).options(joinedload(User.orders)).where(User.username == "alice_dev")
        user_with_orders = session.execute(stmt_eager).unique().scalar_one()
        print(f"User {user_with_orders.username} has orders:")
        for order in user_with_orders.orders:
            print(f" - Order ID: {order.id}, Quantity: {order.quantity}")

        # Eager Loading Many-to-Many: selectinload is optimal for collections
        print("\n--- Querying Products and Tags (selectinload) ---")
        stmt_products = select(Product).options(selectinload(Product.tags))
        products = session.scalars(stmt_products).all()
        for p in products:
            print(f"Product: {p.name}, Tags: {[t.name for t in p.tags]}")

        # -------------------------------------------------------------
        # UPDATE
        # -------------------------------------------------------------
        print("\n--- Updating Records ---")
        # Retrieve product to update
        stmt_product = select(Product).where(Product.name == "Bluetooth Mouse")
        target_product = session.scalars(stmt_product).first()
        if target_product:
            print(f"Old Price: {target_product.price}")
            target_product.price = 24.99 # Make change directly on object
            session.commit() # Save changes
            print(f"Updated Price: {target_product.price}")

        # -------------------------------------------------------------
        # DELETE
        # -------------------------------------------------------------
        print("\n--- Deleting Records ---")
        # Retrieve user to delete (Cascade configuration will automatically delete associated orders)
        stmt_del_user = select(User).where(User.username == "alice_dev")
        del_user = session.scalars(stmt_del_user).first()
        if del_user:
            session.delete(del_user)
            session.commit()
            print("Deleted User and all their associated orders.")

        # Verify Orders are deleted
        remaining_orders = session.scalars(select(Order)).all()
        print(f"Remaining orders in database count: {len(remaining_orders)}")


if __name__ == "__main__":
    main()

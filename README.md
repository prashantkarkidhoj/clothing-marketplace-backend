# Reels-First Clothing Marketplace — Backend

A Flask-based REST API powering a two-sided marketplace connecting clothing sellers and buyers in Nepal. Built from the ground up in Python, with authentication, a relational database, and inventory-aware order processing.

## What it does

This backend is the engine behind a marketplace app where small clothing sellers — many of whom currently operate through scattered Instagram and Facebook pages — can register, list products, and sell with a built-in trust and inventory system. Buyers can browse listings, place orders, and track their purchase history.

## Core features

- **Seller accounts** — registration and login with encrypted password storage
- **Buyer accounts** — separate registration and login flow
- **Product listings** — sellers add products with size, color, and quantity
- **Marketplace browsing** — public endpoint to view all products with seller details attached
- **Order placement** — buyers place orders; inventory is automatically reduced at the moment of purchase, preventing overselling
- **Order history** — buyers can view all their past and pending orders
- **Order status management** — sellers can update an order's status (pending → shipped → delivered), restricted to the seller who owns that product

## Technical stack

- **Framework:** Flask (Python)
- **Database:** SQLite via Flask-SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens) via Flask-JWT-Extended
- **Password security:** Bcrypt hashing — passwords are never stored in plain text
- **API design:** RESTful endpoints following standard HTTP conventions (GET, POST, PUT)

## Architecture

The system is modeled around three core entities:

- `Seller` — owns products, has a shop profile and delivery area
- `Product` — belongs to a seller, tracks live quantity
- `Buyer` — places orders against products
- `Order` — links a buyer to a product, tracks quantity and status, and is the single source of truth for inventory deduction

Every write operation that modifies sensitive data (adding a product, placing an order, updating order status) is protected behind JWT authentication, ensuring only the rightful seller or buyer can perform that action.

## Status

This is the foundational backend layer (Phase 1 of a larger roadmap). Next steps include an AI-powered seller onboarding agent, a Flutter mobile frontend, payment gateway integration (eSewa/Khalti), and KYC verification.

---

*Built independently while learning Python, Flask, and backend development from the ground up — as part of a 4-month plan to become job-ready as an AI automation/backend engineer.*

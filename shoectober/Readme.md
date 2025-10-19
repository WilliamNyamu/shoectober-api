# About the Project

- This is a Django REST Framework (DRF) e-Commerce application built to strengthen my skills in API development. It includes features for product management, reviews, wishlisting, purchases, and token-based authentication.

---

## Features
1. Product CRUD

Supports Product Creation, Reading, Updating, and Deleting.
More details can be found in:
shoectober/product/Product_Readme.md

2. Product Reviews

Allows authenticated users to review products.
Documentation available at:
shoectober/product/Review_Readme.md

3. Product Category

Product categories are currently hard-coded.
Dynamic implementation is not yet completed.

4. Wishlist

Users can add products to their wishlist and manage wishlist entries.
Documentation available at:
shoectober/product/Wishlist_Readme.md

5. Purchases

Users can purchase products through an authenticated endpoint.
Documentation available at:
shoectober/products/Purchase_Readme.md

## Authentication

This project uses Token Authentication.

When a user registers, a token is automatically generated for them.

This token must be included in the Authorization header for all protected API endpoints.

Example:

Authorization: Token <your_token_here>

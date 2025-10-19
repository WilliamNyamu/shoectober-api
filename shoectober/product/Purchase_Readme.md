Purchase API Documentation
1. Get All Purchases

GET /api/products/purchases/
Retrieves a list of all purchase records in the system for the currently authenticated user

Authorization
This endpoint requires authentication.
Example:

Authorization: Token <your_token_here>


Example Request

GET /api/products/purchases/
Authorization: Token abc123def456


Example Response

[
  {
    "id": 14,
    "product": "Jordan Retro 4",
    "quantity": 2,
    "purchased_at": "2025-10-19T08:45:00Z"
  }
]

2. Purchase a Product

POST /api/products/{product_id}/purchase/
Allows an authenticated user to purchase a specific product by specifying a quantity.

Path Variable

product_id — The unique ID of the product being purchased.

Authorization

Authorization: Token <your_token_here>
Content-Type: application/json


Request Body

{
  "quantity": 2
}


Example Request

POST /api/products/11/purchase/
Authorization: Token abc123def456
Content-Type: application/json

{
  "quantity": 2
}


Response
Returns 201 Created on success and confirms the purchase.

{
  "id": 14,
  "product": "Jordan Retro 4",
  "quantity": 2,
  "total_price": "240.00",
  "purchased_at": "2025-10-19T08:45:00Z"
}

Error Responses
Status Code	Meaning
401 Unauthorized	Missing or invalid token
404 Not Found	Product not found
400 Bad Request	Missing or invalid quantity
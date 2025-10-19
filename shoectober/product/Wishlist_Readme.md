Wishlist API Documentation
1. Get User Wishlist

GET /api/products/wishlist/
Retrieves all wishlist items belonging to the authenticated user.

Authorization
This endpoint requires authentication.
Example:

Authorization: Token <your_token>


Example Request

GET /api/products/wishlist/
Authorization: Token abc123def456


Example Response

[
  {
    "id": 7,
    "product": "Jordan Retro 4",
    "description": "To buy as a gift in December",
    "created_at": "2025-10-19T10:20:00Z"
  }
]

2. Add Product to Wishlist

POST /api/products/wishlist/{product_id}/create/
Creates a wishlist entry for a specific product.

Path Variable

product_id — The ID of the product to add to the wishlist.

Authorization

Authorization: Token <your_token>
Content-Type: application/json


Request Body

{
  "description": "To buy as a gift in December"
}


Example Request

POST /api/products/wishlist/10/create/
Authorization: Token abc123def456
Content-Type: application/json

{
  "description": "To buy as a gift in December"
}


Response
Returns 201 Created on success.

{
  "id": 7,
  "product": "Jordan Retro 4",
  "description": "To buy as a gift in December",
  "created_at": "2025-10-19T10:20:00Z"
}

3. Update Wishlist Entry

PATCH /api/products/wishlist/{product_id}/update/{pk}/
Updates the wishlist note/description for a specific wishlist item.

Path Variables

product_id — ID of the product in the wishlist.

pk — ID of the wishlist entry to update.

Authorization

Authorization: Token <your_token>
Content-Type: application/json


Request Body

{
  "description": "Will buy the shoe once I get this month's salary"
}


Example Request

PATCH /api/products/wishlist/10/update/7/
Authorization: Token abc123def456
Content-Type: application/json

{
  "description": "Will buy the shoe once I get this month's salary"
}


Response
Returns 200 OK on success.

{
  "id": 7,
  "product": "Jordan Retro 4",
  "description": "Will buy the shoe once I get this month's salary",
  "updated_at": "2025-10-19T12:05:00Z"
}

Error Responses
Status Code	Meaning
401 Unauthorized	Missing or invalid token
404 Not Found	Product or wishlist entry not found
400 Bad Request	Invalid data provided
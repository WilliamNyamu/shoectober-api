Product Review API Documentation

List All Reviews for a Product
GET /api/products/{product_id}/reviews/
Public endpoint – no authentication required
Path Parameters

product_id (integer): Unique identifier of the product

Example Request
httpGET /api/products/42/reviews/
Response
Returns a JSON array of review objects:
json[
  {
    "id": 15,
    "content": "Excellent durability",
    "rating": 5,
    "created_at": "2025-10-19T08:00:00Z"
  }
]
```

---

## Create New Product Review
**POST** `/api/products/{product_id}/reviews/create/`

### Path Parameters
- `product_id` (integer): ID of product being reviewed

### Headers
```
Authorization: Token <your_token>
Content-Type: application/json
Request Body
FieldTypeRequiredDescriptioncontentstringYesReview text (1-500 characters)ratingintegerYesRating value (1-5)
Example Request
httpPOST /api/products/11/reviews/create/
Authorization: Token abc123def456
Content-Type: application/json

{
  "content": "Cool looking shoes. Do you have white-colored ones?",
  "rating": 3
}
```

### Response
Returns **201 Created** with the new review object.

---

## Update Existing Review
**PATCH** `/api/products/{product_id}/reviews/{pk}/`

### Path Parameters
- `product_id` (integer): ID of associated product
- `pk` (integer): ID of review to update

### Headers
```
Authorization: Token <your_token>
Content-Type: application/json
Request Body
FieldTypeRequiredDescriptionratingintegerYesUpdated rating (1-5)contentstringNoModified review text
Example Request
httpPATCH /api/products/11/reviews/42/
Authorization: Token abc123def456
Content-Type: application/json

{
  "rating": 4,
  "content": "Updated review: Color options now available!"
}
Response
Returns 200 OK with the updated review object.

Error Responses

404 Not Found: Product or review doesn't exist
403 Forbidden: Unauthorized modification attempt
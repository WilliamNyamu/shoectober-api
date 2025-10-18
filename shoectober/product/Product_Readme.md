## Product Endpoints

### Get All Products
**Endpoint**  
`GET http://127.0.0.1:8000/api/products/`

**Response**  
- Returns JSON array of product objects
- Fields: `id`, `name`, `description`, `price`, `creator`, `quantity`, `image`, `category`, `created_at`, `updated_at`

Anyone is allowed to access this api endpoint
---

### Get Single Product
**Endpoint**  
`GET http://127.0.0.1:8000/api/products/{product_id}/`

**Path Parameters**  
- `product_id` (integer): Target product ID

**Response**  
- Returns 404 if not found
- JSON object with full product details

Anyone is allowed to access this api endpoint
---

### Create Product
**Endpoint**  
`POST http://127.0.0.1:8000/api/products/create/`

**Headers**  
- `Authorization: Token <your_token>`

**Body (multipart/form-data)**  
- Required: `name`, `description`, `price`, `quantity`, `category`, `creator`, `image`  
- Example:  
  ```json
  {
    "name": "Macbook Air",
    "description": "Latest model with M3 chip",
    "price": 50000.00,
    "quantity": 30,
    "category": 1,
    "creator": 1
  }
Response

201 Created with new product JSON
## Update Product Quantity
**Endpoint**
 - PATCH http://127.0.0.1:8000/api/products/{product_id}/update/

**Headers**

**Authorization**: Token <your_token>
**permission is given to the an authenticated user who is the creator of the product**
Body (form-data)

quantity (integer): New stock quantity
Example

PATCH /api/products/11/update/
Body: quantity=5
Delete Product
Endpoint

## DELETE
 http://127.0.0.1:8000/api/products/{product_id}/delete/


**permission is given to the an authenticated user who is the creator of the product**
Headers

Authorization: Token <your_token>
Response

204 No Content on success
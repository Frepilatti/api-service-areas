## Introduction
  The Service Area API allows clients to manage providers and their associated service areas, as well as to search for service areas that include a specific geographic location. This documentation outlines the available endpoints, their usage, and examples to help you integrate with the API effectively.

## Base URL 
  http://<your-domain-or-ip>:8000
  Replace <your-domain-or-ip> with the actual domain or IP address where your API is hosted.

## Authentication
  Note: The API currently does not implement authentication. All endpoints are publicly accessible. For production environments, it's recommended to implement proper authentication mechanisms.

## Endpoints Overview
### Providers Endpoints
  POST /providers/: Create a new provider.
  GET /providers/: Retrieve all providers.
  GET /providers/{provider_id}: Retrieve a specific provider by ID.
  PUT /providers/{provider_id}: Update a provider's information.
  DELETE /providers/{provider_id}: Delete a provider.

### Service Areas Endpoints
  POST /providers/{provider_id}/service_areas/: Create a new service area for a provider.
  GET /service_areas/: Retrieve all service areas.
  GET /service_areas/{service_area_id}: Retrieve a specific service area by ID.
  PUT /service_areas/{service_area_id}: Update a service area's information.
  DELETE /service_areas/{service_area_id}: Delete a service area.

### Search Endpoint
  GET /search/?lat={lat}&lng={lng}: Search for service areas that include the given latitude and longitude.

## Providers Endpoints

### 1. Create a Provider
  Endpoint: POST /providers/
  Description: Creates a new provider.
  Method: POST
  Request Body:
    ```
    {
      "name": "string",
      "email": "string (valid email address)",
      "phone_number": "string",
      "language": "string",
      "currency": "string"
    }
    ```
  Response:
    Status Code: 200 OK
    Body:
      ```
      {
        "id": "integer",
        "name": "string",
        "email": "string",
        "phone_number": "string",
        "language": "string",
        "currency": "string",
        "service_areas": []
      }
      ```
  Example:

    Request:
      ```
      POST /providers/
      Content-Type: application/json
      {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone_number": "1234567890",
        "language": "English",
        "currency": "USD"
      }
      ```
    Response:
      ```
      {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone_number": "1234567890",
        "language": "English",
        "currency": "USD",
        "service_areas": []
      }
    ```
### 2. Get All Providers
  Endpoint: GET /providers/
  Description: Retrieves all providers.
  Method: GET
  Response:
    Status Code: 200 OK
    Body: An array of provider objects.
  Example:
  Request:
    GET /providers/
  Response:
    ```
    [
      {
        "id": 1,
        "name": "Name 1",
        "email": "user@example.com",
        "phone_number": "1234567890",
        "language": "English",
        "currency": "USD",
        "service_areas": []
      },
      {
        "id": 2,
        "name": "Name 2",
        "email": "user2@example.com",
        "phone_number": "0987654321",
        "language": "Spanish",
        "currency": "EUR",
        "service_areas": []
      }
    ]
    ```
  ### 3. Get a Provider by ID
    Endpoint: GET /providers/{provider_id}
    Description: Retrieves a provider by their ID.
    Method: GET
    Path Parameters:
      provider_id (integer): The ID of the provider.
    Response:
      Status Code: 200 OK
      Body: A provider object.
    Example:
      Request:
        GET /providers/1
    Response:
      ```
      {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone_number": "1234567890",
        "language": "English",
        "currency": "USD",
        "service_areas": []
      }
      ```
### 4. Update a Provider
  Endpoint: PUT /providers/{provider_id}
  Description: Updates a provider's information.
  Method: PUT
  Path Parameters:
    provider_id (integer): The ID of the provider.
  Request Body:
    ```
    {
      "name": "string",
      "email": "string (valid email address)",
      "phone_number": "string",
      "language": "string",
      "currency": "string"
    }
    ```
  Response:
    Status Code: 200 OK
    Body: The updated provider object.
  Example:
    Request:
      ```
      PUT /providers/1
      Content-Type: application/json

      {
        "name": "John Doe Updated",
        "email": "john.doe@example.com",
        "phone_number": "1234567890",
        "language": "French",
        "currency": "USD"
      }
      ```
    Response:
      ```
      {
        "id": 1,
        "name": "John Doe Updated",
        "email": "john.doe@example.com",
        "phone_number": "1234567890",
        "language": "French",
        "currency": "USD",
        "service_areas": []
      }
      ```
### 5. Delete a Provider
  Endpoint: DELETE /providers/{provider_id}
  Description: Deletes a provider.
  Method: DELETE
  Path Parameters:
    provider_id (integer): The ID of the provider.
  Response:
    Status Code: 200 OK
    Body: A confirmation message.
  Example:
    Request:
      DELETE /providers/1
  Response:
    ```
    {
      "detail": "Provider deleted successfully"
    }
    ```
## Service Areas Endpoints
### 1. Create a Service Area
Endpoint: POST /providers/{provider_id}/service_areas/
Description: Creates a new service area for a provider.
Method: POST
Path Parameters:
  provider_id (integer): The ID of the provider.
Request Body:
```
{
  "name": "string",
  "price": "float",
  "geojson": "string (valid GeoJSON Polygon)"
}
```
Response:
  Status Code: 200 OK
  Body: The created service area object.
Example:

  Request:
    POST /providers/1/service_areas/
    Content-Type: application/json
    ```
    {
      "name": "Downtown Area",
      "price": 150.0,
      "geojson": "{\"type\": \"Polygon\", \"coordinates\": [[[0.0, 0.0], [0.0, 10.0], [10.0, 10.0], [10.0, 0.0], [0.0, 0.0]]] }"
    }
    ```
  Response:
    ```
    {
      "id": 1,
      "provider_id": 1,
      "name": "Downtown Area",
      "price": 150.0,
      "geojson": "{\"type\": \"Polygon\", \"coordinates\": [[[0.0, 0.0], [0.0, 10.0], [10.0, 10.0], [10.0, 0.0], [0.0, 0.0]]] }"
    }
    ```
### 2. Get All Service Areas
  Endpoint: GET /service_areas/
  Description: Retrieves all service areas.
  Method: GET
  Response:
  Status Code: 200 OK
  Body: An array of service area objects.
  Example:
    Request:
      GET /service_areas/
    Response:
      ```
      [
        {
          "id": 1,
          "provider_id": 1,
          "name": "Downtown Area",
          "price": 150.0,
          "geojson": "{\"type\": \"Polygon\", \"coordinates\": [[[0.0, 0.0], [0.0, 10.0], [10.0, 10.0], [10.0, 0.0], [0.0, 0.0]]] }"
        }
      ]
      ```
### 3. Get a Service Area by ID
  Endpoint: GET /service_areas/{service_area_id}
  Description: Retrieves a service area by its ID.
  Method: GET
  Path Parameters:
    service_area_id (integer): The ID of the service area.
  Response:
    Status Code: 200 OK
    Body: A service area object.
  Example:
    Request:
      GET /service_areas/1
    Response:
      ```
      {
        "id": 1,
        "provider_id": 1,
        "name": "Downtown Area",
        "price": 150.0,
        "geojson": "{\"type\": \"Polygon\", \"coordinates\": [[[0.0, 0.0], [0.0, 10.0], [10.0, 10.0], [10.0, 0.0], [0.0, 0.0]]] }"
      }
      ```
### 4. Update a Service Area
  Endpoint: PUT /service_areas/{service_area_id}
  Description: Updates a service area's information.
  Method: PUT
  Path Parameters:
    service_area_id (integer): The ID of the service area.
  Request Body:
    ```
    {
      "name": "string",
      "price": "float",
      "geojson": "string (valid GeoJSON Polygon)"
    }
    ```
  Response:
    Status Code: 200 OK
    Body: The updated service area object.
    Example:
      Request:
        PUT /service_areas/1
        Content-Type: application/json
        ```
        {
          "name": "Downtown Area Updated",
          "price": 175.0,
          "geojson": "{\"type\": \"Polygon\", \"coordinates\": [[[5.0, 5.0], [5.0, 15.0], [15.0, 15.0], [15.0, 5.0], [5.0, 5.0]]] }"
        }
        ```
      Response:
        ```
        {
          "id": 1,
          "provider_id": 1,
          "name": "Downtown Area Updated",
          "price": 175.0,
          "geojson": "{\"type\": \"Polygon\", \"coordinates\": [[[5.0, 5.0], [5.0, 15.0], [15.0, 15.0], [15.0, 5.0], [5.0, 5.0]]] }"
        }
        ```
### 5. Delete a Service Area
  Endpoint: DELETE /service_areas/{service_area_id}
  Description: Deletes a service area.
  Method: DELETE
  Path Parameters:
    service_area_id (integer): The ID of the service area.
  Response:
    Status Code: 200 OK
    Body: A confirmation message.
  Example:
    Request:
      DELETE /service_areas/1
    Response:
      ```
      json
      Copiar código
      {
        "detail": "Service Area deleted successfully"
      }
      ```
## Search Endpoint
### Search Service Areas by Location
  Endpoint: GET /search/?lat={lat}&lng={lng}
  Description: Returns a list of all service areas that include the given latitude and longitude.
  Method: GET
  Query Parameters:
    lat (float): Latitude of the point.
    lng (float): Longitude of the point.
  Response:
    Status Code: 200 OK
    Body: An array of objects containing the service area name, provider's name, and price.
  Example:
    Request:
      GET /search/?lat=7.5&lng=7.5
    Response:
      ```
      [
        {
          "service_area_name": "Downtown Area Updated",
          "provider_name": "John Doe Updated",
          "price": 175.0
        }
      ]
      ```
## Error Handling
  The API returns errors using standard HTTP status codes along with a JSON response containing the error details.

### Common Status Codes
  200 OK: The request was successful.
  400 Bad Request: The request was invalid or cannot be served.
  404 Not Found: The requested resource could not be found.
  422 Unprocessable Entity: The request was well-formed but contains semantic errors (e.g., validation errors).
  500 Internal Server Error: An unexpected error occurred on the server.

## Data Models
### Provider Model
Fields:
  id (integer): Unique identifier.
  name (string): Provider's name.
  email (string): Valid email address.
  phone_number (string): Contact phone number.
  language (string): Language(s) spoken.
  currency (string): Currency accepted.
  service_areas (list): List of associated service areas.
### Service Area Model
Fields:
  id (integer): Unique identifier.
  provider_id (integer): ID of the associated provider.
  name (string): Name of the service area.
  price (float): Price for services within the area.
  geojson (string): GeoJSON representation of the area.

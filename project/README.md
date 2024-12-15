# Network Module Project

This project demonstrates a FastAPI application deployed behind Traefik, leveraging load balancing, HTTPS, and proper RESTful API design. The system is configured with a controlled CIDR, self-signed certificates, and a simple API for managing products.

## **Project Structure**

### Directory Overview:

- `/app` - Contains the FastAPI application (`main.py`).
- `/certs` - Contains the self-signed certificate and key (`cert.pem` and `key.pem`).
- `docker-compose.yml` - Defines the services, networks, and Traefik configurations.
- `dynamic.yml` - Configures Traefik's routers and middlewares.
- `.gitignore` - Prevents unnecessary files like `__pycache__` from being uploaded.
- `README.md` - Project documentation.

## **Setup Instructions**

### Prerequisites

1. Install Docker and Docker Compose.
2. Clone this repository.
3. Generate a self-signed certificate:
   ```bash
   mkdir certs
   openssl req -x509 -newkey rsa:4096 -keyout certs/key.pem -out certs/cert.pem -days 365 -nodes -subj "/CN=localhost"
   ```

### Steps to Run the Project

1. **Start the Docker Compose Services:**

   ```bash
   docker-compose up --build
   ```

2. Access the Traefik dashboard:

   - URL: [http://localhost:8080](http://localhost:8080)

3. Test the API:

   - Base URL: [https://localhost](https://localhost)
   - Swagger documentation: [https://localhost/docs](https://localhost/docs)

4. To verify the CIDR configuration:

   - Ensure that only requests from the `192.168.100.0/24` subnet can access the `fastapi-app` service.

## **Components Overview**

### 1. **Network Infrastructure**

- **Controlled CIDR:**
  The project uses a controlled CIDR (`192.168.100.0/24`) for the `fast` network.

  ```yaml
  networks:
    fast:
      driver: bridge
      ipam:
        config:
          - subnet: 192.168.100.0/24
  ```

- **Load Balancer:**
  Traefik load-balances requests across replicas of the FastAPI app. This is achieved via:

  ```yaml
  deploy:
    replicas: 3
  ```

- **Networks:**
  The services are connected via `web`, `fast`, and `reverse` networks, ensuring proper separation and communication between Traefik and the FastAPI app.

### 2. **Security**

- **HTTPS Configuration:**
  Traefik is configured to serve the application over HTTPS using a self-signed certificate. Redirection from HTTP to HTTPS is enforced via the middleware `redirect-to-https`:

  ```yaml
  middlewares:
    redirect-to-https:
      redirectScheme:
        scheme: https
        permanent: true
  ```

- **Certificates:**
  Self-signed certificates are stored in the `certs` directory and mounted to the Traefik container.

### 3. **REST API**

- **Endpoints:**
  The API allows CRUD operations on a list of products:

  | Method | Endpoint        | Description                 |
  | ------ | --------------- | --------------------------- |
  | GET    | `/products`     | Fetch all products.         |
  | POST   | `/products`     | Add a new product.          |
  | PUT    | `/product/{id}` | Update an existing product. |
  | DELETE | `/product/{id}` | Delete a product.           |

- **HTTP Status Codes:**
  The API properly handles requests by returning correct HTTP status codes for success (e.g., `200 OK`) and errors (e.g., `404 Not Found`).

#### Example Request and Response:

1. **GET /products**:

   ```bash
   curl -X GET https://localhost/products --insecure
   ```

   **Response:**

   ```json
   []
   ```

2. **POST /products**:

   ```bash
   curl -X POST https://localhost/products -H "Content-Type: application/json" -d '{"id": 1, "name": "Laptop", "price": 999.99}' --insecure
   ```

   **Response:**

   ```json
   {
     "message": "Product created",
     "product": {
       "id": 1,
       "name": "Laptop",
       "price": 999.99
     }
   }
   ```

## **Project Configuration Details**

### docker-compose.yml

Defines services for the FastAPI app and Traefik.

- **FastAPI Service:**

  ```yaml
  labels:
    - "traefik.http.routers.fastapi-http.rule=Host(`localhost`)"
    - "traefik.http.routers.fastapi-http.middlewares=redirect-to-https"
    - "traefik.http.routers.fastapi-https.rule=Host(`localhost`)"
    - "traefik.http.routers.fastapi-https.entrypoints=websecure"
    - "traefik.http.routers.fastapi-https.tls=true"
  ```

- **Traefik Configuration:**

  ```yaml
  command:
    - "--entrypoints.web.address=:80"
    - "--entrypoints.websecure.address=:443"
  ```

### dynamic.yml

Specifies Traefik's routers, middleware, and TLS certificates.

- **Middleware for Redirection:**
  ```yaml
  middlewares:
    redirect-to-https:
      redirectScheme:
        scheme: https
        permanent: true
  ```

### main.py

Implements the REST API using FastAPI.

- **CRUD Endpoints:**

  ```python
  @app.get("/products")
  def get_products():
      return products

  @app.post("/products")
  def create_products(product: Product):
      products.append(product)
      return {"message": "Product created", "product": product}

  @app.put("/product/{product_id}")
  def update_product(product_id: int, updated_product: Product):
      ...
  ```

## **Testing**

1. **Verify Network CIDR:**
   Use `docker network inspect` to check that the `fast` network uses the `192.168.100.0/24` subnet:

   ```bash
   docker network inspect project_fast
   ```

2. **Test HTTPS Redirection:**
   Access `http://localhost/products` and confirm it redirects to `https://localhost/products`.

3. **Run API Tests:**
   Use tools like `curl` or Postman to test all API endpoints.

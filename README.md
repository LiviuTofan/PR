# [Lab 1: Web Scraper and Data Processing](https://github.com/LiviuTofan/PR/tree/main/Lab1)

This repository contains the implementation of **Lab 1**, where a web scraper was built to process product data from [xstore.md](https://xstore.md). The project features data validation, transformation, and serialization techniques.

## Features

### 1. Web Scraping
- Retrieves product names, prices, and additional data from product links.
- Extracted using a custom HTML parser and HTTP-formatted requests via a TCP socket.

### 2. Data Validation
- Ensures product data integrity using two validation checks.

### 3. Data Processing
- Applies **Map**, **Filter**, and **Reduce** functions:
  - Converts prices between EUR and MDL.
  - Filters products based on a specified price range.
  - Calculates the total cost of filtered products and appends a UTC timestamp.

### 4. Serialization
- Manual implementation of **JSON** and **XML** serialization.
- A custom serialization format was designed for this project.

### 5. Docker Setup
- Docker installation and configuration were completed as part of the project requirements.


# [Lab 2: Database and Application Development](https://github.com/LiviuTofan/PR/tree/main/Lab2) 

This repository contains the implementation of **Lab 2**, which builds upon the web scraping project from Lab 1 by integrating a database and additional functionalities like CRUD operations, WebSocket communication, and file synchronization.

## Features

### 1. Database Selection
- **SQLite** was chosen as the database for this project.

### 2. Data Model Design
- The database schema was designed based on the product data scraped in Lab 1.
- Interaction with the database was implemented using raw SQL queries.

### 3. CRUD Operations
- Implemented Create, Read, Update, and Delete operations via an HTTP interface.
- DELETE, PUT, and GET operations use query parameters "ID" to identify resources.

### 4. Pagination
- Added pagination to resource endpoints using `offset` and `limit` query parameters.

### 5. File Upload Handling
- Implemented a route/handler to accept **multipart/form-data** file uploads.
- Tested by uploading JSON files via Postman and scripts.

### 6. Chat Room using WebSocket
- Developed a chat room logic using the WebSocket protocol for real-time communication.

### 7. Docker Integration
- Used **Docker Compose** to run the SQLite database inside a Docker container.
- Configured the container to connect to the database server over a network.

### 8. Dockerfile for the Application
- Created a `Dockerfile` to containerize the application.
- Verified functionality using Docker commands.

### 9. TCP Server
- Implemented a separate TCP server to handle client connections and messages.

### 10. Synchronization Mechanism
- Coordinated the execution order of read and write operations on a shared file.
- Ensured that all write operations complete before read operations using synchronization mechanisms.
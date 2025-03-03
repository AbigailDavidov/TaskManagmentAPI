**TaskManagmentAPI**

I have implemented a well documented RESTful API for Task Management. The API allows users to create, update, read, and delete tasks. For this I used **Flask-RESTX** to generate interactive Swagger documentation for the Flask app**,** the code also includes **logging**, **basic authentication** and **unit tests**. I’ll also add some examples for requests and responses and link to SwaggerHub.

 **1\. Logging:**

Captures all important actions (fetching tasks, task creation, updates, deletions) and logs errors (such as invalid date format). This will be helpful for debugging or auditing the API behavior.

### **2\. Basic Authentication:**

The `@auth.verify_password` function checks for valid credentials and ensures only authorized users can interact with the API. Password stored securely (e.g., in environment variables) 

### **3\. Task Model & Data Handling:**

The task model uses `uuid` for generating unique task IDs, for identifying tasks uniquely. Also parsing the date and handling invalid date formats with a `ValueError` catch.

### **4\. Error Handling:**

* The `404` response for a task not found.  
* The `400` response for invalid date format.  
* The `409` response for conflict with existing task

### **Example Requests and Responses:**

## **1\. Create a Task (POST /tasks/)**

### **HTTP Request**

`POST /tasks/` 

`Authorization: Basic <Base64EncodedUsername:Password>`

`Content-Type: application/json`

`{`

    `"description": "Complete project report",`

    `"due_date": "2025-03-10",`

    `"status": "active"`

`}`

### **Response (201 Created)**

`{`

    `"id": "550e8400-e29b-41d4-a716-446655440000",`

    `"description": "Complete project report",`

    `"due_date": "2025-03-10",`

    `"status": "active"`

`}`

---

## **2\. Get All Tasks (GET /tasks/)**

### **HTTP Request**

`GET /tasks/` 

`Authorization: Basic <Base64EncodedUsername:Password>`

`Accept: application/json`

### **Response (200 OK)**

`[`

    `{`

        `"id": "550e8400-e29b-41d4-a716-446655440000",`

        `"description": "Complete project report",`

        `"due_date": "2025-03-10",`

        `"status": "active"`

    `}`

`]`

---

## **3\. Get a Task by ID (GET /tasks/{task\_id})**

### **HTTP Request**

`GET /tasks/550e8400-e29b-41d4-a716-446655440000` 

`Authorization: Basic <Base64EncodedUsername:Password>`

`Accept: application/json`

### **Response (200 OK)**

`{`

    `"id": "550e8400-e29b-41d4-a716-446655440000",`

    `"description": "Complete project report",`

    `"due_date": "2025-03-10",`

    `"status": "active"`

`}`

---

## **4\. Update a Task (PUT /tasks/{task\_id})**

### **HTTP Request**

`PUT /tasks/550e8400-e29b-41d4-a716-446655440000` 

`Authorization: Basic <Base64EncodedUsername:Password>`

`Content-Type: application/json`

`{`

    `"description": "Complete project report (Updated)",`

    `"due_date": "2025-03-15",`

    `"status": "completed"`

`}`

### **Response (200 OK)**

`{`

    `"id": "550e8400-e29b-41d4-a716-446655440000",`

    `"description": "Complete project report (Updated)",`

    `"due_date": "2025-03-15",`

    `"status": "completed"`

`}`

---

## **5\. Delete a Task (DELETE /tasks/{task\_id})**

### **HTTP Request**

`DELETE /tasks/550e8400-e29b-41d4-a716-446655440000` 

`Authorization: Basic <Base64EncodedUsername:Password>`

### **Response (204 No Content)**

*(No response body)*

---

## **6\. Handle Duplicate Task Creation (POST /tasks/)**

### **HTTP Request**

`POST /tasks/` 

`Authorization: Basic <Base64EncodedUsername:Password>`

`Content-Type: application/json`

`{`

    `"description": "Complete project report",`

    `"due_date": "2025-03-10",`

    `"status": "active"`

`}`

### **Response (409 Conflict)**

`{`

    `"message": "Conflict: Task with the same description, due date, and status already exists."`

`}`

**Link to SwaggerHub**\- [https://app.swaggerhub.com/apis/private-987/task-management\_api/1.0\#/](https://app.swaggerhub.com/apis/private-987/task-management_api/1.0#/)


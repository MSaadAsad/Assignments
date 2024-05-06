# REST API Endpoint Schema

## Authentication API

### Base: `/auth`

1. **Register User**
   - **Endpoint:** `POST /register`
   - **Request Body:**
     - `username`: string (required)
     - `email`: string (required)
     - `password`: string (required)
   - **Responses:**
     - `201 Created`: `message`: "Registered successfully"
     - `400 Bad Request`: `message`: "Username, email, and password required" or "Username already exists" or "Email already registered"

2. **Login User**
   - **Endpoint:** `POST /login`
   - **Request Body:**
     - `login_identifier`: string (required)
     - `password`: string (required)
   - **Responses:**
     - `200 OK`: `access_token`: string
     - `401 Unauthorized`: `message`: "Invalid credentials"

3. **Logout User**
   - **Endpoint:** `POST /logout`
   - **Headers:**
     - `Authorization`: string (required) - Bearer token
   - **Responses:**
     - `200 OK`: `message`: "Access token has been revoked"
     - `401 Unauthorized`: `message`: "Token is missing or invalid"
     - `500 Internal Server Error`: `message`: "Something went wrong"

## Document Processing API

### Base: `/docs`

1. **Create Document**
   - **Endpoint:** `POST /`
   - **Headers:** `Authorization`: Bearer Token
   - **Body:**
     - `title`: string
     - `text`: string
   - **Responses:**
     - `200 OK` with document processing results
     - `400 Bad Request` if title or text is missing

2. **Upload PDF**
   - **Endpoint:** `POST /pdf`
   - **Headers:** `Authorization`: Bearer Token
   - **Form Data:**
     - `pdf`: file
   - **Responses:**
     - `201 Created` with PDF processing results
     - `400 Bad Request` if file part is missing

3. **Delete Document**
   - **Endpoint:** `DELETE /:document_id`
   - **Headers:** `Authorization`: Bearer Token
   - **Responses:**
     - `200 OK` with message "Document deleted successfully"
     - `404 Not Found` if document not found or access denied

4. **Update Document**
   - **Endpoint:** `PUT /:document_id`
   - **Headers:** `Authorization`: Bearer Token
   - **Body:**
     - `title`: string (optional)
     - `text`: string (optional)
   - **Responses:**
     - `200 OK` with updated document details
     - `404 Not Found` if document not found or access denied

5. **Get Original Scores**
   - **Endpoint:** `GET /scores/:document_id`
   - **Headers:** `Authorization`: Bearer Token
   - **Responses:**
     - `200 OK` with original scores
     - `404 Not Found` if scores or document not found or access denied

6. **Get Document Details**
   - **Endpoint:** `GET /:document_id`
   - **Headers:** `Authorization`: Bearer Token
   - **Responses:**
     - `200 OK` with document details
     - `404 Not Found` if document not found or access denied

7. **Export Document as PDF**
   - **Endpoint:** `GET /pdf/:document_id`
   - **Headers:** `Authorization`: Bearer Token
   - **Responses:**
     - `200 OK` with the document as pdf
     - `404 Not Found` if document not found or access denied

## Search API

### Base: `/api`

1. **Search Documents**
   - **Endpoint:** `GET /search`
   - **Query Parameters:**
     - `q`: Query string
     - `page`: Page number (optional)
     - `limit`: Documents per page (optional)
   - **Responses:**
     - `200 OK` with paginated list of documents
     - `204 No Content` if no documents found
     - `200 OK` if no matching documents found

## Rewrite API

### Base: `/fix`

1. **Get Rewritten Sentences**
   - **Endpoint:** `GET /:document_id`
   - **Headers:** `Authorization`: Bearer Token
   - **Responses:**
     - `200 OK` with list of rewritten sentences
     - `404 Not Found` if document not found or access denied

2. **Accept Suggestion**
   - **Endpoint:** `PUT /:document_id/:sentence_id`
   - **Headers:** `Authorization`: Bearer Token
   - **Responses:**
     - `200 OK` with message "Sentence updated successfully"
     - `404 Not Found` if document or sentence not found or access denied

3. **Delete Suggestion**
   - **Endpoint:** `DELETE /<int:document_id>/<int:sentence_id>`
   - **Headers:** `Authorization`: Bearer Token
   - **Responses:**
     - `200 OK` with message "Sentence reset to original text successfully"
     - `404 Not Found` if document, text chunk, or sentence not found or access denied

4. **Accept All Suggestions**
   - **Endpoint:** `PUT /<int:document_id>/all`
   - **Headers:** `Authorization`: Bearer Token
   - **Responses:**
     - `200 OK` with message "All suggestions accepted successfully"
     - `404 Not Found` if document or text chunk not found or access denied

5. **Delete All Suggestions**
   - **Endpoint:** `DELETE /<int:document_id>/all`
   - **Headers:** `Authorization`: Bearer Token
   - **Responses:**
     - `200 OK` with message "All suggestions deleted successfully"
     - `404 Not Found` if document or text chunk not found or access denied
    

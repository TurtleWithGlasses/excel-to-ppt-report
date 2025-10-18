# DataDeck API Examples

This document provides practical examples for using the DataDeck API.

## Authentication

### 1. Register a New User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john.doe",
    "email": "john.doe@example.com",
    "password": "SecurePassword123!",
    "role": "user"
  }'
```

Response:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "username": "john.doe",
  "email": "john.doe@example.com",
  "role": "user",
  "created_at": "2024-01-15T10:30:00"
}
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john.doe&password=SecurePassword123!"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Note**: Save this token! You'll need it for authenticated requests.

---

## Client Management

### 3. Create a Client

```bash
curl -X POST "http://localhost:8000/api/v1/clients/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Acme Corporation",
    "industry": "Technology"
  }'
```

### 4. List All Clients

```bash
curl -X GET "http://localhost:8000/api/v1/clients/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 5. Get Specific Client

```bash
curl -X GET "http://localhost:8000/api/v1/clients/CLIENT_UUID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Template Management

### 6. Create a Simple Template

```bash
curl -X POST "http://localhost:8000/api/v1/templates/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "CLIENT_UUID",
    "name": "Monthly Sales Report",
    "structure": {
      "template_name": "Monthly Sales Report",
      "sections": [
        {
          "name": "Executive Summary",
          "type": "text_analysis",
          "data_source": ["Sheet1"],
          "ai_processing": true
        },
        {
          "name": "Sales Data",
          "type": "data_table",
          "data_source": ["Sheet1"]
        }
      ]
    }
  }'
```

### 7. Create a Complex Template

```bash
curl -X POST "http://localhost:8000/api/v1/templates/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d @examples/example_template.json
```

### 8. List Templates for a Client

```bash
curl -X GET "http://localhost:8000/api/v1/templates/?client_id=CLIENT_UUID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 9. Update a Template

```bash
curl -X PUT "http://localhost:8000/api/v1/templates/TEMPLATE_UUID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "is_active": false
  }'
```

---

## Data Upload

### 10. Upload Excel File

```bash
curl -X POST "http://localhost:8000/api/v1/data/upload" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/your/data.xlsx" \
  -F "client_id=CLIENT_UUID"
```

Response:
```json
{
  "id": "data-upload-uuid",
  "client_id": "CLIENT_UUID",
  "file_name": "data.xlsx",
  "file_path": "/app/data/uploads/...",
  "data_snapshot": {
    "file_name": "data.xlsx",
    "total_sheets": 2,
    "sheets": {
      "Sheet1": {
        "total_rows": 100,
        "total_columns": 5,
        "columns": ["Date", "Sales", "Region", "Product", "Amount"]
      }
    }
  },
  "uploaded_by": "user-uuid",
  "upload_date": "2024-01-15T10:45:00"
}
```

### 11. List Data Uploads

```bash
curl -X GET "http://localhost:8000/api/v1/data/?client_id=CLIENT_UUID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 12. Get Upload Details

```bash
curl -X GET "http://localhost:8000/api/v1/data/UPLOAD_UUID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Report Generation

### 13. Generate a Report

```bash
curl -X POST "http://localhost:8000/api/v1/reports/generate" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "CLIENT_UUID",
    "template_id": "TEMPLATE_UUID",
    "data_upload_id": "UPLOAD_UUID"
  }'
```

Response:
```json
{
  "id": "report-uuid",
  "client_id": "CLIENT_UUID",
  "template_id": "TEMPLATE_UUID",
  "data_upload_id": "UPLOAD_UUID",
  "status": "pending",
  "generated_by": "user-uuid",
  "generated_at": "2024-01-15T11:00:00"
}
```

**Status values**: `pending`, `processing`, `completed`, `failed`

### 14. Check Report Status

```bash
curl -X GET "http://localhost:8000/api/v1/reports/REPORT_UUID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 15. Download Report (when completed)

```bash
curl -X GET "http://localhost:8000/api/v1/reports/REPORT_UUID/download" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -o "my_report.pptx"
```

### 16. List All Reports

```bash
curl -X GET "http://localhost:8000/api/v1/reports/?client_id=CLIENT_UUID" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Python Examples

### Using Python `requests` library

```python
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000/api/v1"

# 1. Register and Login
def login(username, password):
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={"username": username, "password": password}
    )
    return response.json()["access_token"]

# Get token
token = login("john.doe", "SecurePassword123!")
headers = {"Authorization": f"Bearer {token}"}

# 2. Create a client
client_data = {
    "name": "My Company",
    "industry": "Technology"
}
response = requests.post(
    f"{BASE_URL}/clients/",
    headers=headers,
    json=client_data
)
client = response.json()
client_id = client["id"]

# 3. Create a template
template_data = {
    "client_id": client_id,
    "name": "Monthly Report",
    "structure": {
        "template_name": "Monthly Report",
        "sections": [
            {
                "name": "Summary",
                "type": "text_analysis",
                "data_source": ["Sheet1"],
                "ai_processing": True
            }
        ]
    }
}
response = requests.post(
    f"{BASE_URL}/templates/",
    headers=headers,
    json=template_data
)
template = response.json()
template_id = template["id"]

# 4. Upload data
files = {"file": open("data.xlsx", "rb")}
data = {"client_id": client_id}
response = requests.post(
    f"{BASE_URL}/data/upload",
    headers=headers,
    files=files,
    data=data
)
upload = response.json()
upload_id = upload["id"]

# 5. Generate report
report_data = {
    "client_id": client_id,
    "template_id": template_id,
    "data_upload_id": upload_id
}
response = requests.post(
    f"{BASE_URL}/reports/generate",
    headers=headers,
    json=report_data
)
report = response.json()
report_id = report["id"]

# 6. Check status and download
import time

while True:
    response = requests.get(
        f"{BASE_URL}/reports/{report_id}",
        headers=headers
    )
    status = response.json()["status"]
    print(f"Status: {status}")
    
    if status == "completed":
        # Download report
        response = requests.get(
            f"{BASE_URL}/reports/{report_id}/download",
            headers=headers
        )
        with open("output_report.pptx", "wb") as f:
            f.write(response.content)
        print("Report downloaded!")
        break
    elif status == "failed":
        print("Report generation failed!")
        break
    
    time.sleep(5)  # Wait 5 seconds before checking again
```

---

## JavaScript/Node.js Examples

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const BASE_URL = 'http://localhost:8000/api/v1';

// 1. Login
async function login(username, password) {
  const params = new URLSearchParams();
  params.append('username', username);
  params.append('password', password);
  
  const response = await axios.post(
    `${BASE_URL}/auth/login`,
    params
  );
  return response.data.access_token;
}

// 2. Upload file and generate report
async function generateReport() {
  const token = await login('john.doe', 'SecurePassword123!');
  const headers = { Authorization: `Bearer ${token}` };
  
  // Create client
  const clientRes = await axios.post(
    `${BASE_URL}/clients/`,
    { name: 'My Company', industry: 'Tech' },
    { headers }
  );
  const clientId = clientRes.data.id;
  
  // Upload file
  const formData = new FormData();
  formData.append('file', fs.createReadStream('data.xlsx'));
  formData.append('client_id', clientId);
  
  const uploadRes = await axios.post(
    `${BASE_URL}/data/upload`,
    formData,
    { headers: { ...headers, ...formData.getHeaders() } }
  );
  
  console.log('Upload successful:', uploadRes.data);
}

generateReport();
```

---

## Complete Workflow Example

Here's a complete workflow from start to finish:

```bash
# 1. Register
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@example.com","password":"Demo123!"}' | jq -r '.id')

# 2. Login
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/login" \
  -d "username=demo&password=Demo123!" | jq -r '.access_token')

# 3. Create Client
CLIENT_ID=$(curl -s -X POST "http://localhost:8000/api/v1/clients/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Demo Corp","industry":"Technology"}' | jq -r '.id')

# 4. Create Template
TEMPLATE_ID=$(curl -s -X POST "http://localhost:8000/api/v1/templates/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"client_id\":\"$CLIENT_ID\",\"name\":\"Demo Template\",\"structure\":{\"template_name\":\"Demo\",\"sections\":[{\"name\":\"Summary\",\"type\":\"text_analysis\",\"data_source\":[\"Sheet1\"],\"ai_processing\":true}]}}" | jq -r '.id')

# 5. Upload Data
UPLOAD_ID=$(curl -s -X POST "http://localhost:8000/api/v1/data/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@data.xlsx" \
  -F "client_id=$CLIENT_ID" | jq -r '.id')

# 6. Generate Report
REPORT_ID=$(curl -s -X POST "http://localhost:8000/api/v1/reports/generate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"client_id\":\"$CLIENT_ID\",\"template_id\":\"$TEMPLATE_ID\",\"data_upload_id\":\"$UPLOAD_ID\"}" | jq -r '.id')

# 7. Wait and Download
echo "Report ID: $REPORT_ID"
echo "Check status at: http://localhost:8000/api/v1/reports/$REPORT_ID"
echo "Download when ready: http://localhost:8000/api/v1/reports/$REPORT_ID/download"
```

---

## Tips

1. **Save your access token**: It expires after 30 minutes by default
2. **Check report status**: Report generation is asynchronous, poll the status endpoint
3. **Use jq**: For parsing JSON responses in bash (install with `brew install jq` or `apt-get install jq`)
4. **Test with curl**: Use `curl -v` for verbose output when debugging
5. **API Documentation**: Visit http://localhost:8000/docs for interactive API docs


# Navi Mumbai House Price Predictor - API Reference

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

JWT Bearer Token in Authorization header:
```
Authorization: Bearer <access_token>
```

---

## Endpoints

### 🔐 Authentication

#### Register User
```
POST /auth/register
```

**Request:**
```json
{
  "email": "user@example.com",
  "password": "secure_password",
  "full_name": "John Doe",
  "phone": "+919876543210",
  "user_type": "buyer"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "user_type": "buyer",
  "is_active": true,
  "created_at": "2026-02-23T10:00:00"
}
```

#### Login
```
POST /auth/login?email={email}&password={password}
```

**Response:** `200 OK`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer",
  "user": { ... }
}
```

---

### 🏠 Prediction (F-01, F-02)

#### Get Price Prediction
```
POST /prediction/predict
```

**Request:**
```json
{
  "locality_name": "Vashi",
  "bhk": 2,
  "carpet_area_sqft": 1200,
  "floor_number": 8,
  "total_floors": 15,
  "building_age_years": 5,
  "lift": true,
  "parking": true,
  "gym": true,
  "swimming_pool": false,
  "gated_society": true,
  "cctv": true
}
```

**Response:** `200 OK`
```json
{
  "id": 1,
  "locality_name": "Vashi",
  "bhk": 2,
  "carpet_area_sqft": 1200,
  "predicted_total_price": 144000000,
  "predicted_price_per_sqft": 120000,
  "confidence_score": 0.85,
  "lower_bound": 129600000,
  "upper_bound": 158400000,
  "model_version": "1.0",
  "created_at": "2026-02-23T10:00:00"
}
```

**Error Responses:**
- `400 Bad Request` - Invalid locality or missing required fields
- `500 Internal Server Error` - Prediction generation failed

#### Get Prediction History
```
GET /prediction/history/{locality_name}?limit=10
```

**Response:** `200 OK`
```json
{
  "predictions": [
    {
      "id": 100,
      "locality_name": "Vashi",
      "bhk": 2,
      "carpet_area_sqft": 1200,
      "predicted_total_price": 144000000,
      "predicted_price_per_sqft": 120000,
      "confidence_score": 0.85,
      "lower_bound": 129600000,
      "upper_bound": 158400000,
      "model_version": "1.0",
      "created_at": "2026-02-23T10:00:00"
    }
  ]
}
```

---

### 🏢 Properties (F-04)

#### Create Property
```
POST /properties/
```

**Request:**
```json
{
  "locality_id": 1,
  "name": "Sample Property",
  "bhk": 2,
  "carpet_area_sqft": 1200,
  "floor_number": 5,
  "total_floors": 15,
  "building_age_years": 3,
  "price": 144000000,
  "lift": true,
  "parking": true,
  "gym": true,
  "swimming_pool": false,
  "gated_society": true,
  "cctv": true,
  "source": "rera"
}
```

**Response:** `201 Created`
```json
{
  "id": 1,
  "locality_id": 1,
  "bhk": 2,
  "carpet_area_sqft": 1200,
  "price": 144000000,
  "price_per_sqft": 120000,
  "source": "rera",
  "created_at": "2026-02-23T10:00:00"
}
```

#### Get Property by ID
```
GET /properties/{property_id}
```

**Response:** `200 OK` (same as above)

#### Get Properties by Locality (Comparable Listings - F-04)
```
GET /properties/locality/{locality_id}?limit=20
```

**Response:** `200 OK`
```json
{
  "properties": [
    {
      "id": 1,
      "locality_id": 1,
      "bhk": 2,
      "carpet_area_sqft": 1200,
      "price": 144000000,
      "price_per_sqft": 120000,
      "source": "rera",
      "created_at": "2026-02-23T10:00:00"
    }
  ],
  "count": 1
}
```

---

### 📍 Localities (F-03)

#### Get All Localities
```
GET /localities/?skip=0&limit=20
```

**Response:** `200 OK`
```json
[
  {
    "id": 1,
    "name": "Kharghar",
    "node_type": "Residential",
    "metro_distance_km": 8.5,
    "highway_distance_km": 2.0,
    "avg_price_per_sqft": 85000,
    "transaction_volume_30days": 45,
    "avg_price_updated": "2026-02-23T10:00:00",
    "created_at": "2026-02-23T10:00:00"
  }
]
```

#### Get Locality Details
```
GET /localities/{locality_name}
```

**Response:** `200 OK`
```json
{
  "id": 2,
  "name": "Vashi",
  "node_type": "Mixed",
  "metro_distance_km": 0.5,
  "highway_distance_km": 3.0,
  "avg_price_per_sqft": 120000,
  "transaction_volume_30days": 120,
  "avg_price_updated": "2026-02-23T10:00:00",
  "created_at": "2026-02-23T10:00:00",
  "properties": []
}
```

#### Get Locality Statistics (Heatmap Data - F-03)
```
GET /localities/stats/all
```

**Response:** `200 OK`
```json
{
  "localities": [
    {
      "id": 1,
      "name": "Kharghar",
      "avg_price_per_sqft": 85000,
      "transaction_volume": 45,
      "metro_distance": 8.5
    },
    {
      "id": 2,
      "name": "Vashi",
      "avg_price_per_sqft": 120000,
      "transaction_volume": 120,
      "metro_distance": 0.5
    }
  ]
}
```

---

### 📈 Trends (F-05)

#### Get 6-Month Price Trend
```
GET /trends/{locality_name}/6m
```

**Response:** `200 OK`
```json
{
  "locality_name": "Vashi",
  "period_days": 180,
  "trend_data": [
    {
      "date": "2026-02-23T10:00:00",
      "avg_price_per_sqft": 120000,
      "transaction_count": 5
    }
  ]
}
```

#### Get 12-Month Price Trend
```
GET /trends/{locality_name}/12m
```

**Response:** `200 OK` (same structure, `period_days": 365`)

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Missing or invalid token |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Server error |

---

## Supported Localities

```
Kharghar, Vashi, Panvel, Nerul, Belapur, Airoli, Ulwe, Dronagiri,
CBD Belapur, Seawoods, Koparkhairane, Ghansoli, Kamothe, Taloje
```

---

## Rate Limiting

Currently no rate limiting implemented. Will be added in Phase 2.

---

## Pagination

Endpoints supporting pagination use:
- `skip` - Number of records to skip (default: 0)
- `limit` - Number of records to return (default: 20, max: 100)

---

## Examples

### cURL Examples

#### Get Prediction
```bash
curl -X POST http://localhost:8000/api/v1/prediction/predict \
  -H "Content-Type: application/json" \
  -d '{
    "locality_name": "Vashi",
    "bhk": 2,
    "carpet_area_sqft": 1200,
    "floor_number": 8,
    "total_floors": 15,
    "building_age_years": 5,
    "lift": true,
    "parking": true,
    "gym": true,
    "swimming_pool": false,
    "gated_society": true,
    "cctv": true
  }'
```

#### Get All Localities
```bash
curl http://localhost:8000/api/v1/localities/
```

#### Get 6-Month Trend
```bash
curl http://localhost:8000/api/v1/trends/Vashi/6m
```

---

## Interactive Documentation

Visit `http://localhost:8000/docs` for interactive API documentation with Swagger UI.

---

**Last Updated**: February 23, 2026

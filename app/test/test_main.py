# app/tests/test_main.py

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
import pytest
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
TEST_DATABASE_URL = os.getenv('TEST_DATABASE_URL')

def create_test_database():
    # Connect to the default database to create the test database
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()
    conn.execution_options(isolation_level="AUTOCOMMIT")
    # Drop the test database if it exists
    conn.execute(text("DROP DATABASE IF EXISTS test_database"))
    # Create the test database
    conn.execute(text("CREATE DATABASE test_database"))
    conn.close()
    engine.dispose()

    # Connect to the test database and enable PostGIS extension
    test_engine = create_engine(TEST_DATABASE_URL)
    test_conn = test_engine.connect()
    test_conn.execution_options(isolation_level="AUTOCOMMIT")
    test_conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
    test_conn.close()
    test_engine.dispose()

try:
    create_test_database()
except Exception as e:
    print(f"Test database creation skipped or failed: {e}")

# Set up the test engine and session
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the test database
Base.metadata.create_all(bind=engine)

# Dependency override to use the test database session
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Apply the dependency override
app.dependency_overrides[get_db] = override_get_db

# Initialize the TestClient with the app
client = TestClient(app)

# Fixture to run each test in a transaction and roll it back after
@pytest.fixture(scope='function', autouse=True)
def db_session():
    # Connect to the database and begin a transaction
    connection = engine.connect()
    transaction = connection.begin()
    # Bind an individual session to the connection
    db = TestingSessionLocal(bind=connection)

    # Override the get_db dependency to use this session
    app.dependency_overrides[get_db] = lambda: db

    yield

    # Roll back the transaction and close the connection after each test
    transaction.rollback()
    connection.close()
    db.close()

# Test functions start here

# Providers Endpoints

def test_create_provider():
    response = client.post(
        "/providers/",
        json={
            "name": "Test Provider",
            "email": "testprovider@example.com",
            "phone_number": "1234567890",
            "language": "English",
            "currency": "USD"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Provider"
    assert data["email"] == "testprovider@example.com"
    assert "id" in data

def test_get_providers():
    # Create a provider
    test_create_provider()
    response = client.get("/providers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_get_provider_by_id():
    # Create a provider
    response = client.post(
        "/providers/",
        json={
            "name": "Provider By ID",
            "email": "providerbyid@example.com",
            "phone_number": "0987654321",
            "language": "English",
            "currency": "USD"
        }
    )
    assert response.status_code == 200
    provider_id = response.json()["id"]

    # Retrieve the provider by ID
    response = client.get(f"/providers/{provider_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Provider By ID"

def test_update_provider():
    # Create a provider
    response = client.post(
        "/providers/",
        json={
            "name": "Provider to Update",
            "email": "updatetest@example.com",
            "phone_number": "2222222222",
            "language": "English",
            "currency": "USD"
        }
    )
    assert response.status_code == 200
    provider_id = response.json()["id"]

    # Update the provider's name
    response = client.put(
        f"/providers/{provider_id}",
        json={
            "name": "Updated Provider",
            "email": "updatetest@example.com",
            "phone_number": "2222222222",
            "language": "English",
            "currency": "USD"
        }
    )
    assert response.status_code == 200
    updated_provider = response.json()
    assert updated_provider["name"] == "Updated Provider"

def test_delete_provider():
    # Create a provider
    response = client.post(
        "/providers/",
        json={
            "name": "Provider to Delete",
            "email": "deletetest@example.com",
            "phone_number": "3333333333",
            "language": "English",
            "currency": "USD"
        }
    )
    assert response.status_code == 200
    provider_id = response.json()["id"]

    # Delete the provider
    response = client.delete(f"/providers/{provider_id}")
    assert response.status_code == 200

    # Verify the provider no longer exists
    response = client.get(f"/providers/{provider_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Provider not found"

# Service Areas Endpoints

def test_create_service_area():
    # Create a provider
    response = client.post(
        "/providers/",
        json={
            "name": "Service Area Provider",
            "email": "serviceareaprovider@example.com",
            "phone_number": "4444444444",
            "language": "English",
            "currency": "USD"
        }
    )
    provider_id = response.json()["id"]

    # Create a service area for the provider
    response = client.post(
        f"/providers/{provider_id}/service_areas/",
        json={
            "name": "Test Service Area",
            "price": 150.0,
            "geojson": "{\"type\": \"Polygon\", \"coordinates\": [[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]}"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Service Area"
    assert "id" in data

def test_get_service_areas():
    # Create a service area
    test_create_service_area()
    response = client.get("/service_areas/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1

def test_get_service_area_by_id():
    # Create a provider and service area
    response = client.post(
        "/providers/",
        json={
            "name": "Service Area By ID Provider",
            "email": "serviceareabyid@example.com",
            "phone_number": "5555555555",
            "language": "English",
            "currency": "USD"
        }
    )
    provider_id = response.json()["id"]

    response = client.post(
        f"/providers/{provider_id}/service_areas/",
        json={
            "name": "Service Area By ID",
            "price": 200.0,
            "geojson": "{\"type\": \"Polygon\", \"coordinates\": [[[1, 1], [1, 2], [2, 2], [2, 1], [1, 1]]]}"
        }
    )
    service_area_id = response.json()["id"]

    # Retrieve the service area by ID
    response = client.get(f"/service_areas/{service_area_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Service Area By ID"

def test_update_service_area():
    # Create a provider and service area
    response = client.post(
        "/providers/",
        json={
            "name": "Provider for Update Service Area",
            "email": "updateservicearea@example.com",
            "phone_number": "6666666666",
            "language": "English",
            "currency": "USD"
        }
    )
    provider_id = response.json()["id"]

    response = client.post(
        f"/providers/{provider_id}/service_areas/",
        json={
            "name": "Service Area to Update",
            "price": 250.0,
            "geojson": "{\"type\": \"Polygon\", \"coordinates\": [[[2, 2], [2, 3], [3, 3], [3, 2], [2, 2]]]}"
        }
    )
    service_area_id = response.json()["id"]

    # Update the service area's price
    response = client.put(
        f"/service_areas/{service_area_id}",
        json={
            "name": "Service Area to Update",
            "price": 300.0,
            "geojson": "{\"type\": \"Polygon\", \"coordinates\": [[[2, 2], [2, 3], [3, 3], [3, 2], [2, 2]]]}"
        }
    )
    assert response.status_code == 200
    updated_service_area = response.json()
    assert updated_service_area["price"] == 300.0

def test_delete_service_area():
    # Create a provider and service area
    response = client.post(
        "/providers/",
        json={
            "name": "Provider for Delete Service Area",
            "email": "deleteservicearea@example.com",
            "phone_number": "7777777777",
            "language": "English",
            "currency": "USD"
        }
    )
    provider_id = response.json()["id"]

    response = client.post(
        f"/providers/{provider_id}/service_areas/",
        json={
            "name": "Service Area to Delete",
            "price": 350.0,
            "geojson": "{\"type\": \"Polygon\", \"coordinates\": [[[3, 3], [3, 4], [4, 4], [4, 3], [3, 3]]]}"
        }
    )
    service_area_id = response.json()["id"]

    # Delete the service area
    response = client.delete(f"/service_areas/{service_area_id}")
    assert response.status_code == 200

    # Verify the service area no longer exists
    response = client.get(f"/service_areas/{service_area_id}")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Service Area not found"

# Geospatial Endpoint

def test_search_service_area():
    # Create a provider and service area
    response = client.post(
        "/providers/",
        json={
            "name": "Search Provider",
            "email": "searchprovider@example.com",
            "phone_number": "8888888888",
            "language": "English",
            "currency": "USD"
        }
    )
    provider_id = response.json()["id"]

    response = client.post(
        f"/providers/{provider_id}/service_areas/",
        json={
            "name": "Search Service Area",
            "price": 400.0,
            "geojson": "{\"type\": \"Polygon\", \"coordinates\": [[[10, 10], [10, 20], [20, 20], [20, 10], [10, 10]]]}"
        }
    )
    assert response.status_code == 200

    # Search for a point inside the service area
    response = client.get("/search/?lat=15&lng=15")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    found = any(item["service_area_name"] == "Search Service Area" for item in data)
    assert found

# Additional tests for invalid inputs and edge cases

def test_create_provider_invalid_email():
    response = client.post(
        "/providers/",
        json={
            "name": "Invalid Email Provider",
            "email": "invalid-email",
            "phone_number": "9999999999",
            "language": "English",
            "currency": "USD"
        }
    )
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["msg"] == "value is not a valid email address"

def test_create_service_area_invalid_geojson():
    # Create a provider
    response = client.post(
        "/providers/",
        json={
            "name": "Invalid GeoJSON Provider",
            "email": "invalidgeojson@example.com",
            "phone_number": "1010101010",
            "language": "English",
            "currency": "USD"
        }
    )
    provider_id = response.json()["id"]

    # Attempt to create a service area with invalid GeoJSON
    response = client.post(
        f"/providers/{provider_id}/service_areas/",
        json={
            "name": "Invalid GeoJSON Service Area",
            "price": 100.0,
            "geojson": "Invalid GeoJSON String"
        }
    )
    assert response.status_code == 422
    data = response.json()
    assert data["detail"] == "Invalid GeoJSON format"

def test_search_no_service_area_found():
    # Search for a point outside any service area
    response = client.get("/search/?lat=100&lng=100")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

def test_get_nonexistent_provider():
    response = client.get("/providers/99999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Provider not found"

def test_get_nonexistent_service_area():
    response = client.get("/service_areas/99999")
    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "Service Area not found"

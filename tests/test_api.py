from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["service"] == "AeroCopilot API"
    assert data["docs"] == "/docs"
    assert data["search"] == "/search"


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert data["service"] == "AeroCopilot API"


def test_documents():

    response = client.get("/documents")

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "documents" in data

    assert data["count"] >= 1


def test_empty_question():

    response = client.post(
        "/ask",
        json={
            "question": "",
            "k": 4
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Question cannot be empty."


def test_invalid_k():

    response = client.post(
        "/ask",
        json={
            "question": "What should be checked during a hydraulic system inspection?",
            "k": 20
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "k must be between 1 and 10."


def test_search():

    response = client.post(
        "/search",
        json={
            "query": "hydraulic system inspection",
            "k": 3
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["query"] == "hydraulic system inspection"
    assert data["count"] > 0
    assert len(data["results"]) > 0

    first_result = data["results"][0]

    assert "text" in first_result
    assert "source" in first_result
    assert "page" in first_result
    assert "score" in first_result


def test_empty_search():

    response = client.post(
        "/search",
        json={
            "query": "",
            "k": 4
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "Query cannot be empty."


def test_invalid_search_k():

    response = client.post(
        "/search",
        json={
            "query": "hydraulic inspection",
            "k": 20
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"] == "k must be between 1 and 10."
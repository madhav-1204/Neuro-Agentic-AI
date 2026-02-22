"""
Backend API tests — run with: pytest tests/
"""
import pytest
from httpx import AsyncClient, ASGITransport
from main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.anyio
async def test_health(client):
    resp = await client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"


@pytest.mark.anyio
async def test_analyze_no_file(client):
    """POST /analyze without a file should return 422."""
    resp = await client.post("/analyze")
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_analyze_invalid_extension(client):
    """Upload a .txt file — should be rejected."""
    resp = await client.post(
        "/analyze",
        files={"file": ("test.txt", b"not an image", "text/plain")},
    )
    assert resp.status_code == 400


@pytest.mark.anyio
async def test_auth_google_invalid_token(client):
    """POST /auth/google with an invalid token should fail."""
    resp = await client.post(
        "/auth/google",
        json={"token": "invalid-token"},
    )
    assert resp.status_code in (400, 401, 500)

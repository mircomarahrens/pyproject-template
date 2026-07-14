from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from pyproject_template.api.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}


def test_lifespan_shutdown_with_providers():
    mock_trace_provider = MagicMock()
    mock_meter_provider = MagicMock()

    # Set the providers on app.state
    app.state.trace_provider = mock_trace_provider
    app.state.meter_provider = mock_meter_provider

    try:
        with TestClient(app) as test_client:
            response = test_client.get("/")
            assert response.status_code == 200

        # Verify the shutdown methods were called
        mock_trace_provider.shutdown.assert_called_once()
        mock_meter_provider.shutdown.assert_called_once()
    finally:
        # Clean up
        if hasattr(app.state, "trace_provider"):
            delattr(app.state, "trace_provider")
        if hasattr(app.state, "meter_provider"):
            delattr(app.state, "meter_provider")


def test_lifespan_shutdown_without_providers():
    # Make sure they are not on app.state
    if hasattr(app.state, "trace_provider"):
        delattr(app.state, "trace_provider")
    if hasattr(app.state, "meter_provider"):
        delattr(app.state, "meter_provider")

    with TestClient(app) as test_client:
        response = test_client.get("/")
        assert response.status_code == 200

    # Asserting that no exception is raised and code passes smoothly

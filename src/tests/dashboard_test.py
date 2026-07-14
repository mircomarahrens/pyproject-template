import importlib
import sys
from unittest.mock import MagicMock

import pytest


@pytest.fixture
def mock_streamlit(monkeypatch):
    mock_st = MagicMock()

    # st.tabs returns 3 items
    mock_st.tabs.return_value = [MagicMock(), MagicMock(), MagicMock()]

    # st.columns returns appropriate length list
    def mock_columns(arg):
        n = len(arg) if isinstance(arg, list) else int(arg)
        return [MagicMock() for _ in range(n)]

    mock_st.columns.side_effect = mock_columns

    # Default values for inputs
    mock_st.sidebar.text_input.return_value = "http://localhost:8000"
    mock_st.number_input.side_effect = lambda *args, **kwargs: kwargs.get("value", 0)
    mock_st.text_input.side_effect = lambda *args, **kwargs: kwargs.get("value", "")

    # Default button behavior (all unclicked)
    mock_st.button.return_value = False

    # Mock progress and empty for elements
    mock_st.progress.return_value = MagicMock()
    mock_st.empty.return_value = MagicMock()

    monkeypatch.setitem(sys.modules, "streamlit", mock_st)
    return mock_st


def _load_dashboard():
    if "pyproject_template.dashboard.main" in sys.modules:
        importlib.reload(sys.modules["pyproject_template.dashboard.main"])
    else:
        importlib.import_module("pyproject_template.dashboard.main")


def test_dashboard_initial_render(mock_streamlit):
    # Test importing the dashboard for the first time
    _load_dashboard()

    # Check that basic setup was called
    mock_streamlit.set_page_config.assert_called_once()
    mock_streamlit.tabs.assert_called_once()


def test_dashboard_addition_success(mock_streamlit, monkeypatch):
    mock_st = mock_streamlit

    # Mock "Calculate Addition" button to be clicked
    mock_st.button.side_effect = (
        lambda label, *args, **kwargs: label == "Calculate Addition"
    )

    # Mock requests.get
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = 42
    mock_get = MagicMock(return_value=mock_response)
    monkeypatch.setattr("requests.get", mock_get)

    _load_dashboard()
    mock_st.success.assert_any_call("Result from API: **42**")


def test_dashboard_addition_failure(mock_streamlit, monkeypatch):
    mock_st = mock_streamlit
    mock_st.button.side_effect = (
        lambda label, *args, **kwargs: label == "Calculate Addition"
    )

    # Mock requests.get to return non-200
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get = MagicMock(return_value=mock_response)
    monkeypatch.setattr("requests.get", mock_get)

    _load_dashboard()
    mock_st.error.assert_any_call("Error status code: 500")


def test_dashboard_addition_exception(mock_streamlit, monkeypatch):
    mock_st = mock_streamlit
    mock_st.button.side_effect = (
        lambda label, *args, **kwargs: label == "Calculate Addition"
    )

    # Mock requests.get to raise exception
    mock_get = MagicMock(side_effect=Exception("Connection refused"))
    monkeypatch.setattr("requests.get", mock_get)

    _load_dashboard()
    mock_st.error.assert_any_call(
        "Could not connect to FastAPI server at http://localhost:8000. Verify that it is running."
    )


def test_dashboard_item_success(mock_streamlit, monkeypatch):
    mock_st = mock_streamlit
    mock_st.button.side_effect = lambda label, *args, **kwargs: label == "Lookup Item"

    # Mock requests.get
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"item_id": 42, "q": "streamlit-showcase"}
    mock_get = MagicMock(return_value=mock_response)
    monkeypatch.setattr("requests.get", mock_get)

    _load_dashboard()
    mock_st.json.assert_called_with({"item_id": 42, "q": "streamlit-showcase"})


def test_dashboard_item_success_no_query(mock_streamlit, monkeypatch):
    mock_st = mock_streamlit
    mock_st.button.side_effect = lambda label, *args, **kwargs: label == "Lookup Item"
    mock_st.text_input.side_effect = (
        lambda label, *args, **kwargs: ""
        if "Query Parameter" in label
        else kwargs.get("value", "")
    )

    # Mock requests.get
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"item_id": 42, "q": None}
    mock_get = MagicMock(return_value=mock_response)
    monkeypatch.setattr("requests.get", mock_get)

    _load_dashboard()
    mock_st.json.assert_called_with({"item_id": 42, "q": None})


def test_dashboard_item_failure(mock_streamlit, monkeypatch):
    mock_st = mock_streamlit
    mock_st.button.side_effect = lambda label, *args, **kwargs: label == "Lookup Item"

    # Mock requests.get to return non-200
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_get = MagicMock(return_value=mock_response)
    monkeypatch.setattr("requests.get", mock_get)

    _load_dashboard()
    mock_st.error.assert_any_call("Error status code: 404")


def test_dashboard_item_exception(mock_streamlit, monkeypatch):
    mock_st = mock_streamlit
    mock_st.button.side_effect = lambda label, *args, **kwargs: label == "Lookup Item"

    # Mock requests.get to raise exception
    mock_get = MagicMock(side_effect=Exception("Connection refused"))
    monkeypatch.setattr("requests.get", mock_get)

    _load_dashboard()
    mock_st.error.assert_any_call(
        "Could not connect to FastAPI server at http://localhost:8000. Verify that it is running."
    )


def test_dashboard_stream_success(mock_streamlit, monkeypatch):
    mock_st = mock_streamlit
    mock_st.button.side_effect = (
        lambda label, *args, **kwargs: label == "🚀 Start Event Stream"
    )

    # Mock time.sleep to avoid wait
    monkeypatch.setattr("time.sleep", lambda x: None)

    # Mock requests.get with stream=True and iter_lines
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.iter_lines.return_value = [b"0\n", b"1\n", b"2\n", b"", b"3\n"]
    mock_get = MagicMock(return_value=mock_response)
    monkeypatch.setattr("requests.get", mock_get)

    _load_dashboard()
    mock_st.success.assert_any_call("Successfully completed event streaming session.")


def test_dashboard_stream_failure(mock_streamlit, monkeypatch):
    mock_st = mock_streamlit
    mock_st.button.side_effect = (
        lambda label, *args, **kwargs: label == "🚀 Start Event Stream"
    )

    # Mock requests.get returning non-200
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get = MagicMock(return_value=mock_response)
    monkeypatch.setattr("requests.get", mock_get)

    _load_dashboard()
    mock_st.error.assert_any_call("Failed connection: Status 500")


def test_dashboard_stream_exception(mock_streamlit, monkeypatch):
    mock_st = mock_streamlit
    mock_st.button.side_effect = (
        lambda label, *args, **kwargs: label == "🚀 Start Event Stream"
    )

    # Mock requests.get raising exception
    mock_get = MagicMock(side_effect=Exception("Connection reset"))
    monkeypatch.setattr("requests.get", mock_get)

    _load_dashboard()
    mock_st.error.assert_any_call(
        "Could not reach Backend at http://localhost:8000/test. Verify your FastAPI server is started."
    )

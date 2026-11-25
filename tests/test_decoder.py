from metacyc_pathway_decoder import get_pathway_name


def test_get_pathway_name_exists():
    assert callable(get_pathway_name)

from unittest.mock import Mock
from metacyc_pathway_decoder import get_pathway_name


def test_get_pathway_name_exists():
    assert callable(get_pathway_name)


def test_get_pathway_name_extracts_name():

    mock_session = Mock()
    mock_response = Mock()

    mock_response.headers = {
        "Content-Type": "application/xml"
    }

    mock_response.content = b"""
    <ptools-xml>
        <Pathway>
            <common-name>aerobic respiration I</common-name>
        </Pathway>
    </ptools-xml>
    """

    mock_session.get.return_value = mock_response

    result = get_pathway_name(
        "PWY-3781",
        mock_session
    )

    assert result == "aerobic respiration I"

def test_get_pathway_name_missing_name():

    mock_session = Mock()
    mock_response = Mock()

    mock_response.headers = {
        "Content-Type": "application/xml"
    }

    mock_response.content = b"""
    <ptools-xml>
        <Pathway>
        </Pathway>
    </ptools-xml>
    """

    mock_session.get.return_value = mock_response

    result = get_pathway_name(
        "PWY-3781",
        mock_session
    )

    assert result is None

import requests


def test_get_pathway_name_http_error():

    mock_session = Mock()
    mock_response = Mock()

    mock_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError("404 Not Found")
    )

    mock_session.get.return_value = mock_response

    try:
        get_pathway_name("INVALID-PWY-12345", mock_session)
    except requests.exceptions.HTTPError:
        pass
    else:
        assert False, "Expected HTTPError was not raised"

def test_get_pathway_name_authentication_error():

    mock_session = Mock()
    mock_response = Mock()

    mock_response.status_code = 200
    mock_response.url = (
        "https://websvc.biocyc.org/account-required.shtml"
    )

    mock_response.headers = {
        "Content-Type": "text/html"
    }

    mock_session.get.return_value = mock_response

    try:
        get_pathway_name("PWY-3781", mock_session)
    except PermissionError as error:
        assert "authentication required" in str(error).lower()
    else:
        assert False, "Expected PermissionError was not raised"

from metacyc_pathway_decoder import get_pathway_names


def test_get_pathway_names_bulk():

    mock_session = Mock()

    xml_responses = [
        b"""
        <ptools-xml>
            <Pathway>
                <common-name>Pathway One</common-name>
            </Pathway>
        </ptools-xml>
        """,
        b"""
        <ptools-xml>
            <Pathway>
                <common-name>Pathway Two</common-name>
            </Pathway>
        </ptools-xml>
        """
    ]

    mock_responses = []

    for xml in xml_responses:
        response = Mock()
        response.headers = {
            "Content-Type": "application/xml"
        }
        response.content = xml
        mock_responses.append(response)

    mock_session.get.side_effect = mock_responses

    results = get_pathway_names(
        ["PWY-3781", "PWY-5973"],
        mock_session,
        delay=0,
        verbose=False
    )

    assert len(results) == 2
    assert results[0]["Pathway_Name"] == "Pathway One"
    assert results[1]["Pathway_Name"] == "Pathway Two"

def test_bulk_mixed_results():

    mock_session = Mock()

    success_response = Mock()
    success_response.headers = {
        "Content-Type": "application/xml"
    }
    success_response.content = b"""
    <ptools-xml>
        <Pathway>
            <common-name>Pathway One</common-name>
        </Pathway>
    </ptools-xml>
    """

    failed_response = Mock()
    failed_response.raise_for_status.side_effect = (
        requests.exceptions.HTTPError("404 Not Found")
    )

    mock_session.get.side_effect = [
        success_response,
        failed_response
    ]

    results = get_pathway_names(
        ["PWY-3781", "INVALID-PWY-12345"],
        mock_session,
        delay=0,
        verbose=False
    )

    assert len(results) == 2
    assert results[0]["Status"] == "success"
    assert results[1]["Status"] == "failed"
    assert results[1]["Pathway_Name"] is None

def test_bulk_negative_delay():

    mock_session = Mock()

    try:
        get_pathway_names(
            ["PWY-3781"],
            mock_session,
            delay=-1,
            verbose=False
        )
    except ValueError:
        pass
    else:
        assert False, "Expected ValueError"


def test_bulk_invalid_delay_type():

    mock_session = Mock()

    try:
        get_pathway_names(
            ["PWY-3781"],
            mock_session,
            delay="one",
            verbose=False
        )
    except TypeError:
        pass
    else:
        assert False, "Expected TypeError"

def test_bulk_empty_input():

    mock_session = Mock()

    results = get_pathway_names(
        [],
        mock_session,
        delay=0,
        verbose=False
    )

    assert results == []
    mock_session.get.assert_not_called()
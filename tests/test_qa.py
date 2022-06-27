import pytest
from aleph_alpha_client.aleph_alpha_client import AlephAlphaClient
from aleph_alpha_client.document import Document
from aleph_alpha_client.qa import QaRequest

from tests.common import client, model


def test_qa(client: AlephAlphaClient, model: str):
    # given a client
    assert model in map(lambda model: model["name"], client.available_models())

    # when posting a QA request with a QaRequest object
    request = QaRequest(
        query="Who likes pizza?",
        documents=[Document.from_prompt(["Andreas likes pizza."])],
    )

    response = client.qa(
        model,
        hosting="cloud",
        request=request,
    )

    # the response should exist and be in the form of a named tuple class
    assert len(response.answers) == 1
    assert response.model_version is not None


def test_qa_no_answer_found(client: AlephAlphaClient, model: str):
    # given a client
    assert model in map(lambda model: model["name"], client.available_models())

    # when posting a QA request with a QaRequest object
    request = QaRequest(
        query="Who likes pizza?",
        documents=[],
    )

    response = client.qa(
        model,
        hosting="cloud",
        request=request,
    )

    # the response should exist and be in the form of a named tuple class
    assert len(response.answers) == 0
    assert response.model_version is not None


def test_qa_with_explicit_parameters(client: AlephAlphaClient, model: str):
    # given a client
    assert model in map(lambda model: model["name"], client.available_models())

    # when posting a QA request with explicit parameters
    response = client.qa(
        model,
        hosting="cloud",
        query="Who likes pizza?",
        documents=[Document.from_prompt(["Andreas likes pizza."])],
    )

    # The response should exist in the form of a json dict
    assert len(response["answers"]) == 1
    assert response["model_version"] is not None


def test_qa_fails(client: AlephAlphaClient, model: str):
    # given a client
    assert model in map(lambda model: model["name"], client.available_models())

    # when posting an illegal request
    request = QaRequest(
        query="Who likes pizza?",
        documents=[Document.from_prompt(["Andreas likes pizza."]) for _ in range(21)],
    )

    # then we expect an exception tue to a bad request response from the API
    with pytest.raises(ValueError) as e:
        response = client.qa(
            model,
            hosting="cloud",
            request=request,
        )

    assert e.value.args[0] == 400

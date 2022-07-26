from enum import Enum
from typing import (
    Any,
    Dict,
    List,
    Literal,
    NamedTuple,
    Optional,
    Tuple,
)
from aleph_alpha_client.prompt import Prompt


class EmbeddingRequest(NamedTuple):
    """
    Embeds a text and returns vectors that can be used for downstream tasks (e.g. semantic similarity) and models (e.g. classifiers).

    Parameters:
        prompt
            The text and/or image(s) to be embedded.

        layers
            A list of layer indices from which to return embeddings.
                * Index 0 corresponds to the word embeddings used as input to the first transformer layer
                * Index 1 corresponds to the hidden state as output by the first transformer layer, index 2 to the output of the second layer etc.
                * Index -1 corresponds to the last transformer layer (not the language modelling head), index -2 to the second last layer etc.

        pooling
            Pooling operation to use.
            Pooling operations include:
                * mean: aggregate token embeddings across the sequence dimension using an average
                * max: aggregate token embeddings across the sequence dimension using a maximum
                * last_token: just use the last token
                * abs_max: aggregate token embeddings across the sequence dimension using a maximum of absolute values

        type
            Type of the embedding (e.g. symmetric or asymmetric)

        tokens
            Flag indicating whether the tokenized prompt is to be returned (True) or not (False)

    """

    prompt: Prompt
    layers: List[int]
    pooling: List[str]
    type: Optional[str] = None
    tokens: bool = False


class EmbeddingResponse(NamedTuple):
    model_version: str
    embeddings: Optional[Dict[Tuple[str, str], List[float]]]
    tokens: Optional[List[str]]

    @staticmethod
    def from_json(json: Dict[str, Any]) -> "EmbeddingResponse":
        return EmbeddingResponse(
            model_version=json["model_version"],
            embeddings={
                (layer, pooling): embedding
                for layer, pooling_dict in json["embeddings"].items()
                for pooling, embedding in pooling_dict.items()
            },
            tokens=json.get("tokens"),
        )


class SemanticRepresentation(Enum):
    """
    Available types of semantic representations that prompts can be embedded with.
    """

    Symmetric = "symmetric"
    """
    `Symmetric` is useful for comparing prompts to each other, in use cases such as clustering, classification, similarity, etc. `Symmetric` embeddings should be compared with other `Symmetric` embeddings.
    """
    Document = "document"
    """
    `Document` and `Query` are used together in use cases such as search where you want to compare shorter queries against larger documents.

    `Document` embeddings are optimized for larger pieces of text to compare queries against.
    """
    Query = "query"
    """
    `Document` and `Query` are used together in use cases such as search where you want to compare shorter queries against larger documents.

    `Query` embeddings are optimized for shorter texts, such as questions or keywords.
    """


class SemanticEmbeddingRequest(NamedTuple):
    """
    Embeds a text and returns vectors that can be used for downstream tasks (e.g. semantic similarity) and models (e.g. classifiers).
    """

    prompt: Prompt
    """
    The text and/or image(s) to be embedded.
    """
    representation: SemanticRepresentation
    """
    Semantic representation to embed the prompt with.
    """
    size: Optional[Literal[128, 5120]] = None
    """
    Options available: 128 5120
    Default: 5120
    The number of dimensions in the embedding. Default behavior is to return the full, 5120 dimension, embedding.

    The 128 size is expected to have a small drop in accuracy performance (4-6%), with the benefit of being much smaller, which makes comparing these embeddings much faster for use cases where speed is critical.

    The 128 size also can perform better if you are embedding really short texts or documents.
    """


class SemanticEmbeddingResponse(NamedTuple):
    model_version: str
    embedding: List[float]

    @staticmethod
    def from_json(json: Dict[str, Any]) -> "SemanticEmbeddingResponse":
        return SemanticEmbeddingResponse(
            model_version=json["model_version"], embedding=json["embedding"]
        )

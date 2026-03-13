from llm.llm_client import LLMClient


def test_llm_generate_response():
    client = LLMClient()

    response = client.generate("Reply in one sentence: what is a wellness risk summary?")

    assert response is not None
    assert isinstance(response, str)
    assert len(response.strip()) > 0
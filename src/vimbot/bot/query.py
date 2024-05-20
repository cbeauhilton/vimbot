import llm  # type: ignore[attr-defined]
from ..config import DEV_MODE, TMP_OUT_FILE_PATH, PROMPT_FILE_PATH
from .process_response import add_target_blank, process_markdown


def process_query(query: str, model_name: str, RAG) -> str:  # type: ignore[unknown]
    model = llm.get_model(model_name)  # type: ignore[type-partially-unknown]

    k = 10
    if DEV_MODE:
        k = 2

    retrieved = " ".join([d["content"] for d in RAG.search(query, k=k)])  # type: ignore[type-partially-unknown]
    with open(TMP_OUT_FILE_PATH, "w") as f:
        _ = f.write(retrieved)

    with open(PROMPT_FILE_PATH, "r") as prompt_file:
        prompt_text = prompt_file.read()

    system_prompt = prompt_text + "\n" + retrieved

    response = model.prompt(query, system=system_prompt, temperature=0).text()  # type: ignore[type-partially-unknown]

    response = add_target_blank(process_markdown(response))  # type: ignore[call-response)

    return response

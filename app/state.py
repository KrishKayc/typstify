from typing import TypedDict, List

class AgentState(TypedDict):
    original_pdf_path: str
    original_images: List[str]
    compiled_images: List[str]
    typst_code: str
    compilation_success: bool
    compilation_error: str
    feedback: str
    satisfied: bool
    iterations: int

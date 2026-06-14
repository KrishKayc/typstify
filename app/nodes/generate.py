import time
import re
import codecs
from langchain_core.messages import HumanMessage, SystemMessage
from app.state import AgentState

def clean_code(text: str) -> str:
    """Extracts code from markdown blocks and unescapes common LLM artifacts."""
    # 1. Try to find content between ```typst and ``` or just ``` and ```
    # Use re.DOTALL to match across multiple lines
    pattern = r"```(?:typst)?\n?(.*?)\n?```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        text = match.group(1)
    
    # 2. Handle escape sequences (like literal \n, \t, etc.)
    try:
        # Use unicode_escape to handle all standard escape characters
        # We encode then decode to apply the escape rules
        text = codecs.decode(text.encode('utf-8'), 'unicode_escape')
    except Exception:
        # Fallback if there's a decoding error
        text = text.replace('\\n', '\n').replace('\\t', '\t')
    
    return text.strip()

def generate_typst_node(state: AgentState, llm):
    """Generates or updates Typst code based on original PDF and feedback."""
    if state['iterations'] > 0:
        print("Waiting 5 seconds to avoid rate limits...")
        time.sleep(5)
    
    print(f"--- GENERATING TYPST (Iteration {state['iterations'] + 1}) ---")
    
    images = state['original_images']
    feedback = state.get('feedback', "")
    comp_error = state.get('compilation_error', "")
    
    prompt = "Convert the attached PDF pages into a Typst template that matches the layout and content exactly. "
    
    if state['typst_code']:
        prompt += f"\n\nHere is the CURRENT Typst code that needs improvement:\n```typst\n{state['typst_code']}\n```"

    if comp_error:
        print(f"Including Comp Error in prompt: {comp_error[:100]}...")
        prompt += f"\n\nCRITICAL: The code above failed to compile with this error:\n{comp_error}\nPlease fix the syntax or structural errors first."
    
    if feedback:
        print(f"Including Visual Feedback in prompt: {feedback[:100]}...")
        prompt += f"\n\nPrevious visual feedback to address:\n{feedback}"
    
    prompt += "\n\nProvide ONLY the Typst code, wrapped in ```typst blocks."
    
    content = [{"type": "text", "text": prompt}]
    for img in images:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{img}"}
        })
    
    msg = HumanMessage(content=content)
    response = llm.invoke([
        SystemMessage(content="You are a Typst expert. You convert PDFs to high-quality Typst templates."),
        msg
    ])
    
    code = response.content
    if isinstance(code, list):
        code = "\n".join([part if isinstance(part, str) else str(part) for part in code])

    # Apply the robust cleaning logic
    code = clean_code(code)
    
    return {
        "typst_code": code,
        "iterations": state['iterations'] + 1
    }

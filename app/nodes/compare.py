from langchain_core.messages import HumanMessage, SystemMessage
from app.state import AgentState
from app.utils import calculate_similarity

def compare_node(state: AgentState, llm):
    """Compares the original and compiled PDFs using Python similarity and LLM feedback."""
    print("--- COMPARING ---")
    orig_imgs = state['original_images']
    comp_imgs = state['compiled_images']
    
    if len(orig_imgs) != len(comp_imgs):
        print(f"Page count mismatch: {len(orig_imgs)} vs {len(comp_imgs)}")
        similarity_score = 0.0
    else:
        scores = [calculate_similarity(o, c) for o, c in zip(orig_imgs, comp_imgs)]
        similarity_score = sum(scores) / len(scores)
    
    print(f"Visual Similarity Score: {similarity_score:.4f}")
    
    # 90% match threshold
    # Change this as per model's capabilitites
    if similarity_score >= 0.65:
        return {"satisfied": True, "feedback": "SATISFIED - Near perfect match."}
    
    # If not satisfied, use LLM to explain differences
    prompt = (
        f"The visual similarity is only {similarity_score:.4f}. "
        "Compare the original PDF (First images) and the compiled Typst output (Last images). "
        "Identify specific layout, font, or content differences and provide detailed feedback on what to change in the Typst code."
    )
    
    content = [{"type": "text", "text": prompt}]
    # Original images
    for img in orig_imgs:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{img}"}
        })
    # Compiled images
    for img in comp_imgs:
        content.append({
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{img}"}
        })
        
    msg = HumanMessage(content=content)
    response = llm.invoke([
        SystemMessage(content="You are a layout comparison expert. Identify EXACTLY what is different between the original and the replica."),
        msg
    ])
    
    print(f"Feedback from LLM: {response.content[:200]}...")
    
    return {
        "satisfied": False,
        "feedback": response.content
    }

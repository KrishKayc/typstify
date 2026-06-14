from app.state import AgentState
from app.utils import pdf_to_base64_images, compile_typst

def compile_node(state: AgentState):
    """Compiles the generated Typst code."""
    iteration = state['iterations']
    output_filename = f"output_iter_{iteration}.pdf"
    print(f"--- COMPILING (Saving to {output_filename}) ---")
    
    success, logs = compile_typst(state['typst_code'], output_filename)
    
    compiled_images = []
    if success:
        compiled_images = pdf_to_base64_images(output_filename)
        print(f"Successfully compiled {output_filename}")
    else:
        print(f"Compilation failed for iteration {iteration}")
    
    return {
        "compilation_success": success,
        "compilation_error": logs if not success else "",
        "compiled_images": compiled_images
    }

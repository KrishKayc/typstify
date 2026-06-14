from app.state import AgentState

def check_compilation(state: AgentState):
    """Determines whether to proceed to comparison or retry generation due to compilation failure."""
    if state['compilation_success']:
        return "compare"
    
    if state['iterations'] >= 10:
        print("Max iterations reached after compilation failure.")
        return "end"
    
    return "generate"

def should_continue(state: AgentState):
    """Determines whether to continue looping or end."""
    if state['satisfied'] or state['iterations'] >= 10:
        return "end"
    return "generate"

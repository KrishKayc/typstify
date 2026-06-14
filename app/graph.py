from functools import partial
from langgraph.graph import StateGraph, END
from app.state import AgentState
from app.nodes import generate_typst_node, compile_node, compare_node, should_continue, check_compilation

def create_app(llm):
    # Define Graph
    workflow = StateGraph(AgentState)

    # Inject LLM into nodes that need it
    workflow.add_node("generate", partial(generate_typst_node, llm=llm))
    workflow.add_node("compile", compile_node)
    workflow.add_node("compare", partial(compare_node, llm=llm))

    workflow.set_entry_point("generate")

    workflow.add_edge("generate", "compile")

    workflow.add_conditional_edges(
        "compile",
        check_compilation,
        {
            "compare": "compare",
            "generate": "generate",
            "end": END
        }
    )

    workflow.add_conditional_edges(
        "compare",
        should_continue,
        {
            "generate": "generate",
            "end": END
        }
    )

    return workflow.compile()

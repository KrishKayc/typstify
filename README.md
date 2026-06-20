# Typstify 🚀

**Typstify** is an AI-powered agentic application that converts PDF documents into high-quality, editable [Typst](https://github.com/typst/typst) templates. 

Using **LangGraph** to manage an iterative refinement loop and **Advanced LLMs** (like Gemini, GPT-4o, or Claude) for vision and code generation, Typstify doesn't just "guess" the layout—it verifies it by compiling the code and visually comparing the result against the original.

---

## 🛠 How it Works: The Iterative Loop

Typstify operates on a **Generate -> Compile -> Compare** lifecycle:

1.  **Generate Node**: Analyzes the original PDF images and generates Typst code. If previous attempts failed, it receives the error logs or visual feedback to perform surgical fixes.
2.  **Compile Node**: Uses the local `typst` CLI to compile the generated code into a PDF.
3.  **Compare Node**: 
    - Calculates a **Visual Similarity Score (SSIM)** between the original and the new PDF.
    - If the match is below 95%, it sends both versions back to the LLM to identify layout, font, or spacing discrepancies.
4.  **Routing**: The graph automatically loops back to the generation step with specific feedback until it reaches a near-perfect match or hits the iteration limit.

---

## 📂 Project Structure

```text
typstify/
├── app/                # Core logic package
│   ├── nodes/          # Individual graph nodes (generate, compile, compare, etc.)
│   ├── graph.py        # LangGraph workflow orchestration
│   ├── state.py        # Agent state definition
│   └── utils.py        # Helper functions (PDF processing, SSIM calculation)
├── inputs/             # Place your source PDF files here
├── output/             # Final .typ templates and verified PDFs
├── main.py             # App entry point (LLM injection happens here)
└── requirements.txt    # Python dependencies
```

---

## ⚙️ Prerequisites

### 1. Typst CLI (Required)
The app **must** have access to the `typst` binary to verify the code.
- **Ubuntu/Debian**: `sudo snap install typst`
- **macOS**: `brew install typst`
- **Manual**: Download from [Typst Releases](https://github.com/typst/typst/releases).

### 2. System Dependencies
`pdf2image` requires **Poppler**:
- **Linux**: `sudo apt-get install poppler-utils`
- **macOS**: `brew install poppler`

### 3. Python Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🚀 Getting Started

1.  **Set up your Environment**:
    Create a `.env` file in the root directory and add the API key for your preferred provider:
    ```env
    # Example for Gemini (Default)
    GOOGLE_API_KEY=your_gemini_api_key
    
    # Or for OpenAI
    # OPENAI_API_KEY=your_openai_api_key
    ```

2.  **Add your PDF**:
    Place the PDF you want to convert into the `inputs/` folder.

3.  **Run the Agent**:
    ```bash
    python main.py inputs/your_document.pdf
    ```

4.  **Get your Results**:
    Check the `output/` folder for the final editable source and the verified PDF.

---

## 🧠 Model Flexibility & Customization
Typstify uses the **LangChain/LangGraph** LLM interface, meaning you can use **any model** that supports vision and is compatible with LangChain (Gemini, OpenAI, Anthropic, etc.).

By default, it is configured for Gemini in `main.py`, but you can easily swap it:

```python
# In main.py: Switch from Gemini to OpenAI
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o", temperature=0)
app = create_app(llm)
```

**Note:** Ensure your chosen model supports **Vision** (multi-modal input), as it needs to "see" the PDF pages for accurate layout replication.

---

## 📝 TODO

- [ ] Implement Prompt Caching.



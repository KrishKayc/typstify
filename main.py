import os
import sys
import shutil
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from app.graph import create_app
from app.utils import pdf_to_base64_images, cleanup_temp_files

load_dotenv()

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <input_pdf>")
        sys.exit(1)
        
    input_pdf = sys.argv[1]
    if not os.path.exists(input_pdf):
        print(f"Error: {input_pdf} not found.")
        sys.exit(1)
        
    # Initialize LLM
    if not os.getenv("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY not found in environment.")
        sys.exit(1)
    
    # You can easily swap this model for a higher one here
    llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0)
    
    # Create the graph app with injected LLM
    app = create_app(llm)
    
    # Prepare output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get base filename for output
    base_name = os.path.splitext(os.path.basename(input_pdf))[0]
    final_typ_path = os.path.join(output_dir, f"{base_name}.typ")
    final_pdf_path = os.path.join(output_dir, f"{base_name}_verified.pdf")
    
    print(f"Processing {input_pdf}...")
    initial_state = {
        "original_pdf_path": input_pdf,
        "original_images": pdf_to_base64_images(input_pdf),
        "compiled_images": [],
        "typst_code": "",
        "compilation_success": False,
        "compilation_error": "",
        "feedback": "",
        "satisfied": False,
        "iterations": 0
    }
    
    final_state = app.invoke(initial_state)
    
    print("\n--- FINAL RESULT ---")
    if final_state['satisfied']:
        print("Success! Typst template generated and verified.")
    else:
        print("Reached maximum iterations or ended without full satisfaction.")
        
    with open(final_typ_path, "w") as f:
        f.write(final_state['typst_code'])
    print(f"Final template saved to {final_typ_path}")

    # Save the final compiled PDF
    iteration = final_state['iterations']
    last_pdf = f"output_iter_{iteration}.pdf"
    if os.path.exists(last_pdf):
        shutil.copy(last_pdf, final_pdf_path)
        print(f"Final compiled PDF saved to {final_pdf_path}")
    
    # Cleanup temporary files but keep iteration PDFs
    cleanup_temp_files(["temp.typ"])

if __name__ == "__main__":
    main()

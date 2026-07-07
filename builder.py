import os
from app import load_json_data, build_resume_html

def build_resume():
    # Load resume data using the utility from app.py
    data = load_json_data()
    if not data:
        print("❌ Error: resume.json not found or empty.")
        return None
        
    # Compile the template
    output_html_path = build_resume_html(data)
    
    print(f"Resume successfully compiled to {output_html_path}")
    return output_html_path

if __name__ == "__main__":
    build_resume()
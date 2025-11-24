import os
import json
import google.generativeai as genai
from typing import List, Dict, Any

# Configure Gemini API
# Note: Ensure GOOGLE_API_KEY is set in environment variables
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def generate_test_cases(context: str, query: str) -> List[Dict[str, Any]]:
    model = genai.GenerativeModel('gemini-flash-latest')
    
    prompt = f"""
    Role: You are a Senior QA Automation Engineer.
    
    Task: Generate comprehensive test cases based ONLY on the provided context.
    
    Context:
    {context}
    
    User Request: {query}
    
    Constraints:
    1. Only generate test cases based on the provided docs. Do not hallucinate features not mentioned.
    2. Output must be a valid JSON array of objects.
    3. Each object must have the following keys:
       - Test_ID: string (e.g., TC001)
       - Feature: string
       - Test_Scenario: string
       - Expected_Result: string
       - Grounded_In: string (source document filename)
       
    Response Format:
    ```json
    [
        {{
            "Test_ID": "TC001",
            "Feature": "...",
            "Test_Scenario": "...",
            "Expected_Result": "...",
            "Grounded_In": "..."
        }}
    ]
    ```
    """
    
    response = model.generate_content(prompt)
    
    try:
        # Extract JSON from code block if present
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1]
            
        return json.loads(text)
    except Exception as e:
        print(f"Error parsing LLM response: {e}")
        return []

def generate_selenium_script(test_case: Dict[str, Any], html_content: str) -> str:
    model = genai.GenerativeModel('gemini-flash-latest')
    
    prompt = f"""
    Role: You are a Senior Selenium Automation Expert.
    
    Task: Generate a Python Selenium script for the following test case, using the provided HTML to identify elements.
    
    Test Case:
    {json.dumps(test_case, indent=2)}
    
    Target HTML:
    {html_content}
    
    Requirements:
    1. Use `selenium` library.
    2. Assume `driver` is already initialized (but provide a setup block commented out).
    3. Select elements using ID, Class, or XPath based on the provided HTML.
    4. Include assertions to verify the Expected Result.
    5. Output ONLY raw Python code. No markdown formatting.
    
    Code:
    """
    
    response = model.generate_content(prompt)
    
    text = response.text
    # Clean up markdown code blocks if present
    if "```python" in text:
        text = text.split("```python")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1]
        
    return text.strip()

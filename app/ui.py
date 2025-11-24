import streamlit as st
import requests
import json
import graphviz

# Backend API URL
API_URL = "http://localhost:8000"

st.set_page_config(page_title="Autonomous QA Agent", page_icon="🤖", layout="wide")

# --- Custom CSS for Styling & Dark/Light Mode ---
def inject_custom_css(is_dark_mode):
    if is_dark_mode:
        # Dark Mode Styles (Premium)
        css = """
        <style>
        .stApp {
            background-color: #0e1117;
            color: #fafafa;
        }
        .stButton>button {
            background: linear-gradient(45deg, #2b5876, #4e4376);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: #262730;
            color: white;
            border-radius: 8px;
        }
        .css-1aumxhk {
            background-color: #262730;
        }
        h1, h2, h3 {
            background: -webkit-linear-gradient(45deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        </style>
        """
    else:
        # Light Mode Styles (Clean)
        css = """
        <style>
        .stApp {
            background-color: #ffffff;
            color: #31333F;
        }
        .stButton>button {
            background: linear-gradient(45deg, #4facfe, #00f2fe);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        h1, h2, h3 {
            color: #1f77b4;
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Settings")
    dark_mode = st.toggle("🌙 Dark Mode", value=True)
    inject_custom_css(dark_mode)
    
    st.divider()
    st.header("🧠 Knowledge Base")
    if st.button("🗑️ Clear Knowledge Base"):
        try:
            requests.post(f"{API_URL}/clear-kb/")
            st.success("Knowledge Base Cleared!")
        except:
            st.error("Backend not reachable")

# --- Main Layout ---
st.title("🤖 Autonomous QA Agent")
st.markdown("### *Your AI-powered partner for automated testing*")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🏠 Overview", "📂 Ingestion", "🧪 Test Generation", "📜 Selenium Scripts"])

# --- Tab 1: Overview ---
with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🚀 Project Workflow")
        st.markdown("""
        This agent automates the QA process by:
        1.  **Ingesting** product specifications and UI designs.
        2.  **Generating** test cases using RAG (Retrieval Augmented Generation).
        3.  **Creating** executable Selenium scripts for automated testing.
        """)
        
        # Pipeline Diagram
        graph = graphviz.Digraph()
        graph.attr(rankdir='LR', bgcolor='transparent')
        graph.attr('node', shape='box', style='filled', fillcolor='#4e4376', fontcolor='white', fontname='Helvetica')
        graph.attr('edge', color='#fafafa')
        
        if not dark_mode:
            graph.attr('node', fillcolor='#4facfe', fontcolor='white')
            graph.attr('edge', color='#333333')

        graph.node('A', '📄 Docs & HTML')
        graph.node('B', '🧠 Vector DB (RAG)')
        graph.node('C', '🤖 Gemini LLM')
        graph.node('D', '🧪 Test Cases')
        graph.node('E', '📜 Selenium Scripts')

        graph.edge('A', 'B', 'Ingest')
        graph.edge('B', 'C', 'Context')
        graph.edge('C', 'D', 'Generate')
        graph.edge('D', 'C', 'Refine')
        graph.edge('C', 'E', 'Code')

        st.graphviz_chart(graph)

    with col2:
        st.info("💡 **Tip:** Start by uploading your documents in the 'Ingestion' tab.")
        st.success("✅ **Status:** System Online")
        st.warning("⚠️ **Note:** Ensure API Key is valid.")

# --- Tab 2: Ingestion ---
with tab2:
    st.header("📂 Upload Project Assets")
    st.markdown("Upload your **Product Specs (MD)**, **UI Guides (TXT)**, and **Target HTML**.")
    
    uploaded_files = st.file_uploader("Drag and drop files here", accept_multiple_files=True)
    
    if st.button("🚀 Ingest Documents", use_container_width=True):
        if uploaded_files:
            files = [("files", (file.name, file, file.type)) for file in uploaded_files]
            with st.spinner("Processing Knowledge Base..."):
                try:
                    response = requests.post(f"{API_URL}/ingest/", files=files)
                    if response.status_code == 200:
                        st.balloons()
                        st.success(f"✅ Successfully ingested {len(uploaded_files)} files!")
                        st.json(response.json())
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Connection Error: {e}")
        else:
            st.warning("⚠️ Please upload files first.")

# --- Tab 3: Test Generation ---
with tab3:
    st.header("🧪 Generate Test Cases")
    
    col_q, col_r = st.columns([1, 2])
    
    with col_q:
        user_query = st.text_area("🎯 What do you want to test?", "Generate tests for discount code functionality.", height=150)
        generate_btn = st.button("✨ Generate Test Cases", use_container_width=True)
    
    with col_r:
        if generate_btn:
            with st.spinner("🤖 AI is thinking..."):
                try:
                    response = requests.post(f"{API_URL}/generate-tests/", json={"query": user_query})
                    if response.status_code == 200:
                        test_cases = response.json().get("test_cases", [])
                        st.session_state['test_cases'] = test_cases
                        st.success(f"✅ Generated {len(test_cases)} Test Cases")
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Connection Error: {e}")

        if 'test_cases' in st.session_state:
            for i, tc in enumerate(st.session_state['test_cases']):
                with st.expander(f"📌 {tc.get('Test_ID')}: {tc.get('Feature')}"):
                    st.markdown(f"**Scenario:** {tc.get('Test_Scenario')}")
                    st.markdown(f"**Expected:** {tc.get('Expected_Result')}")
                    st.caption(f"Source: {tc.get('Grounded_In')}")
                    
                    if st.button(f"⚡ Generate Script for {tc.get('Test_ID')}", key=f"btn_{i}"):
                        st.session_state['selected_test_case'] = tc
                        st.toast(f"Selected {tc.get('Test_ID')} for script generation!", icon="✅")

# --- Tab 4: Selenium Scripts ---
with tab4:
    st.header("📜 Selenium Script Generation")
    
    if 'selected_test_case' in st.session_state:
        tc = st.session_state['selected_test_case']
        st.info(f"👉 **Selected Test Case:** {tc.get('Test_ID')} - {tc.get('Test_Scenario')}")
        
        target_html = st.file_uploader("📄 Upload Target HTML (checkout.html)", type=["html"], key="html_uploader")
        
        if target_html:
            html_content = target_html.getvalue().decode("utf-8")
            if st.button("💻 Generate Python Code", use_container_width=True):
                with st.spinner("👨‍💻 Writing code..."):
                    try:
                        payload = {
                            "test_case": tc,
                            "html_content": html_content
                        }
                        response = requests.post(f"{API_URL}/generate-selenium/", json=payload)
                        if response.status_code == 200:
                            script = response.json().get("selenium_script", "")
                            st.code(script, language="python")
                            st.success("✅ Script Generated!")
                        else:
                            st.error(f"❌ Error: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Connection Error: {e}")
        else:
            st.warning("⚠️ Please upload the target HTML file to proceed.")
    else:
        st.info("👈 Please select a test case from the 'Test Generation' tab first.")

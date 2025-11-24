import streamlit as st
import requests
import json
import graphviz

# Backend API URL
API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="AI QA Genesis - Autonomous Testing Agent", 
    page_icon="🧬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Premium Styling & Dark/Light Mode ---
def inject_custom_css(is_dark_mode):
    if is_dark_mode:
        # Dark Mode Styles (Premium Cyberpunk)
        css = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #0a0e27 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff !important;
            font-family: 'Rajdhani', sans-serif;
        }
        
        /* Force all text to be white */
        p, span, div, label, li {
            color: #ffffff !important;
        }
        
        /* Links should be visible too */
        a {
            color: #00d2ff !important;
        }
        
        a:hover {
            color: #b721ff !important;
        }
        
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif !important;
            background: linear-gradient(45deg, #00d2ff, #3a47d5, #b721ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white !important;
            border: 2px solid #b721ff;
            border-radius: 12px;
            padding: 0.6rem 1.2rem;
            font-weight: bold;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.4s ease;
            box-shadow: 0 4px 15px rgba(103, 126, 234, 0.4);
        }
        
        .stButton>button:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 25px rgba(183, 33, 255, 0.6);
            border-color: #00d2ff;
        }
        
        .stTextInput>div>div>input, .stTextArea>div>div>textarea {
            background-color: rgba(38, 39, 48, 0.8);
            color: #ffffff !important;
            border: 1px solid #667eea;
            border-radius: 8px;
            font-family: 'Rajdhani', sans-serif;
        }
        
        .stExpander {
            background-color: rgba(26, 26, 46, 0.6);
            border: 1px solid #667eea;
            border-radius: 10px;
            color: #ffffff !important;
        }
        
        .author-badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
            font-family: 'Orbitron', sans-serif;
            font-size: 14px;
            color: white;
            box-shadow: 0 4px 15px rgba(103, 126, 234, 0.5);
        }
        
        .feature-box {
            background: rgba(38, 39, 48, 0.6);
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
        }
        </style>
        """
    else:
        # Light Mode Styles (Premium Modern)
        css = """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600&display=swap');
        
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: #2c3e50;
            font-family: 'Rajdhani', sans-serif;
        }
        
        h1, h2, h3 {
            font-family: 'Orbitron', sans-serif !important;
            color: #667eea;
            font-weight: 900;
            text-transform: uppercase;
            letter-spacing: 2px;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 12px;
            padding: 0.6rem 1.2rem;
            font-weight: bold;
            font-family: 'Orbitron', sans-serif;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.4s ease;
            box-shadow: 0 4px 15px rgba(103, 126, 234, 0.3);
        }
        
        .stButton>button:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 8px 25px rgba(103, 126, 234, 0.5);
        }
        
        .author-badge {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 8px 16px;
            border-radius: 20px;
            display: inline-block;
            font-family: 'Orbitron', sans-serif;
            font-size: 14px;
            color: white;
            box-shadow: 0 4px 15px rgba(103, 126, 234, 0.4);
        }
        
        .feature-box {
            background: white;
            border-left: 4px solid #667eea;
            padding: 15px;
            border-radius: 8px;
            margin: 10px 0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")
    dark_mode = st.toggle("🌙 Dark Mode", value=True)
    inject_custom_css(dark_mode)
    
    st.divider()
    st.markdown("### 🧠 Knowledge Base")
    if st.button("🗑️ Clear Database", use_container_width=True):
        try:
            requests.post(f"{API_URL}/clear-kb/")
            st.success("✅ Database Cleared!")
        except:
            st.error("❌ Backend Offline")
    
    st.divider()
    st.markdown("### 👨‍💻 Creator")
    st.markdown('<div class="author-badge">Made by Pranjal Khare</div>', unsafe_allow_html=True)
    st.markdown("🔗 [GitHub](https://github.com/pranjalkhare2004)")

# --- Main Layout ---
st.markdown("# 🧬 AI QA GENESIS")
st.markdown("### *Next-Generation Autonomous Testing Intelligence*")
st.caption("Powered by Google Gemini AI & RAG Architecture")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🏠 Dashboard", 
    "📂 Knowledge Ingestion", 
    "🧪 Test Generation", 
    "📜 Script Automation"
])

# --- Tab 1: Dashboard ---
with tab1:
    st.markdown("## 🚀 Mission Control")
    
    # About Section
    st.markdown("### 📖 About This Project")
    st.markdown("""
    <div class="feature-box">
    <b>AI QA Genesis</b> is a cutting-edge autonomous testing agent that revolutionizes the QA workflow by:
    
    🎯 <b>Intelligent Context Understanding</b> - Uses RAG (Retrieval Augmented Generation) to comprehend product specifications<br>
    🤖 <b>AI-Powered Test Generation</b> - Leverages Google Gemini to create comprehensive test cases<br>
    📜 <b>Automated Script Creation</b> - Generates ready-to-run Selenium Python scripts<br>
    🔄 <b>Continuous Learning</b> - Adapts to your project's evolving requirements
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    
    # Enhanced Pipeline Diagram
    st.markdown("### 🔬 Intelligence Pipeline")
    st.caption("Advanced Multi-Stage Processing Architecture")
    
    # Create pipeline diagram with mixed layout
    diagram = graphviz.Digraph('pipeline', format='png')
    
    # Graph settings
    diagram.attr(bgcolor='transparent')
    diagram.attr('node', 
                 shape='box',
                 style='filled,rounded',
                 fontname='Arial Bold',
                 fontsize='12',
                 margin='0.5,0.4',
                 height='1.3',
                 width='2.2')
    diagram.attr('edge',
                 fontname='Arial Bold',
                 fontsize='24',
                 penwidth='3')
    
    # Colors
    if dark_mode:
        colors = {
            'input': '#667eea',
            'process': '#764ba2', 
            'embed': '#f093fb',
            'store': '#4facfe',
            'retrieve': '#00f2fe',
            'output': '#43e97b'
        }
        edge_color = '#00eaff'
        text_color = 'white'
    else:
        colors = {
            'input': '#667eea',
            'process': '#764ba2',
            'embed': '#f093fb', 
            'store': '#4facfe',
            'retrieve': '#00f2fe',
            'output': '#43e97b'
        }
        edge_color = '#667eea'
        text_color = 'white'
    
    # First row - horizontal (4 nodes)
    with diagram.subgraph(name='cluster_0') as sub:
        sub.attr(rank='same', style='invis')
        sub.node('input', '📄 Input\nDocs/HTML', 
                fillcolor=colors['input'], fontcolor=text_color)
        sub.node('parse', '🔍 Parser\nMD/TXT/HTML',
                fillcolor=colors['process'], fontcolor=text_color)
        sub.node('chunk', '✂️ Chunker\nSegment',
                fillcolor=colors['process'], fontcolor=text_color)
        sub.node('embed', '🧠 Embeddings\nGemini',
                fillcolor=colors['embed'], fontcolor=text_color)
    
    # Second row nodes (vertical flow)
    diagram.node('vector', '💾 Vector DB\nChromaDB',
                fillcolor=colors['store'], fontcolor=text_color)
    
    diagram.node('query', '🎯 Query\nUser Input',
                fillcolor=colors['input'], fontcolor=text_color)
    
    diagram.node('retrieve', '🔎 Retrieve\nContext',
                fillcolor=colors['retrieve'], fontcolor=text_color)
    
    diagram.node('llm', '🤖 LLM\nGemini Flash',
                fillcolor=colors['embed'], fontcolor=text_color)
    
    diagram.node('tests', '✅ Tests\nJSON',
                fillcolor=colors['output'], fontcolor=text_color)
    
    diagram.node('selenium', '📜 Scripts\nPython',
                fillcolor=colors['output'], fontcolor=text_color)
    
    # Edges - horizontal flow for first 4
    diagram.edge('input', 'parse', label='Upload', color=edge_color, fontcolor=edge_color)
    diagram.edge('parse', 'chunk', label='Split', color=edge_color, fontcolor=edge_color)
    diagram.edge('chunk', 'embed', label='Vectorize', color=edge_color, fontcolor=edge_color)
    
    # Vertical flow
    diagram.edge('embed', 'vector', label='Store', color=edge_color, fontcolor=edge_color)
    diagram.edge('query', 'retrieve', label='Search', color=edge_color, fontcolor=edge_color)
    diagram.edge('vector', 'retrieve', label='Match', color=edge_color, style='dashed', fontcolor=edge_color)
    diagram.edge('retrieve', 'llm', label='Context', color=edge_color, fontcolor=edge_color)
    diagram.edge('llm', 'tests', label='Generate', color=edge_color, fontcolor=edge_color)
    diagram.edge('tests', 'llm', label='Refine', color=edge_color, style='dotted', fontcolor=edge_color)
    diagram.edge('llm', 'selenium', label='Code', color=edge_color, fontcolor=edge_color)
    
    # Center the diagram
    col_left, col_center, col_right = st.columns([1, 3, 1])
    with col_center:
        st.graphviz_chart(diagram)
    
    # System Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🚀 Status", "ONLINE", "✓")
    with col2:
        st.metric("🧠 AI Model", "Gemini", "Flash")
    with col3:
        st.metric("💾 Storage", "Persistent", "ChromaDB")
    with col4:
        st.metric("🔒 Security", "API Key", "Secured")

# --- Tab 2: Ingestion ---
with tab2:
    st.markdown("## 📂 Knowledge Ingestion Portal")
    st.markdown("Upload your **Product Specs**, **UI Guides**, and **Target HTML** to build the knowledge base.")
    
    uploaded_files = st.file_uploader(
        "🎯 Drag and Drop Assets Here", 
        accept_multiple_files=True,
        help="Supported formats: MD, TXT, JSON, HTML"
    )
    
    if st.button("⚡ INGEST & VECTORIZE", use_container_width=True, type="primary"):
        if uploaded_files:
            files = [("files", (file.name, file, file.type)) for file in uploaded_files]
            with st.spinner("🔄 Processing Knowledge Base..."):
                try:
                    response = requests.post(f"{API_URL}/ingest/", files=files)
                    if response.status_code == 200:
                        st.balloons()
                        st.success(f"✅ Successfully ingested {len(uploaded_files)} files!")
                        result = response.json()
                        st.info(f"📊 Created {result.get('total_chunks', 0)} knowledge chunks")
                        with st.expander("📋 View Details"):
                            st.json(result)
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Connection Error: {e}")
        else:
            st.warning("⚠️ Please upload files first.")

# --- Tab 3: Test Generation ---
with tab3:
    st.markdown("## 🧪 AI Test Case Generator")
    
    col_q, col_r = st.columns([1, 2])
    
    with col_q:
        user_query = st.text_area(
            "🎯 Define Your Testing Objective", 
            "Generate comprehensive test cases for discount code functionality (SAVE15)",
            height=180,
            help="Describe what you want to test in natural language"
        )
        generate_btn = st.button("✨ GENERATE TESTS", use_container_width=True, type="primary")
    
    with col_r:
        if generate_btn:
            with st.spinner("🤖 AI Analyzing Knowledge Base..."):
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
            st.markdown("### 📋 Generated Test Suite")
            for i, tc in enumerate(st.session_state['test_cases']):
                with st.expander(f"🧪 **{tc.get('Test_ID')}** | {tc.get('Feature')}"):
                    st.markdown(f"**📝 Scenario:** {tc.get('Test_Scenario')}")
                    st.markdown(f"**✅ Expected:** {tc.get('Expected_Result')}")
                    st.caption(f"📚 Source: {tc.get('Grounded_In')}")
                    
                    if st.button(f"⚡ Generate Selenium Script", key=f"btn_{i}", use_container_width=True):
                        st.session_state['selected_test_case'] = tc
                        st.toast(f"✅ Selected {tc.get('Test_ID')} for automation!", icon="🎯")

# --- Tab 4: Selenium Scripts ---
with tab4:
    st.markdown("## 📜 Selenium Automation Generator")
    
    if 'selected_test_case' in st.session_state:
        tc = st.session_state['selected_test_case']
        st.info(f"🎯 **Active Test Case:** {tc.get('Test_ID')} - {tc.get('Test_Scenario')}")
        
        target_html = st.file_uploader(
            "📄 Upload Target HTML (e.g., checkout.html)", 
            type=["html"], 
            key="html_uploader",
            help="The HTML file that contains the elements to be tested"
        )
        
        if target_html:
            html_content = target_html.getvalue().decode("utf-8")
            if st.button("💻 GENERATE PYTHON CODE", use_container_width=True, type="primary"):
                with st.spinner("👨‍💻 AI Writing Selenium Script..."):
                    try:
                        payload = {
                            "test_case": tc,
                            "html_content": html_content
                        }
                        response = requests.post(f"{API_URL}/generate-selenium/", json=payload)
                        if response.status_code == 200:
                            script = response.json().get("selenium_script", "")
                            st.success("✅ Script Generated Successfully!")
                            st.code(script, language="python")
                            st.download_button(
                                label="⬇️ Download Script",
                                data=script,
                                file_name=f"test_{tc.get('Test_ID').lower()}.py",
                                mime="text/plain"
                            )
                        else:
                            st.error(f"❌ Error: {response.text}")
                    except Exception as e:
                        st.error(f"❌ Connection Error: {e}")
        else:
            st.warning("⚠️ Please upload the target HTML file to proceed.")
    else:
        st.info("👈 Please select a test case from the 'Test Generation' tab first.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #667eea; font-family: Orbitron;'>
    <b>AI QA Genesis v1.0</b> | Powered by Google Gemini AI | Made with ❤️ by Pranjal Khare
</div>
""", unsafe_allow_html=True)

from collections import Counter
from collections import defaultdict
from streamlit_echarts import st_echarts
import ast
import networkx as nx
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import json

@st.cache_data
def load_data():
    df = pd.read_csv('data/data.csv')
    return df

df = load_data()

st.markdown("""
    # Concepts and Functions Analysis

    Dive into the world of Data Analysis Expressions (DAX) with this comprehensive exploration:

    - 📊 Concept frequency and difficulty levels
    - 🔧 Most-used functions and their relationships
    - 🕸️ Real-world concept and function connections
    - 📈 DAX function popularity trends
    - 📚 Categorized function guide with examples

    Whether you're a DAX novice or expert, gain valuable insights to enhance your skills and knowledge.

""")
st.markdown("---")

st.header("🎭 DAX Categories Challenge Spectrum")

def safe_eval(x):
    try:
        return ast.literal_eval(x)
    except ValueError:
        return []

df['Categories in Question'] = df['Categories in Question'].apply(safe_eval)

df_exploded_categories = df['Categories in Question'].explode()

df_exploded_categories = df_exploded_categories[df_exploded_categories.notna()]

category_counts = df_exploded_categories.value_counts().reset_index(name='Counts')
category_counts.columns = ['Category', 'Counts']
category_counts = category_counts.sort_values(by='Counts', ascending=False)

fig_categories = px.bar(
    category_counts,
    x='Category',
    y='Counts',
    labels={'Category': 'Categories', 'Counts': 'Frequency'},
    title='DAX Categories by Frequency of Questions'
)

fig_categories.update_layout(
    xaxis_title="Categories",
    yaxis_title="Frequency"
)

st.plotly_chart(fig_categories, use_container_width=True)

st.markdown("""
    This chart illustrates which DAX categories users encounter most frequently in their questions and challenges. The taller the bar, the more questions and discussions we see around that category.

    🔍 What This Means for You:
    1. **High Bars = Common Areas of Focus**: Categories with taller bars represent areas where users frequently seek help or clarification. These are key areas to prioritize in your DAX learning journey.
    
    2. **Learning Roadmap**: If you're new to DAX or looking to enhance your skills, start with the categories at the left. They represent the most common areas of interest and potential challenges.
    
    3. **Expertise Development**: For more experienced users, these top categories highlight where your expertise can be most valuable. Consider deepening your knowledge in these areas to become a DAX specialist.

    Remember: Frequency of questions often correlates with the importance and complexity of a category. Mastering these key areas will significantly enhance your DAX proficiency! 💪📊
""")
st.info("""
            **Pro Tip:** Use this chart as a guide to structure your DAX learning. Focus on mastering the most frequent categories first, then progress to the less common ones. This approach will help you tackle the most relevant DAX challenges effectively.
""")

st.markdown("---")

with open('data/dax-categories.json') as f:
    dax_categories = json.load(f)

st.header("🔍 DAX Function Deep Dive by Category")

selected_category = st.selectbox(
    "Select a DAX category to explore:",
    options=list(dax_categories.keys()),
    index=0
)

def get_function_counts(category):
    functions = dax_categories[category]
    
    df['DAX Functions in Question'] = df['DAX Functions in Question'].apply(safe_eval)
    
    df_exploded = df.explode('DAX Functions in Question')
    
    df_category = df_exploded[df_exploded['DAX Functions in Question'].isin(functions)]
    
    function_counts = df_category['DAX Functions in Question'].value_counts()
    
    return function_counts

function_counts = get_function_counts(selected_category)

fig = px.bar(
    x=function_counts.index,
    y=function_counts.values,
    labels={'x': 'Function', 'y': 'Frequency'},
    title=f'Function Usage in {selected_category} Category'
)

fig.update_layout(
    xaxis_title="DAX Functions",
    yaxis_title="Frequency of Use",
    xaxis_tickangle=-45
)

st.plotly_chart(fig, use_container_width=True)

st.info("""
        Remember, frequency doesn't always equate to importance for your specific needs. Some less frequent functions 
    might be crucial for particular analyses or industries.
""")

df['Asked Date'] = pd.to_datetime(df['Asked Date'])

st.markdown("---")

df = load_data()

st.header("🔧 The DAX Function Toolbox")

df['DAX Functions'] = df['DAX Functions in Question'].apply(safe_eval)
all_functions = [func for funcs in df['DAX Functions'] for func in funcs if func]
function_counts = Counter(all_functions)
top_functions = function_counts.most_common(20)

treemap_data = pd.DataFrame(top_functions, columns=['Function', 'Count'])

fig_functions = px.treemap(
    treemap_data,
    path=['Function'],
    values='Count',
    title='Top 20 DAX Functions',
)

fig_functions.update_traces(textinfo="label+value")
fig_functions.update_layout(margin=dict(t=50, l=25, r=25, b=25))

st.plotly_chart(fig_functions, use_container_width=True)

st.info("""
        **Learning Tip:** Start with the largest boxes and work your way down. As you master these common functions, 
    you'll be equipped to handle a wide range of DAX scenarios!
""")

st.markdown("---")

st.header("📈 The DAX Function Time Machine")

df['Year'] = pd.to_datetime(df['Asked Date']).dt.year
function_trends = df.explode('DAX Functions').groupby(['Year', 'DAX Functions']).size().unstack(fill_value=0)

selected_functions = st.multiselect(
    'Select DAX functions to view trends',
    options=function_trends.columns,
    default=function_trends.sum().nlargest(3).index.tolist()
)

if selected_functions:
    fig_trends = px.line(
        function_trends[selected_functions],
        labels={'value': 'Frequency', 'Year': 'Year'},
        title='DAX Function Usage Trends'
    )
    fig_trends.update_layout(
        xaxis_title="Year",
        yaxis_title="Frequency"
    )
    st.plotly_chart(fig_trends, use_container_width=True)

else:
    st.write("Please select at least one function to view its trend.")

st.markdown("---")

def safe_eval(x):
    try:
        return ast.literal_eval(x)
    except:
        return []

df['DAX Functions in Question'] = df['DAX Functions in Question'].apply(safe_eval)

function_usage = defaultdict(int)
function_co_occurrence = defaultdict(int)

for functions in df['DAX Functions in Question']:
    for func in functions:
        function_usage[func] += 1
    for i, func1 in enumerate(functions):
        for func2 in functions[i+1:]:
            if func1 < func2:
                function_co_occurrence[(func1, func2)] += 1
            else:
                function_co_occurrence[(func2, func1)] += 1

st.title("DAX Function Co-occurrence Network")

mode = st.radio("Select mode:", ["Top N Functions", "Free Select Functions"])

if mode == "Top N Functions":
    max_functions = min(50, len(function_usage))
    top_n = st.slider("Select top N functions to visualize:", min_value=5, max_value=max_functions, value=20, step=1)
    
    top_functions = sorted(function_usage.items(), key=lambda x: x[1], reverse=True)[:top_n]
    selected_functions = [func for func, _ in top_functions]
else:
    all_functions = sorted(function_usage.keys())
    default_functions = [func for func, _ in sorted(function_usage.items(), key=lambda x: x[1], reverse=True)[:10]]
    selected_functions = st.multiselect(
        "Select DAX functions to visualize:",
        options=all_functions,
        default=default_functions
    )

filtered_co_occurrence = {(func1, func2): count 
                          for (func1, func2), count in function_co_occurrence.items() 
                          if func1 in selected_functions and func2 in selected_functions}

G = nx.Graph()
for func in selected_functions:
    G.add_node(func, size=function_usage[func])

for (func1, func2), count in filtered_co_occurrence.items():
    G.add_edge(func1, func2, weight=count)

pos = nx.spring_layout(G)

nodes = [
    {
        "name": func,
        "symbolSize": min(20 + function_usage[func] / 5, 50),
        "x": pos[func][0] * 1000,
        "y": pos[func][1] * 1000,
        "value": function_usage[func],
        "category": func
    } for func in selected_functions
]

edges = [
    {
        "source": func1,
        "target": func2,
        "lineStyle": {
            "width": min(1 + count / 10, 5)
        }
    } for (func1, func2), count in filtered_co_occurrence.items()
]

option = {
    "title": {
        "text": f"DAX Function Co-occurrence in Questions ({mode})"
    },
    "tooltip": {},
    "animationDurationUpdate": 1500,
    "animationEasingUpdate": "quinticInOut",
    "series": [{
        "type": "graph",
        "layout": "none",
        "data": nodes,
        "links": edges,
        "roam": True,
        "label": {
            "show": True,
            "position": "right",
            "formatter": "{b}"
        },
        "emphasis": {
            "focus": "adjacency",
            "lineStyle": {
                "width": 10
            }
        },
        "lineStyle": {
            "curveness": 0.3
        }
    }]
}

st_echarts(options=option, height="700px")

st.info(f"This graph shows the co-occurrence of the selected DAX functions in questions. "
        "The size of each node represents the frequency of the function's usage, "
        "and the thickness of the edges represents how often two functions appear together.")

st.markdown("### How to interpret this visualization:")
st.markdown("- Each node represents a selected DAX function.")
st.markdown("- The size of a node indicates how frequently the function is used.")
st.markdown("- Edges between nodes show that these functions often appear together in questions.")
st.markdown("- Thicker edges indicate stronger co-occurrence between functions.")
st.markdown("- You can zoom and pan the graph using your mouse or touchpad.")
st.markdown(f"- Use the {mode.lower()} to adjust which functions are displayed.")

st.markdown("---")

df['Asked Date'] = pd.to_datetime(df['Asked Date'])

with open('data/dax-categories.json') as f:
    dax_categories = json.load(f)

with st.container(border=True):
    st.subheader("🔍 Explore Top Questions for a DAX Function")

    selected_category = st.selectbox(
        "Select a DAX category to explore:",
        options=list(dax_categories.keys()),
        index=0,
        key="category_select"
    )

    category_functions = dax_categories[selected_category]

    selected_function = st.selectbox(
        "Select a DAX function:",
        options=category_functions,
        index=0,
        key="function_select"
    )

    num_questions = st.slider(
        "Select number of top viewed questions to display", 
        min_value=1, 
        max_value=10, 
        value=3,
        key="question_slider"
    )
        
    if st.button("🔍 Show Me", key="show_button"):
        function_questions = df[df['DAX Functions in Question'].apply(lambda x: selected_function in x)]
        
        function_questions['Views'] = pd.to_numeric(function_questions['Views'].str.replace(',', ''), errors='coerce')
        
        function_questions = function_questions.dropna(subset=['Views'])
        
        top_views = function_questions.nlargest(num_questions, 'Views')[['context', 'dax_code_provided', 'correct_answer', 'concepts', 'Asked Date', 'Views', 'Number of Answers', 'URL']]

        if not top_views.empty:
            for idx, (index, row) in enumerate(top_views.iterrows()):
                st.markdown(f"### Question {idx + 1}:")

                col1, col2, col3, col4 = st.columns([1.5, 1, 0.7, 2])

                with col1:
                    with st.container(border=True):
                        st.markdown(f"**Asked Date:** {row['Asked Date'].strftime('%Y-%m-%d')}")
                
                with col2:
                    with st.container(border=True):
                        st.markdown(f"**Views:** {format(int(row['Views']), ',')}")

                with col3:
                    with st.container(border=True):
                        st.markdown(f"**Answers:** {row['Number of Answers']}")

                with col4:
                    with st.container(border=True):
                        st.markdown(f"**Concepts**: {row['concepts']}")

                st.write(row['context'])
                
                if row['dax_code_provided']:
                    st.code(row['dax_code_provided'], language='sql')
                
                if row['correct_answer']:
                    st.markdown(f"#### Correct Answer:")
                    st.code(row['correct_answer'], language='sql')
                
                st.markdown(f"[View original post]({row['URL']})", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.write(f"No questions found using the {selected_function} function.")

    if st.button("🔄 Okay, I'm done", key="clear_button"):
        st.experimental_rerun()

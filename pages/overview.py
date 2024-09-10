import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_loader import load_data
import itertools
import ast

df = load_data()

earliest_date = df['Asked Date'].min().strftime('%Y-%m-%d')
latest_date = df['Asked Date'].max().strftime('%Y-%m-%d')
st.title("DAX Analytics Dashboard", anchor=False)

st.divider()

st.info("""
This dashboard provides a comprehensive analysis of DAX (Data Analysis Expressions) usage patterns and challenges, based on Stack Overflow questions. Our goal is to offer valuable insights into:

- 📊 Identifying functions and concepts that DAX users find most challenging
- 📈 Tracking how these trends have evolved over time
- 🔍 Examining common difficulties and function usage trends
- 🏢 Exploring industry-specific applications of DAX
- 📉 Analyzing user engagement metrics

By leveraging this data, you can:

1. Understand prevalent DAX challenges
2. Monitor the popularity of different functions
3. Chart an effective learning path from DAX beginner to expert

Whether you're new to DAX or looking to enhance your expertise, this dashboard serves as a valuable resource to guide your skill development journey.
""")

st.markdown("#### Data Coverage")
st.markdown(f"""
    Analysis timeframe: **{earliest_date}** to **{latest_date}**
    
    This dataset captures DAX-related questions, trends, and community interactions over {(pd.to_datetime(latest_date) - pd.to_datetime(earliest_date)).days // 365} years.
    
    Data source: [Stack Overflow DAX questions](https://stackoverflow.com/questions/tagged/dax)
""")
st.markdown("---")

st.subheader("📊 Data Overview")

flattened_list = list(itertools.chain(*df['DAX Functions in Question']))

unique_functions = set(flattened_list)

count_unique_functions = len(unique_functions)

st.write("")

total_questions = format(len(df), ',')
total_functions_used = count_unique_functions
total_views = format(int(df['Views'].sum()), ',')
total_answers = format(df['Number of Answers'].sum(), ',')
total_votes = f"{df['Votes'].sum():,}"
unique_answer_providers = df['Highest Score Answer Author'].nunique()

st.markdown("""
<style>
    .metric-container {
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 10px;
        margin-bottom: 15px;
    }
    .metric {
        background-color: white;
        border-radius: 6px;
        padding: 10px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    .metric:hover {
        transform: translateY(-3px);
    }
    .metric-icon {
        font-size: 1.5rem;
        margin-bottom: 5px;
    }
    .metric-title {
        font-weight: bold;
        font-size: 0.9rem;
        margin-bottom: 5px;
        color: #333;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #0066cc;
        margin-bottom: 3px;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="metric-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric">
        <div class="metric-icon">📊</div>
        <div class="metric-title">Dataset Overview</div>
        <div class="metric-value">{}</div>
        <div class="metric-label">Total Questions</div>
    </div>
    """.format(total_questions), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric">
        <div class="metric-icon">🛠️</div>
        <div class="metric-title">Function Utilization</div>
        <div class="metric-value">{}</div>
        <div class="metric-label">DAX Functions Employed</div>
    </div>
    """.format(total_functions_used), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric">
        <div class="metric-icon">📈</div>
        <div class="metric-title">Engagement Metrics</div>
        <div class="metric-value">{}</div>
        <div class="metric-label">Total Page Views</div>
    </div>
    """.format(total_views), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="metric-container">', unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric">
        <div class="metric-icon">📝</div>
        <div class="metric-title">Total Responses</div>
        <div class="metric-value">{}</div>
        <div class="metric-label">Answers Provided</div>
    </div>
    """.format(total_answers), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric">
        <div class="metric-icon">👍</div>
        <div class="metric-title">Community Engagement</div>
        <div class="metric-value">{}</div>
        <div class="metric-label">Total Votes Received</div>
    </div>
    """.format(total_votes), unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric">
        <div class="metric-icon">👥</div>
        <div class="metric-title">Contributor Base</div>
        <div class="metric-value">{}</div>
        <div class="metric-label">Unique Contributors</div>
    </div>
    """.format(unique_answer_providers), unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

st.write("")

def safe_eval(x):
    try:
        return ast.literal_eval(x)
    except ValueError:
        return []

df['DAX Functions in Question'] = df['DAX Functions in Question'].apply(safe_eval)

df_exploded = df['DAX Functions in Question'].explode()

df_exploded = df_exploded[df_exploded.notna()]

function_counts = df_exploded.value_counts().reset_index(name='Counts')
function_counts.columns = ['DAX Function', 'Counts']
function_counts = function_counts.sort_values(by='Counts', ascending=False)

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

@st.cache_data
def load_visual_data():
    df = pd.read_csv('data/data.csv')
    return df

df = load_visual_data()

with st.container(border=True):
    st.subheader("🧩 DAX's Toughest Puzzles")
    
    st.markdown("""
    This section provides insights into the most challenging aspects of DAX. 
    We've analyzed thousands of questions to identify the functions, categories, and concepts that users 
    find most difficult. This information can help guide your learning journey and highlight areas where 
    extra attention might be beneficial.
    """)
    
    color_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    col1, col2 = st.columns(2)

    with col1:
        with st.container():
            st.write("#### Most Challenging DAX Functions")
            top_dax_functions = function_counts.head(10)
            fig_dax_functions = px.bar(top_dax_functions, x='Counts', y='DAX Function', orientation='h',
                                    text_auto=True,
                                    color_discrete_sequence=color_palette)
            fig_dax_functions.update_layout(
                yaxis={'categoryorder':'total ascending'},
                xaxis_title="Frequency",
                yaxis_title="DAX Function",
                plot_bgcolor='rgba(0,0,0,0)',
                hoverlabel=dict(bgcolor="white", font_size=12)
            )
            st.plotly_chart(fig_dax_functions, use_container_width=True)

    with col2:
        with st.container():
            st.write("#### Frequently Discussed DAX Categories")
            top_categories = category_counts.head(10)
            fig_categories = px.bar(top_categories, x='Counts', y='Category', orientation='h',
                                    text_auto=True,
                                    color_discrete_sequence=color_palette)
            fig_categories.update_layout(
                yaxis={'categoryorder':'total ascending'},
                xaxis_title="Frequency",
                yaxis_title="Category",
                plot_bgcolor='rgba(0,0,0,0)',
                hoverlabel=dict(bgcolor="white", font_size=12)
            )
            st.plotly_chart(fig_categories, use_container_width=True)

    col1, col2 = st.columns(2)

    with col1:
        df['difficulty_level'] = df['difficulty_level'].replace({'': pd.NA, 'NA': pd.NA, 'none': pd.NA}).dropna()
        difficulty_counts = df['difficulty_level'].value_counts().reset_index()
        difficulty_counts.columns = ['Difficulty Level', 'Counts']

        with st.container():
            st.write("#### Complexity Distribution of DAX Questions")
            chart_container = st.container()
            with chart_container:
                fig_difficulty = px.pie(difficulty_counts, names='Difficulty Level', values='Counts', 
                                        color_discrete_sequence=color_palette)
                fig_difficulty.update_traces(textposition='inside', textinfo='percent+label')
                fig_difficulty.update_layout(
                    legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
                    margin=dict(l=20, r=20, t=40, b=20),
                    height=350
                )
                st.plotly_chart(fig_difficulty, use_container_width=True)

    with col2:
        df['concepts'] = df['concepts'].apply(lambda x: safe_eval(x) if isinstance(x, str) else x)
        df_exploded_concepts = df['concepts'].explode()
        df_exploded_concepts = df_exploded_concepts[df_exploded_concepts.notna()]
        concept_counts = df_exploded_concepts.value_counts().reset_index(name='Counts')
        concept_counts.columns = ['Concept', 'Counts']
        concept_counts = concept_counts.sort_values(by='Counts', ascending=False)

        with st.container():
            st.write("#### Most Challenging DAX Concepts")
            chart_container = st.container()
            with chart_container:
                fig_concepts = px.bar(concept_counts.head(10), x='Counts', y='Concept', orientation='h',
                                    text_auto=True,
                                    color_discrete_sequence=color_palette)
                fig_concepts.update_layout(
                    yaxis={'categoryorder':'total ascending'},
                    xaxis_title="Frequency",
                    yaxis_title="Concept",
                    plot_bgcolor='rgba(0,0,0,0)',
                    hoverlabel=dict(bgcolor="white", font_size=12),
                    height=350
                )
                st.plotly_chart(fig_concepts, use_container_width=True)

st.write("")

df = load_data()

df['Asked Date'] = pd.to_datetime(df['Asked Date'])
df['Highest Score Answer Date'] = pd.to_datetime(df['Highest Score Answer Date'])

views_per_month = df.groupby(df['Asked Date'].dt.to_period("M"))['Views'].sum()
questions_per_month = df.groupby(df['Asked Date'].dt.to_period("M")).size()

with st.container(border=True):
    st.subheader("DAX Question and View Trends Over Time")
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=views_per_month.index.astype(str), y=views_per_month.values,
                            mode='lines', name='Total Views',
                            line=dict(color='#1f77b4', width=2)))

    fig.add_trace(go.Scatter(x=questions_per_month.index.astype(str), y=questions_per_month.values,
                            mode='lines', name='Number of Questions',
                            line=dict(color='#ff7f0e', width=2), yaxis="y2"))

    fig.update_layout(
        xaxis_title='Date',
        yaxis=dict(
            title='Total Views',
            titlefont=dict(color='#1f77b4'),
            tickfont=dict(color='#1f77b4'),
            showgrid=False
        ),
        yaxis2=dict(
            title='Number of Questions',
            titlefont=dict(color='#ff7f0e'),
            tickfont=dict(color='#ff7f0e'),
            overlaying='y',
            side='right'),
        template="plotly_white",
        xaxis=dict(showgrid=False),
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5
        )
    )

    fig.add_vline(x='2015-07', line_width=1, line_dash="dash", line_color="#2ca02c")
    fig.add_annotation(x='2015-07', y=views_per_month.max(),
                    text="Power BI Launch", showarrow=True, arrowhead=1, ax=-50, ay=-40, arrowsize=1, arrowcolor='#2ca02c')

    fig.add_vline(x='2022-11', line_width=1, line_dash="dash", line_color="#d62728")
    fig.add_annotation(x='2022-11', y=views_per_month.max(),
                    text="ChatGPT Release", showarrow=True, arrowhead=1, ax=50, ay=-40, arrowsize=1, arrowcolor='#d62728')

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
        Note: DAX questions appear before Power BI's launch because DAX was introduced in 2009 
        as part of Project Gemini and included in the PowerPivot for Excel 2010 Add-in. 
        Power BI's standalone release in July 2015 significantly increased its adoption and 
        related questions.
        """)


st.write("")
with st.container(border=True):
    st.subheader("🏭 DAX Usage Across Industries")
    
    st.markdown("""
    This visualization illustrates the distribution of DAX queries across various industries. 
    It provides insights into which sectors are most actively utilizing DAX for data analysis and reporting.
    """)

    # Function to safely convert string representations of lists to actual lists
    def safe_eval(x):
        try:
            return ast.literal_eval(x)
        except ValueError:
            return []  # Return an empty list in case of error

    # Apply the conversion function to the 'Industries' column
    df['industries'] = df['industries'].apply(safe_eval)

    # Explode the 'Industries' column
    df_exploded_industries = df['industries'].explode()

    # Remove 'None' and empty entries
    df_exploded_industries = df_exploded_industries[df_exploded_industries.notna()]

    # Count the occurrences of each industry
    industry_counts = df_exploded_industries.value_counts().reset_index(name='Counts')
    industry_counts.columns = ['Industry', 'Counts']

    # Plot the industry distribution using a treemap
    fig_industries = px.treemap(
        industry_counts, 
        path=[px.Constant("Industries"), 'Industry'], 
        values='Counts',
        title="Industry Distribution of DAX Queries",
        color='Counts',
        color_continuous_scale='Viridis'
    )
    fig_industries.update_traces(textinfo='label+value+percent parent')
    fig_industries.update_layout(
        margin=dict(t=30, l=10, r=10, b=10),
        coloraxis_colorbar=dict(title="Query Count")
    )
    st.plotly_chart(fig_industries, use_container_width=True)

    st.caption("The size and color of each box represent the number of DAX queries associated with that industry.")



st.write("")



st.write("")

with st.container(border=True):
    st.subheader("📊 Key Insights and Analytics")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("🔥 Most Upvoted Answer", 
                  f"{df['Votes'].max()} votes", 
                  f"{df['Votes'].max() - df['Votes'].mean():.0f} above average")
        
        average_views = df['Views'].mean()
        above_average_views = df['Views'].max() - df['Views'].mean()
        st.metric("👁️ Most Viewed Question", 
                  f"{format(int(df['Views'].max()),',')} views", 
                  f"Average per Question: {format(int(average_views),',')} views")
    
    with col2:
        filtered_df = df[df['Highest Score Answer Author'] != 'Anonymous']

        top_answerer = filtered_df['Highest Score Answer Author'].value_counts().index[0]
        top_answer_count = filtered_df['Highest Score Answer Author'].value_counts().max()

        st.metric("🏆 Top Contributor", top_answerer, f"{top_answer_count} high-quality answers")
        
        st.metric("🧠 Expert Network Size", 
                  f"{filtered_df['Highest Score Answer Author'].nunique()} experts",
                  "Unique answer providers")

    st.markdown("---")
    
    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            with st.container(border=True):
                st.markdown("📊 **Answer Engagement Metrics**")
                st.markdown(f"""
                - Minimum Votes: {df['Votes'].min()}
                - Average Votes: {df['Votes'].mean():.1f}
                - Maximum Votes: {df['Votes'].max()}
                """)

            with st.container(border=True):
                st.markdown("🎯 **Question Response Analysis**")
                st.markdown(f"""
                - Average Answers per Question: {df['Number of Answers'].mean():.1f}
                - Most Discussed Question: {df['Number of Answers'].max()} responses
                - Modal Answer Count: {df['Number of Answers'].mode().values[0]}
                """)

        with col2:
            with st.container(border=True):
                st.markdown("💬 **Community Engagement Overview**")
                st.markdown(f"""
                - Total Answers: {df['Number of Answers'].sum():,}
                - Total Views: {format(int(df['Views'].sum()), ',')}
                - Average Views per Question: {format(int(df['Views'].mean()), ',')}
                """)

            with st.container(border=True):
                st.markdown("🏆 **Top Contributor Insights**")
                filtered_df_for_top_author = df[df['Highest Score Answer Author'] != 'Anonymous']
                top_author = filtered_df_for_top_author['Highest Score Answer Author'].value_counts().index[0]
                top_author_count = filtered_df_for_top_author['Highest Score Answer Author'].value_counts().max()
                st.markdown(f"""
                - Leading Contributor: {top_author}
                - Contributions by Leading Contributor: {top_author_count}
                - Unique Contributors: {filtered_df_for_top_author['Highest Score Answer Author'].nunique()}
                """)
        
        fig_histogram = px.histogram(df, x='Number of Answers', nbins=10, title='Distribution of Answers per Question', text_auto=True)

        fig_histogram.update_layout(
            xaxis_title='Number of Answers',
            yaxis_title='Frequency',
            template="plotly_white",
            bargap=0.2,
            height=300
        )

        st.plotly_chart(fig_histogram, use_container_width=True)

    st.info("💡 **Professional Tip:** To enhance your DAX proficiency, focus on mastering concepts associated with highly-viewed questions, as these often represent common challenges in the field.")

st.write("")

df['Asked Date'] = pd.to_datetime(df['Asked Date'])

with st.container(border=True):
    st.subheader("👀 Most Viewed Questions")
    
    num_questions = st.slider("Select number of top viewed questions to display", min_value=1, max_value=20, value=3)
    
    if st.button("🔍 Show Me", type="primary"):
        top_views = df.nlargest(num_questions, 'Views')[['context', 'dax_code_provided', 'correct_answer', 'concepts', 'Asked Date', 'Views', 'Number of Answers', 'URL']]

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

    if st.button("🔄 Okay, I'm done", type="primary"):
        st.rerun()

st.divider()
st.markdown("👨‍💻 Created by [Mandla Sibanda](https://www.linkedin.com/in/mandlasibanda/)")

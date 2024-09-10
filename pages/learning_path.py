import streamlit as st

st.title("Your Path to DAX Proficiency", anchor=False)
st.write("Embark on a structured journey to master Data Analysis Expressions (DAX).")

st.divider()

st.header(":material/description: Microsoft Documentation", anchor=False)
st.write(
    "Start with the authoritative source: Microsoft's official DAX documentation. "
    "This comprehensive resource serves as the primary reference for DAX, offering "
    "the most accurate and up-to-date information directly from the source."
)

col1, col2, col3 = st.columns(3)
with col1:
    st.link_button("Functions", "https://docs.microsoft.com/en-us/dax/dax-function-reference", use_container_width=True, type="primary")
with col2:
    st.link_button("Queries", "https://docs.microsoft.com/en-us/dax/dax-queries", use_container_width=True, type="primary")
with col3:
    st.link_button("Syntax", "https://docs.microsoft.com/en-us/dax/dax-syntax-reference", use_container_width=True, type="primary")

st.divider()

st.header(":material/trophy: SQLBI: Comprehensive DAX Resource", anchor=False)
st.write(
    "SQLBI, founded by industry experts Marco Russo and Alberto Ferrari, is a premier "
    "destination for DAX learning. It offers an extensive repository of knowledge, "
    "from foundational concepts to advanced techniques, catering to all proficiency levels."
)
st.link_button("Visit SQLBI", "https://www.sqlbi.com/", type="primary")

st.divider()

st.header(":material/home_storage: Additional Learning Resources", anchor=False)

resources = {
    "Books": [
        ("The Definitive Guide to DAX", "https://www.sqlbi.com/books/the-definitive-guide-to-dax-2nd-edition/"),
        ("DAX Formulas for PowerPivot", "https://www.sqlbi.com/books/dax-formulas-for-powerpivot/"),
        ("Analyzing Data with Power BI", "https://www.microsoftpressstore.com/store/analyzing-data-with-power-bi-and-power-pivot-for-excel-9781509302765"),
        ("Power Pivot and Power BI", "https://powerpivotpro.com/the-book/"),
        ("M Is for (Data) Monkey", "https://www.amazon.com/Data-Monkey-Guide-Language-Excel/dp/1615470344"),
        ("Pro DAX with Power BI", "https://www.apress.com/gp/book/9781484239384")
    ],
    "Blogs": [
        ("PowerPivotPro", "https://powerpivotpro.com/"),
        ("Kasper On BI", "https://www.kasperonbi.com/"),
        ("SQLBI Blog", "https://www.sqlbi.com/articles/"),
        ("Chris Webb's BI Blog", "https://blog.crossjoin.co.uk/"),
        ("Excelerator BI", "https://exceleratorbi.com.au/blog/"),
        ("Rad Reza", "https://radacad.com/blog")
    ],
    "YouTube Channels": [
        ("Guy in a Cube", "https://www.youtube.com/channel/UCFp1vaKzpfvoGai0vE5VJ0w"),
        ("Curbal", "https://www.youtube.com/channel/UCJ7UhloHSA4wAqPzyi6TOkw"),
        ("SQLBI", "https://www.youtube.com/user/sqlbitv"),
        ("PowerBI.Tips", "https://www.youtube.com/channel/UCFp1vaKzpfvoGai0vE5VJ0w"),
        ("Enterprise DNA", "https://www.youtube.com/channel/UCy2rBgj4M1tzK-urTZ28zcA"),
        ("Pragmatic Works", "https://www.youtube.com/user/PragmaticWorks")
    ],
    "Websites": [
        ("Microsoft Learn", "https://learn.microsoft.com/en-us/power-bi/"),
        ("DAX Guide", "https://dax.guide/"),
        ("Power BI Community", "https://community.powerbi.com/"),
        ("DAX Patterns", "https://www.daxpatterns.com/"),
        ("Power BI Tips", "https://powerbi.tips/"),
        ("RADACAD", "https://radacad.com/")
    ]
}

for category, items in resources.items():
    with st.expander(category):
        for item, link in items:
            st.markdown(f"- [{item}]({link})")

st.divider()

st.header(":material/exercise: Practice Makes Perfect", anchor=False)
st.write("Consistent practice is key to mastering DAX. Here are some effective ways to hone your skills:")

practices = [
    "**Daily DAX**: Write at least one DAX formula every day.",
    "**Reverse Engineer**: Analyze existing reports and recreate their measures.",
    "**DAX Challenges**: Solve various DAX challenges to test your skills.",
    "**Teach Others**: Solidify your knowledge by explaining concepts to others."
]

for practice in practices:
    st.markdown(practice)

st.divider()

st.header(":material/link: More Resources", anchor=False)
st.write("Check out these additional resources to further enhance your DAX skills:")

col1, col2 = st.columns(2)
with col1:
    st.link_button("DAX Patterns", "https://www.daxpatterns.com/", use_container_width=True, type="primary")
with col2:
    st.link_button("Power BI Community", "https://community.powerbi.com/", use_container_width=True, type="primary")

st.divider()

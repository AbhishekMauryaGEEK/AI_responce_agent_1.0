import streamlit as st
from src.tools.web_search import WebSearcher
from src.tools.extract_content import ContentExtractor
from src.agents.summarizer import AISummarizer
API_KEY = ""
SEARCH_ENGINE_ID = ""

searcher = WebSearcher(API_KEY, SEARCH_ENGINE_ID)
extractor = ContentExtractor()
summarizer = AISummarizer()

st.set_page_config(page_title="AI Research Agent", layout="wide")
st.title("🔍 AI Research Agent")

with st.form(key='research_form'):
    query = st.text_input("Enter your research topic:", placeholder="e.g. quantum computing breakthroughs 2025")
    num_results = st.slider("Number of search results to process", min_value=1, max_value=10, value=5)
    submit_button = st.form_submit_button(label='Start Research')

if submit_button:
    if not query.strip():
        st.warning("Please enter a valid research topic!")
    else:
        try:
            with st.spinner("Performing web search..."):
                search_results = searcher.search(query, num_results=num_results)
                urls = [item["link"] for item in search_results]
            if not urls:
                st.info("No search results found. Try a different query.")
            else:
                st.success(f"Found {len(urls)} results.")

                with st.spinner("Extracting content from articles..."):
                    articles = extractor.extract_multiple(urls)

                # Display results summary
                st.header("Search Results & Summaries")
                for i, article in enumerate(articles, 1):
                    if article:
                        with st.expander(f"{i}. {article['title']}"):
                            st.markdown(f"[Read full article here]({article['url']})")
                            show_summary = st.checkbox("Show Summary", key=f"sum{i}")
                            if show_summary:
                                summary = summarizer.summarize_text(article['text'])
                                st.write(summary)
                    else:
                        st.warning(f"Article {i} content could not be extracted.")

                with st.spinner("Generating overall synthesis summary..."):
                    full_texts = " ".join([a['text'] for a in articles if a])
                    overall_summary = summarizer.summarize_text(full_texts)

                st.header("Overall Research Summary")
                st.write(overall_summary)

        except Exception as e:
            st.error(f"Oops! Something went wrong: {e}")

import requests
import streamlit as st


# -----------------------------------------
# Configuration
# -----------------------------------------

API_URL = "https://urban-possibility-club-scale.trycloudflare.com/research"

RESEARCH_URL = f"{API_URL}/research"


# -----------------------------------------
# Page Configuration
# -----------------------------------------

st.set_page_config(
    page_title="Company Research AI",
    page_icon="🔎",
    layout="wide"
)


# -----------------------------------------
# Custom CSS
# -----------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #666666;
        margin-bottom: 30px;
    }

    .source-card {
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #dddddd;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# -----------------------------------------
# Header
# -----------------------------------------

st.markdown(
    '<div class="main-title">🔎 Company Research AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Research companies using live internet data with Tavily + Groq'
    '</div>',
    unsafe_allow_html=True
)


# -----------------------------------------
# Sidebar
# -----------------------------------------

with st.sidebar:

    st.header("About")

    st.write(
        """
        This AI research assistant searches the
        live internet and generates an answer
        using Groq.
        """
    )

    st.divider()

    st.subheader("Technology")

    st.write("🔎 Tavily — Web Search")
    st.write("🧠 Groq — LLM")
    st.write("⚡ FastAPI — Backend")
    st.write("🎨 Streamlit — Frontend")


# -----------------------------------------
# Query Input
# -----------------------------------------

st.subheader("Ask your research question")

query = st.text_area(
    "Enter your question",
    placeholder=(
        "Example: What are the latest projects, "
        "partnerships and technology developments "
        "of Tata Motors in 2026?"
    ),
    height=120
)


# -----------------------------------------
# Example Questions
# -----------------------------------------

st.write("**Example questions:**")

col1, col2, col3 = st.columns(3)

with col1:

    if st.button(
        "Tata Motors latest projects",
        use_container_width=True
    ):

        query = (
            "What are the latest projects of "
            "Tata Motors in 2026?"
        )


with col2:

    if st.button(
        "Latest company news",
        use_container_width=True
    ):

        query = (
            "What are the latest major developments "
            "of Tata Motors in the last 30 days?"
        )


with col3:

    if st.button(
        "Technology developments",
        use_container_width=True
    ):

        query = (
            "What are the latest technology developments "
            "of Tata Motors?"
        )


# -----------------------------------------
# Research Button
# -----------------------------------------

if st.button(
    "🔎 Research",
    type="primary",
    use_container_width=True
):

    if not query.strip():

        st.warning(
            "Please enter a research question."
        )

    else:

        with st.spinner(
            "Searching the live internet and analyzing the results..."
        ):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "query": query
                    },
                    timeout=120
                )


                # -----------------------------------------
                # Successful response
                # -----------------------------------------

                if response.status_code == 200:

                    data = response.json()

                    answer = data.get(
                        "answer",
                        ""
                    )

                    sources = data.get(
                        "sources",
                        []
                    )


                    # -----------------------------------------
                    # Answer
                    # -----------------------------------------

                    st.divider()

                    st.subheader("📋 Research Result")

                    st.markdown(answer)


                    # -----------------------------------------
                    # Sources
                    # -----------------------------------------

                    st.divider()

                    st.subheader("🔗 Sources")

                    if sources:

                        for index, source in enumerate(
                            sources,
                            start=1
                        ):

                            title = source.get(
                                "title",
                                "Source"
                            )

                            url = source.get(
                                "url",
                                ""
                            )

                            st.markdown(
                                f"""
                                **{index}. [{title}]({url})**
                                """
                            )

                    else:

                        st.info(
                            "No sources were returned."
                        )


                # -----------------------------------------
                # API error
                # -----------------------------------------

                else:

                    try:

                        error_data = response.json()

                        error_message = error_data.get(
                            "detail",
                            "Unknown API error"
                        )

                    except Exception:

                        error_message = response.text


                    st.error(
                        f"API Error: {error_message}"
                    )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to FastAPI. "
                    "Make sure the backend is running."
                )


            except requests.exceptions.Timeout:

                st.error(
                    "The request timed out. "
                    "The web search may be taking longer than expected."
                )


            except Exception as e:

                st.error(
                    f"Unexpected error: {str(e)}"
                )

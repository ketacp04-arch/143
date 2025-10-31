import streamlit as st
import pandas as pd
import datetime

# --- Configuration ---
st.set_page_config(
    page_title="Indian Market News Aggregator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Define the market segments and timeframes based on the user request
MARKET_SEGMENTS = {
    "Large Cap FNO": "Nifty 50, Sensex, Reliance, HDFC Bank, Large Cap FNO news",
    "Mid Cap FNO": "Nifty Midcap 100, Midcap FNO news",
    "Small Cap FNO": "Nifty Smallcap 100, Smallcap FNO news",
    "All FNO": "Indian F&O market news, derivative segment"
}

TIMEFRAME_OPTIONS = [
    "Last One Week",
    "Last One Month",
    "Last Three Months"
]

# A simple function to simulate fetching news from a News API
# NOTE: In a real application, you would replace this function with code that
# uses a library like 'newsapi-python' or a dedicated financial news API.
# The 'search_query' and 'timeframe' would be used to filter the actual API call.
@st.cache_data(ttl=3600) # Cache the result for 1 hour to reduce API calls
def fetch_mock_news(segment_key, timeframe):
    """
    Mocks an API call to fetch news articles based on segment and timeframe.

    Args:
        segment_key (str): The display name of the market segment.
        timeframe (str): The selected time frame.

    Returns:
        list: A list of mock news articles (dictionaries).
    """
    search_query = MARKET_SEGMENTS[segment_key]
    
    # Calculate the simulated date based on the timeframe
    today = datetime.date.today()
    if timeframe == "Last One Week":
        start_date = today - datetime.timedelta(days=7)
    elif timeframe == "Last One Month":
        start_date = today - datetime.timedelta(days=30)
    else: # Last Three Months
        start_date = today - datetime.timedelta(days=90)

    # Generate mock data
    articles = []
    num_articles = 5
    for i in range(1, num_articles + 1):
        article_date = start_date + datetime.timedelta(days=i * 5)
        articles.append({
            "title": f"({segment_key}) Market Update: {search_query.split(',')[0].strip()} Shows Volatility {i}",
            "source": f"Financial Times {i % 3 + 1}",
            "date": article_date.strftime("%Y-%m-%d"),
            "summary": f"Detailed analysis shows that {segment_key} indices experienced a sharp rise followed by a consolidation phase over the {timeframe} period. Key drivers included FII activity and sector-specific policy changes. The outlook remains cautious.",
            "url": f"https://mock-news.com/{segment_key.replace(' ', '-').lower()}-{i}"
        })
    return articles

# --- Streamlit UI Components ---

st.title("💰 Indian Market News Aggregator")
st.markdown("Use the filters on the left to track FNO, Midcap, Smallcap, and Largecap news over different time periods.")

# --- Sidebar Filters ---
with st.sidebar:
    st.header("News Filters")
    
    selected_segment = st.selectbox(
        "Select Market Segment:",
        options=list(MARKET_SEGMENTS.keys()),
        index=0,
        help="Choose the specific market segment you want news for."
    )

    selected_timeframe = st.selectbox(
        "Select Timeframe:",
        options=TIMEFRAME_OPTIONS,
        index=1, # Default to Last One Month
        help="Select the period for which to retrieve historical news. Note: Actual news filtering by date depends on the external API used."
    )
    
    # Button to trigger the data fetch (optional, but good for control)
    st.subheader("Action")
    if st.button("Fetch Latest News"):
        st.session_state.run_fetch = True
    
    if 'run_fetch' not in st.session_state:
        st.session_state.run_fetch = True

# --- Main Content Display ---

if st.session_state.run_fetch:
    st.subheader(f"News for {selected_segment} ({selected_timeframe})")
    
    with st.spinner(f"Searching for news on {selected_segment}..."):
        # Fetch the news using the mock function
        news_data = fetch_mock_news(selected_segment, selected_timeframe)
    
    if news_data:
        # Sort news by date descending for better relevance
        df = pd.DataFrame(news_data)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values(by='date', ascending=False)
        
        # Display each article using a Streamlit Expander
        for index, row in df.iterrows():
            with st.expander(f"**{row['title']}** - ({row['source']} | {row['date'].strftime('%b %d, %Y')})"):
                st.write(row['summary'])
                st.markdown(f"**Read Full Article:** [Click Here]({row['url']})")
                
        st.success("News articles loaded successfully.")

        st.markdown(
            """
            ---
            **How to integrate a real News API (e.g., NewsAPI.org):**
            1. Sign up and get your API Key.
            2. Install the library: `pip install newsapi-python`
            3. Modify the `fetch_mock_news` function to use the API:
               ```python
               # from newsapi import NewsApiClient
               # newsapi = NewsApiClient(api_key='YOUR_API_KEY')
               # def fetch_real_news(segment, timeframe):
               #     # Calculate start_date based on 'timeframe'
               #     # articles = newsapi.get_everything(q=MARKET_SEGMENTS[segment], from_param=start_date, ...)
               #     # ... process and return articles
               ```
            4. Rename `fetch_mock_news` to `fetch_real_news` and update the call.
            """
        )
    else:
        st.info(f"No news found for **{selected_segment}** in the last {selected_timeframe.lower()}.")

# Add a footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown("Developed with Streamlit for Financial Data Aggregation")

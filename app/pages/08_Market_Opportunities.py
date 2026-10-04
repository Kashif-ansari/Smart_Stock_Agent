import streamlit as st
from app.integrations.market_search import search_public
st.title("Market Opportunities")
q=st.text_input("Public research query","grocery product trends Pakistan")
if st.button("Research"):
    try:
        for r in search_public(q): st.markdown(f"**{r['title']}**\n\n{r['snippet']}\n\n{r['url']}\n\nRetrieved: {r['retrieved_at']}")
    except Exception as e: st.error(f"Search unavailable: {e}")
st.caption("Public-search evidence is not equivalent to verified sales. New-product quantities should be treated as uncertain pilot scenarios.")

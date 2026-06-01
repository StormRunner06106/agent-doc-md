import pandas as pd
import streamlit as st

from db import connect, init_db
from nl_to_sql import to_sql


st.set_page_config(page_title="Eshop NL to SQL", layout="wide")
init_db()

st.title("Eshop Natural Language to SQL")

prompt = st.text_input(
    "Ask a question",
    "Show revenue by order",
    placeholder="Example: show top products by quantity sold",
)

if st.button("Run query", type="primary") and prompt.strip():
    try:
        sql = to_sql(prompt)
        st.code(sql, language="sql")

        with connect() as conn:
            df = pd.read_sql_query(sql, conn)
        st.dataframe(df, use_container_width=True)
    except Exception as exc:
        st.error(str(exc))

with st.expander("Example prompts"):
    st.markdown(
        """
        - Show all users
        - Show all products
        - Show top products by quantity sold
        - Show revenue by order
        - Show customers by city
        """
    )

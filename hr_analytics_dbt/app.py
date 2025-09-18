import streamlit as st
import pandas as pd
import snowflake.connector

st.set_page_config(page_title="Jobbannonser Dashboard", layout="wide")

SF = st.secrets["snowflake"]

@st.cache_resource(show_spinner=False)
def get_conn():
    return snowflake.connector.connect(
        user=SF["user"],
        password=SF["password"],
        account=SF["account"],
        warehouse=SF["warehouse"],
        database=SF["database"],
        schema=SF["schema"],
    )

@st.cache_data(show_spinner=True, ttl=300)
def load_data(mart_table_name: str):
    fq_table = f'{SF["database"]}.{SF["schema"]}.{mart_table_name}'
    query = f"SELECT * FROM {fq_table}"
    conn = get_conn()
    df = pd.read_sql(query, conn)
    df.columns = [c.lower() for c in df.columns]
    if "application_deadline" in df.columns:
        df["application_deadline"] = pd.to_datetime(df["application_deadline"], errors="coerce")
    # ensure vacancies exists
    if "vacancies" not in df.columns:
        df["vacancies"] = 0
    return df

st.title("Jobbannonser Dashboard")

mart_tables = {
    "Administration, ekonomi, juridik": "MART_ADMINISTRATION_EKONOMI_JURIDIK",
    "Hälso- och sjukvård": "MART_HALSO_OCH_SJUKVARD",
    "Försäljning, inköp, marknadsföring": "MART_FORSALJNING_INKOP_MARKNADSFORING"
}

selected_field = st.selectbox("Välj yrkesområde:", list(mart_tables.keys()))
mart_table_name = mart_tables[selected_field]

df = load_data(mart_table_name)
filtered = df 

k1, k2 = st.columns(2)
k1.metric("Antal annonser", len(filtered))
k2.metric("Totala lediga tjänster", int(filtered["vacancies"].fillna(0).sum()))


st.subheader("Detaljerade annonser")
st.dataframe(filtered, use_container_width=True)

if not filtered.empty:
    st.subheader("Vacancies per arbetsgivare")
    st.bar_chart(filtered.groupby("employer_name")["vacancies"].sum())


import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px
 
st.set_page_config(page_title="Jobbannonser Dashboard", layout="wide")
 
SF = st.secrets["snowflake"]
 
@st.cache_resource
def get_conn():
    return snowflake.connector.connect(
        account="FMVXUQS-IF87024",   
        user="DBT_USER",             
        password="RANDOM_PASSWORD",   
        role="TRANSFORM_DBT_ROLE",   
        warehouse="HR_ANALYTICS_WH",
        database="HR_ANALYTICS",
        schema="MART",              
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
    if "vacancies" not in df.columns:
        df["vacancies"] = 0
    return df
 
def style_bar_chart(df, x_col, y_col, title):
    
    df = df.sort_values(x_col, ascending=False)
    fig = px.bar(
        df, x=x_col, y=y_col, orientation='h',
        text=df[x_col],
        title=title,
        color=y_col,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(
        textposition='outside',
        texttemplate='<b>%{text}</b>',
        textfont=dict(color='black', size=14),
        cliponaxis=False,
        showlegend=False
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=50, b=10)
    )
    return fig
 
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
 

top_vacancies_region = filtered.groupby("workplace_region")["vacancies"].sum().nlargest(5)
top_vacancies_occupation = filtered.groupby("occupation")["vacancies"].sum().nlargest(5)
top_employers = filtered.groupby("employer_name")["vacancies"].sum().nlargest(5)
employment_type_counts = filtered["employment_type"].value_counts()
 

top_vacancies_region_df = top_vacancies_region.reset_index()
top_vacancies_occupation_df = top_vacancies_occupation.reset_index()
top_employers_df = top_employers.reset_index()
 

c1, c2 = st.columns(2)
with c1:
    fig1 = style_bar_chart(top_vacancies_region_df, 'vacancies', 'workplace_region', 'Top 5 regioner efter lediga tjänster')
    st.plotly_chart(fig1, use_container_width=True, height=500)
 
with c2:
    fig2 = style_bar_chart(top_vacancies_occupation_df, 'vacancies', 'occupation', 'Top 5 yrken efter lediga tjänster')
    st.plotly_chart(fig2, use_container_width=True, height=500)
 
c3, c4 = st.columns(2)
with c3:
    fig3 = style_bar_chart(top_employers_df, 'vacancies', 'employer_name', 'Top 5 arbetsgivare efter lediga tjänster')
    st.plotly_chart(fig3, use_container_width=True, height=500)
 
with c4:
    fig4 = px.pie(
        values=employment_type_counts.values,
        names=employment_type_counts.index,
        title='Antal annonser per anställningstyp',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig4.update_traces(
        textinfo='label',  
        hovertemplate='%{label}: %{percent}', 
        pull=[0.05]*len(employment_type_counts)
    )
    fig4.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10,r=10,t=50,b=10),
        legend_title_text='Percentage',
    )
    st.plotly_chart(fig4, use_container_width=True, height=500)
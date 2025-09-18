HR Analytics Data Warehouse - Group viktor, Abdirahman & Mustafa 
📌 Project Overview
Detta projekt implementerar en modern data stack för att lösa HR-analysutmaningar för en talangförmedlingsbyrå. Vårt system automatiserar extraktion, transformering och analys av jobbmarknadsdata från Arbetsförmedlingen (Jobtech API) för att hjälpa rekryterare och HR-specialister fatta datadrivna beslut.
🏗️ Architecture
Dataflödet följer principerna för en modern data stack:
Jobtech API → dlt → Snowflake → dbt → Streamlit Dashboard
Data Source: Jobtech API (Arbetsförmedlingen)
Data Ingestion: dlt (data load tool)
Data Warehouse: Snowflake
Data Transformation: dbt (data build tool)
Analytics Layer: Streamlit Dashboard
📊 Data Model
Fact Table: fact_job_ads — central fact-tabell med jobbannons-metriker
Dimension Tables:
dim_occupation — yrkesinformation och klassificeringar
dim_employer — arbetsgivardata
dim_location — geografisk information (städer, regioner)
dim_date — datumdimension för tidsbaserad analys
Schema Organization:
Staging Schema: rådata laddat via dlt
Data Warehouse Schema: strukturerad, ren datamodell
Mart Schema: affärsanpassade vyer för specifika yrkesfält
🚀 Getting Started
Prerequisites
Python 3.9+
Git
Snowflake-konto
dbt installerat
(valfritt) UV package manager
Installation
Klona repot
git clone https://github.com/Mustafa44536/projekt_hr_analytics.git
cd projekt_hr_analytics
Skapa och aktivera virtuell miljö
python3 -m venv .venv
source .venv/bin/activate   
Installera beroenden
pip install -r requirements.txt
Konfigurera dbt
dbt deps
Kontrollera att din profiles.yml är korrekt konfigurerad med dina Snowflake-uppgifter.
5. Ställ in hemligheter: Skapa en .streamlit/secrets.toml i hr_analytics_dbt/ med:
[snowflake]
user = "DITT_ANVÄNDARNAMN"
password = "DITT_LÖSENORD"
account = "DITT_ACCOUNT"
warehouse = "DITT_WAREHOUSE"
database = "DITT_DATABASE"
schema = "DITT_SCHEMA"
⚡ Usage
Data Ingestion: Kör dlt-pipelinen för att hämta data från Jobtech API:
python scripts/load_job_ads.py
Data Transformation: Kör dbt-modeller och tester:
dbt run
dbt test
Dashboard: Starta Streamlit-appen:
cd hr_analytics_dbt
streamlit run app.py
✅ Data Quality & Testing
För att verifiera datakvalitet kör:
dbt test
📖 Documentation
Generera och visa dbt-dokumentation:
dbt docs generate
dbt docs serve
📂 Project Structure
projekt_hr_analytics/
├── hr_analytics_dbt/         
│   ├── app.py
│   ├── .streamlit/
│   │   └── secrets.toml
│   └── models/
│       ├── staging/
│       ├── warehouse/
│       └── marts/
├── dlt_code/                 
├── worksheets_sql/           
├── requirements.txt
├── .gitignore
└── README.md
👨‍💻 Team Members
Mustafa
Abdirahman
Viktor
📄 License
Detta projekt är en del av en akademisk inlämning och är endast avsett för utbildningssyften.
Obs: Projektet använder riktig data från Arbetsförmedlingens Jobtech API. Se till att följa deras användarvillkor och dataskyddspolicyer.
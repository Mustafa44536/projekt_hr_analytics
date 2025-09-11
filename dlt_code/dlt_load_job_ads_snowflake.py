# projekt/dlt_load_job_ads_snowflake.py
import requests
import dlt
from typing import Iterable, Dict

def fetch_job_ads(occupation_field: str, limit: int = 100) -> Iterable[Dict]:
    url = "https://jobsearch.api.jobtechdev.se/search"
    offset = 0
    while True:
        params = {"occupation-field": occupation_field, "limit": limit, "offset": offset}
        resp = requests.get(url, params=params)
        resp.raise_for_status()
        j = resp.json()
        hits = j.get("hits", [])
        if not hits:
            break
        for hit in hits:
            # lägg till fält för spårbarhet
            hit["_ingested_occupation_field"] = occupation_field
            yield hit
        offset += limit
        # skydd mot oändlig loop
        if offset > 20000:
            break

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="job_ads_pipeline",
        destination="snowflake",
        dataset_name="staging",   # maps to HR_ANALYTICS.STAGING
    )

    occupation_fields = [
        "administration-ekonomi-juridik",
        "halso-och-sjukvard",
        "forsaljning-inkop-marknadsforing"
    ]

    # Kör en körning per område — allt landar i STAGING.job_ads
    for area in occupation_fields:
        print(f"Loading area: {area} ...")
        data_iter = fetch_job_ads(area, limit=100)
        info = pipeline.run(data_iter, table_name="job_ads")
        print(info)

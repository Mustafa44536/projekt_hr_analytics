import dlt
import requests
import json
from pathlib import Path
import os

def _get_ads(url_for_search, params):
    headers = {"accept": "application/json"}
    response = requests.get(url_for_search, headers=headers, params=params)
    response.raise_for_status()  # check for HTTP errors
    return json.loads(response.content.decode("utf8"))


@dlt.resource(write_disposition="replace")
def jobads_resource(params, occupation_fields):
    url = "https://jobsearch.api.jobtechdev.se"
    url_for_search = f"{url}/search"
    limit = params.get("limit", 100)

    for occ_field in occupation_fields:
        offset = 0
        while True:
            params_with_pagination = {
                **params,
                "occupation-field": occ_field,
                "offset": offset,
                "limit": limit,
            }

            try:
                data = _get_ads(url_for_search, params_with_pagination)
            except requests.exceptions.HTTPError as e:
                # stop pagination if the API returns a 400
                print(f"Reached end of results for {occ_field} at offset {offset}.")
                break

            hits = data.get("hits", [])
            if not hits:
                break

            for ad in hits:
                yield ad

            offset += limit


def run_pipeline(table_name):
    pipeline = dlt.pipeline(
        pipeline_name="jobsearch",
        destination="snowflake",
        dataset_name="staging",
    )

    # params without occupation-field, added later per field
    params = {"limit": 100}

    occupation_fields = [
        "X82t_awd_Qyc",
        "NYW6_mP6_vwf",
        "RPTn_bxG_ExZ",
    ]

    load_info = pipeline.run(
        jobads_resource(params=params, occupation_fields=occupation_fields),
        table_name=table_name,
    )
    print(load_info)


if __name__ == "__main__":
    working_directory = Path(__file__).parent
    os.chdir(working_directory)

    run_pipeline(table_name="admin_healthcare_sales_job_ads")
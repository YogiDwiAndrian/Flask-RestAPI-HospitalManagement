from google.cloud import bigquery
from google.oauth2 import service_account
import json

credentials = service_account.Credentials.from_service_account_file(
'delman.json')

client = bigquery.Client(location="US")
print("Client creating using default project: {}".format(client.project))

project_id = 'delman-interview'
client = bigquery.Client(credentials= credentials,project=project_id)


query = """
    SELECT *
    FROM `delman-interview.interview_mock_data.vaccine-data`
"""
query_job = client.query(
    query,
    # Location must match that of the dataset(s) referenced in the query.
    location="US",
)  # API request - starts the query
for row in query_job:
    print(dict(row))
# records = [dict(row) for row in query_job]
# json_obj = json.dumps(str(records))

# print(json_obj)

# results = query_job.result()
# for result in results:
#     print(result)

# schema = results.schema

# print(f'schema : {schema}')
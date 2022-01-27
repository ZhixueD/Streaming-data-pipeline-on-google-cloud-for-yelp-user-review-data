import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, StandardOptions
import os
from apache_beam import window
from google.cloud import pubsub_v1
import argparse
import json

# Replace 'my-service-account-path' with your service account path
service_account_path = 'token.json'
print("Service account file : ", service_account_path)
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path

# Replace 'my-project' with your project id
gcp_project = 't-osprey-337221'

# your pubsub topic
pubsub_topic = 'yelp_review'
publisher = pubsub_v1.PublisherClient()

topic_path = publisher.topic_path(gcp_project, pubsub_topic)

#GCS storage bucket
BUCKET='yelp-streaming-pipeline'


# Bigquery project-id:dataset_id.table_id
table_spec_review = 't-osprey-337221:yelp_streaming.yelp_review_test'


# column_name:BIGQUERY_TYPE, ...
table_schema_review = 'review_id:string, user_id:string, business_id:string, stars: FLOAT64, useful:integer, funny:integer, cool:integer, date:DATETIME'
	


parser = argparse.ArgumentParser()
# parser.add_argument('--my-arg', help='description')
args, beam_args = parser.parse_known_args()

# Create and set your PipelineOptions.
# For Cloud execution, specify DataflowRunner and set the Cloud Platform
# project, job name, temporary files location, and region.
# For more information about regions, check:
# https://cloud.google.com/dataflow/docs/concepts/regional-endpoints

beam_options = PipelineOptions(
    beam_args,
    runner='DataflowRunner',
    project=gcp_project,
    job_name='yelp-streaming-review-pipeline',
    temp_location='gs://yelp-streaming-pipeline/staging',
    region='us-central1')
beam_options.view_as(StandardOptions).streaming = True

"""
def type_change(line):
    line['review_id']=str(line['review_id'])
    line['user_id']=str(line['user_id'])
    line['business_id']=str(line['business_id'])
    line['stars']=float(line['stars'])
    line['useful']=int(line['useful'])
    line['funny']=int(line['funny'])
    line['cool']=int(line['cool'])
    line['date']=str(line['date'])
"""
def run():

    p = beam.Pipeline(options=beam_options)


    pubsub_data = (
                    p 
                    | 'Read from pub sub' >> beam.io.ReadFromPubSub(topic=topic_path)
                    |'To Json' >> beam.Map(lambda e: json.loads(e.decode('utf-8')))
                    |'remove text column' >> beam.Map(lambda x:  {key:val for key, val in x.items() if key != 'text'})
                    #|'change type' >> beam.Map(type_change)
                    |'Write to BigQuery' >> beam.io.gcp.bigquery.WriteToBigQuery(
                                 table_spec_review,
                                 schema=table_schema_review,
                                 #method=beam.io.WriteToBigQuery.Method.FILE_LOADS,
                                 #triggering_frequency=1, 
                                 write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND,
                                 create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED)
                   )

    result = p.run()
    #result.wait_until_finish()


if __name__ == '__main__':
   run()
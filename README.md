# Build a streaming data pipeline on google cloud by using Pub/Sub, dataflow, apache beam, Bigquery, Tableau

![dataflow pipeline model](https://user-images.githubusercontent.com/98153604/151060089-9ffaa826-fed6-44a1-b84f-b0c508050805.png)

Streaming data pipelines, by extension, is a data pipeline architecture that handle millions of events at scale, in real time. That capability allows for applications, analytics, and reporting in real time. 

How do streaming data pipelines work? 
The first step in a streaming data pipeline is that the information enters the pipeline. Next, software decouples applications, which creates information from the applications using it. That allows for the development of low-latency streams of data (which can be transformed as necessary).'

What is Yelp used for?
With unmatched local business information, photos and review content, Yelp provides a one-stop local platform for consumers to discover, connect and transact with local businesses of all sizes by making it easy to request a quote, join a waitlist, and make a reservation, appointment or purchase.

In this project, I simulate yelp website which continuously collect million's user review on local businesses. Here, I write a python code which can simulate users continuously publish reviews to a Pub/Sub topic. And then, I write a apache beam (python) code to run a streaming dataflow pipeline, do some simple data cleaning and load it to Bigquery data warehouse in real time. Therefore, I can writen SQL code to analyze and report result in real time. And serching reviews for certain business in realtime. The whole streaming pipeline is runing on Google cloud platform.

The whole project include:

1. Install python packages using VM instance
2. Prepare data for publish in Google cloud storage, upload python file to GCS and create ad temp folder in GCS bucket
3. Create a Pub/Sub topic
4. Create and download the JSON key On your Service Account page
5. Create Bigquery dataset and table with data type
6. Copy json key file, 2 python file from google cloud storage to VM storage
7. Simulate users's review data and publish it the Pub/Sub topic
8. Launch Dataflow Pipeline
9. Check dataflow console and Bigquery
10. Tableau connect Bigquery for visulization in real time

## 1. Install python packages using VM instance
In the Console, on the Navigation menu, click Compute Engine > VM instances.
Create a VM instance, region is 'europe-north1'.

![VM](https://user-images.githubusercontent.com/98153604/151070388-7719bb62-52c4-410e-9c2c-3029f64e58eb.JPG)

On the far right, under Connect, click on SSH to open a terminal window.

Run CLI commands in VM instance to intall packages:
      
      sudo apt-get install python3-pip
      sudo pip3 install google-cloud-pubsub==2.9.0
      sudo pip3 install google-cloud-storage
      sudo pip3 install gcsfs
      sudo pip3 install apache-beam[gcp]
      sudo pip3 install oauth2client==3.0.0
      sudo pip3 install -U pip
      
## 2. prepare data, python file and create temp-folder in google cloud storage 
(1). Prepare data for publishing in Google cloud storage.
Here I choose data from my another project, that is the user review data from yelp website, it is already stored in google cloud storage.I will publish this data, 1message per 2 seconds.

![data source](https://user-images.githubusercontent.com/98153604/151121168-13a120fb-7099-477a-afc2-fd5d4b63f8fc.JPG)

(2). Upload  two python files to google cloud storage, yelp_dataflow_test.py for dataflow pipeline, yelp_publish_to_topic2.py for publish the data from google cloud storage to Pub/Sub topic.
![cloud_storage](https://user-images.githubusercontent.com/98153604/151121881-b7e3909b-f529-410f-a2e4-0e91badafece.JPG)

(3). Create ad temp folder in google cloud storage

     yelp-streaming-pipeline/staging

## 3. Create a Pub/Sub topic and subscription

Create a Pub/Sub topic and choose create a default subscription in google Pub/Sub, name the topic: yelp_review
![topic](https://user-images.githubusercontent.com/98153604/151240661-3f2e65d4-249c-42a3-96fc-f97e3070ae97.JPG)

## 4. Create and download the JSON key On your Service Account page

This key will used later in python code, for python to connect your Pub/Sub topic, when you add a key in you IAM , service account. Add key, and a json file will be download,
And this Json file is the key, be careful keep it. And upload it to Google cloud storage.
![key](https://user-images.githubusercontent.com/98153604/151241860-fb6d172a-a3e9-4e4e-bcd4-21dfa23c19a0.JPG)

## 5. Create Bigquery dataset and table with data type
This table used for dataflow to load the streaming data into it in realtime.

![bigquery](https://user-images.githubusercontent.com/98153604/151242594-73276465-82d2-4ed9-a5c2-e2f3812d3695.JPG)

## 6. Copy json key file, 2 python file from google cloud storage to VM storage

   gsutil cp gs://yelp-streaming-pipeline/yelp_publish_to_topic2.py yelp_publish_to_topic2.py
   
   gsutil cp gs://yelp-streaming-pipeline/yelp_dataflow_test.py yelp_dataflow_test.py
   
   gsutil cp gs://yelp-streaming-pipeline/token.json token.json

![VM ls](https://user-images.githubusercontent.com/98153604/151244256-9d1ab835-c094-494c-95ff-13388ceb970d.JPG)

## 7. Simulate users's review data and publish it the Pub/Sub topic

run command line code:
      
      python3 yelp_publish_to_topic2.py
      
The python code:
      
      import os
      import time 
      from google.cloud import pubsub_v1
      #from google.cloud import storage
      import gcsfs
      
      if __name__ == "__main__":

          # Replace 'my-project' with your project id
          gcp_project = 't-osprey-337221'

          # Replace 'my-topic' with your pubsub topic
          pubsub_topic = 'yelp_review'

          # Replace 'my-service-account-path' with your service account path
          path_service_account = 'token.json'
          os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path_service_account    

          # Replace 'my-input-file-path' with your input file path
          input_file = 'gs://t-osprey-337221-yelp/.yelp-dataset/yelp_academic_dataset_review.json'

          # create publisher
          publisher = pubsub_v1.PublisherClient()
          topic_path = publisher.topic_path(gcp_project, pubsub_topic)

         # Reading gcs files with gcsfs
          gcs_file_system = gcsfs.GCSFileSystem(project=gcp_project)
          gcs_json_path = input_file
          with gcs_file_system.open(gcs_json_path) as f:
              for line in f:
                  event_data = line             # entire line of input CSV is the message
                  print(type(event_data))
                  print('Publishing {0} to {1}'.format(event_data, pubsub_topic))
                  publisher.publish(topic_path, event_data)
                  time.sleep(2)

The message start to publish:

![VM_topic_publish](https://user-images.githubusercontent.com/98153604/151245016-c429d90d-bfc4-4193-a02b-b1fc824e6743.JPG)

## 8. Launch Dataflow Pipeline

This pipeline will connect Pub/Sub Topic yelp_review, collect message data,  remove one 'text' column, or other simple transform or cleaning, and load message data into Bigquery in realtime.

Open other VM window, by click SSH in VM instance, and run comand line code:
      
      python3 yelp_dataflow_test.py
 
The code is:
      
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

The result show:

![run_dataflowfile](https://user-images.githubusercontent.com/98153604/151248463-2d76c7a8-f70c-4178-bacb-4c68d6641fea.JPG)

## 9. Check dataflow console and Bigquery

dataflow shows the pipeline:

![dataflow2](https://user-images.githubusercontent.com/98153604/151253854-a92aca66-2fe8-4f94-9f01-dcdaab42f06f.JPG)

Go to Bigquery, and we can see Bigquery table 'yelp-review-test' grandually increase its size, the rows increase with the message publish to the Pub/Sub Topic, we can you bigquery to analyze the data, like check all the reviews for one specific business, or all the reviews from one users.

![bigquery3](https://user-images.githubusercontent.com/98153604/151249239-1bdb9382-9743-4a71-8c2e-d5f518b09910.JPG)

## 10. Tableau connect Bigquery for visulization in real time

We can also connect Tableau, to do visulization in real time, we can updata the visulization when we fresh the data source:

![tableau](https://user-images.githubusercontent.com/98153604/151252777-7ef9bcb2-1075-44e0-ab75-113e15abed3c.JPG)

This tableau figure show the top 20 business with highest review numbers, and also show their average stars given by users, which reflect if this business has more costomers and
is it has a good service for customers.








   
   
   
   








 













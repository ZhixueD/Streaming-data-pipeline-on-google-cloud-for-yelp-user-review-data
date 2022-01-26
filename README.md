# Build a streaming data pipeline on google cloud by using Pub/Sub, dataflow, apache beam, Bigquery

![dataflow pipeline model](https://user-images.githubusercontent.com/98153604/151060089-9ffaa826-fed6-44a1-b84f-b0c508050805.png)

Streaming data pipelines, by extension, is a data pipeline architecture that handle millions of events at scale, in real time. That capability allows for applications, analytics, and reporting in real time. 

How do streaming data pipelines work? 
The first step in a streaming data pipeline is that the information enters the pipeline. Next, software decouples applications, which creates information from the applications using it. That allows for the development of low-latency streams of data (which can be transformed as necessary).'

What is Yelp used for?
With unmatched local business information, photos and review content, Yelp provides a one-stop local platform for consumers to discover, connect and transact with local businesses of all sizes by making it easy to request a quote, join a waitlist, and make a reservation, appointment or purchase.

In this project, I simulate yelp website which continuously collect million's user review on local businesses. Here, I write a python code which can simulate users continuously publish reviews to a Pub/Sub topic. And then, I write a apache beam (python) code to run a streaming dataflow pipeline, do some simple data cleaning and load it to Bigquery data warehouse in real time. Therefore, I can writen SQL code to analyze and report result in real time. And serching reviews for certain business in realtime. The whole streaming pipeline is runing on Google cloud platform.

The whole project include:

1. Install python packages using VM instance
2. Prepare data for publish in Google cloud storage
4. Create a Pub/Sub topic
5. Create and download the JSON key of your SA. On the Service Account page
6. Simulate users's review data and publish it the Pub/Sub topic
7. Create Bigquery dataset and table with data type
8. Start publish the review data to Pub/Sub
9. Launch Dataflow Pipeline

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













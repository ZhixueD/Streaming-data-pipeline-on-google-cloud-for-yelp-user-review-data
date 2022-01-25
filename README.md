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
2. Prepare data for publish
3. Create a Pub/Sub topic
4. Simulate users's review data and publish it the Pub/Sub topic
5. Create Bigquery dataset and table with data type
6. Launch Dataflow Pipeline









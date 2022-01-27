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
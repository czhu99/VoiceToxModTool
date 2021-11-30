import requests, argparse, os, csv, json
from googleapiclient import discovery
from googleapiclient.errors import HttpError
import pandas as pd
import time
from tqdm import tqdm
from dotenv import load_dotenv


# CONSTANTS
load_dotenv()
API_KEY = os.getenv('API_KEY')

LIMIT_BATCH = 998

# GLOBAL DATA STRUCTURE
api_responses = []

# Callback function for batched requests
# Used for collecting the results
def gather_results(request_id, response, exception):
    global scores
    api_responses.append((request_id, response))
    
    
# Read data
file = 'data/train-balanced-sarcasm.csv'
df = pd.read_csv(file)
total_rows = len(df)
print("Total rows = %d" % (total_rows))
df = df[0:3]

# Attributes to request from perspective API
attributes = ["TOXICITY", "SEVERE_TOXICITY", "IDENTITY_ATTACK", "INSULT",
              "PROFANITY", "THREAT", "SEXUALLY_EXPLICIT"]

service = discovery.build("commentanalyzer", 
                          "v1alpha1", 
                          developerKey=API_KEY, 
                          discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
                          static_discovery=False)

batch = service.new_batch_http_request(callback=gather_results)

count = 0
iteration = 0
comments = dict()

for index, row in df.iterrows():
    text = row['comment']
    analyze_request = {
      'comment': { 'text': text },
      'requestedAttributes': {attribute:{} for attribute in attributes}
    }
    batch.add(service.comments().analyze(body=analyze_request), request_id=str(index))
    comments[count] = text
    count += 1
    if (count >= LIMIT_BATCH):
        # Send requests in a bulk
        batch.execute()
        batch = service.new_batch_http_request(callback=gather_results)
        iteration += 1
        if (iteration % 10 == 0):
            num_processed = iteration * LIMIT_BATCH
            percentage_finished = num_processed / float(total_rows) * 100
            print("Processed %d / %d (%.2f percent)" % (num_processed, total_rows, percentage_finished) )
        count = 0

batch.execute()
print("Finish processing the data, write it down to file..")

# Flush data to dataframe
for response in api_responses:
    index = int(response[0])
    json_response = response[1]
    if (json_response != None):
        for attr in attributes:
            column_name = attr.lower() + "_probability"
            df.loc[index, column_name] = json_response['attributeScores'][attr]['summaryScore']['value']

file = 'data/train-balanced-sarcasm-perspective.csv'
df.to_csv(file, quoting=csv.QUOTE_NONNUMERIC)
print("Finish writing the data!")
df.head()
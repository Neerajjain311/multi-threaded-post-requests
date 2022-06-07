# Import necessary modules
import requests
import logging
import json
import time
from concurrent.futures import ThreadPoolExecutor
from models import Activity
import threading


# Global Variable to store unprocessed activity items - due to one of the errors 
queue = []


# Configure Logger
logging.basicConfig(filename='task_status.log', filemode='w', level=logging.INFO, 
        format='%(asctime)s - %(process)d - %(levelname)s - %(message)s')


# Read JSON data from given file (stored at file_path)
def read_json_input(file_path):
    try:
        logging.info("Fetching JSON data from %s", file_path)
        
        with open(file_path) as data_file:
            activities = json.load(data_file)
            return activities['activities']
    
    except FileNotFoundError as f:
        logging.error(f)


# HTTP POST Request
def http_post_request(url, json_load, activity_id) :
    try:
        response = requests.post(url, json=json_load)
        if response.status_code == 429:
            attempts = 0
            # Lets assume max allowed attempts = 10
            max_attempts = 10
        
            while attempts < max_attempts: 
                response = requests.post(url, json=json_load)
           
                # If rate limited, then wait and try again
                if response.status_code != 429:
                    break
                
                # Wait for a while before trying again
                time.sleep((2 ** attempts) + random.random())
                attempts = attempts + 1

        response.raise_for_status()

    except requests.exceptions.HTTPError as errh:
        logging.error("Activity Id : %s - %s - %s", activity_id, url, str(errh))
    except requests.exceptions.ConnectionError as errc:
        logging.error("Activity Id : %s - %s - %s", activity_id, url, str(errc))
    except requests.exceptions.Timeout as errt:
        logging.error("Activity Id : %s - %s - %s", activity_id, url, str(errt))
    finally:
        queue.append(activity_id + " | " + url + " | " + json_load)
       

# POST Requests using Multithreading - using and without using ThreadPoolExecutor
def parallel_http_post_request(urls, json_load, activity_id):
    
    threads = []

    # --------------- ThreadPoolExecutor doesn't allow Daemon threads, thus runs in sequential order
    # ----------------------------------------------------------------------------------------------    
    # with ThreadPoolExecutor(max_workers=30) as executor:
    #     for url in urls:
    #         threads.append(executor.submit(http_post_request, url, json_load, activity_id))
    # ----------------------------------------------------------------------------------------------

    # --------------- Tried to make threads Daemon, thus making them independent with no join() later
    for url in urls:
        t = threading.Thread(target=http_post_request, args=(url, json_load, activity_id), daemon= True)
        t.start() 
        threads.append(t)
    
    # --------------- Doesn't make sense to use thread.join(), as the resultant would be same as that of ThreadPoolExecutor
    
    # for thread in threads:
    #     thread.join()


# Main method
def main():
    
    # Assuming we received this data from a 'GET call' or a 'predefined function' or a 'kafka topic'
    sample_activities = read_json_input('sample_data.json')
    
    # List of Dummy URLs
    urls = [
        "https://www.server_1.com/python/",
        "https://www.server_2.com/python/",
        "https://www.server_3.com/python/",
        "https://www.server_4.com/python/",
        "https://www.server_5.com/python/",
        ]

    # Process activities - if sample_activities is not empty
    if sample_activities is not None:
        
        for activity in sample_activities:
            logging.info("Processing Activity Id : %s", activity['activity_id'])
            
            try:
                activity_obj = Activity(**activity['activity_info'])
                json_load = json.dumps(activity_obj.__dict__)
                parallel_http_post_request(urls, json_load, activity['activity_id'])
            
            except AssertionError as e:
                logging.error("Activity Id : %s - %s - !!Terminating Processing for this Activity ID!!", activity['activity_id'], str(e))
            
    # Sleep reqd to showcase daemon tasks in actions        
    time.sleep(5)
    # Pending/Unsuccessful Items
    # print('Requests in queue : ' + str(len(queue)))
    
    # Verify Queue -- this queue can be parsed later and can be used to reload the data once the errors/issues are resolved
    #print(queue[0])


# For calling main 
if __name__ == '__main__':
    main()



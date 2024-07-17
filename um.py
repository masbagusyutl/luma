import requests
import json
import time
import datetime

def read_data(file_name):
    with open(file_name, 'r') as file:
        return file.readlines()

def send_request(init_data):
    url = "https://bot.lumacoin.org/api/"
    payload = {
        "action": "get_coins",
        "initData": init_data.strip()
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    return response.status_code, response.text

def countdown(minutes):
    total_seconds = minutes * 60
    while total_seconds > 0:
        mins, secs = divmod(total_seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(f"Countdown: {timeformat}", end='\r')
        time.sleep(1)
        total_seconds -= 1

def main():
    init_data_list = read_data('data.txt')
    total_accounts = len(init_data_list)
    print(f"Total accounts: {total_accounts}")

    for i, init_data in enumerate(init_data_list):
        print(f"Processing account {i+1}/{total_accounts}")
        status_code, response_text = send_request(init_data)
        print(f"Status Code: {status_code}, Response: {response_text}")
        time.sleep(5)

    print("All accounts processed. Starting 15-minute countdown...")
    countdown(15)
    print("Restarting process...")
    main()

if __name__ == "__main__":
    main()

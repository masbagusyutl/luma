import requests
import json
import time
import re

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
    return response.status_code, response.json()

def extract_username(init_data):
    match = re.search(r'username%22%3A%22(.*?)%22', init_data)
    return match.group(1) if match else None

def countdown(minutes):
    total_seconds = minutes * 60
    while total_seconds > 0:
        mins, secs = divmod(total_seconds, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(f"Countdown: {timeformat}", end='\r')
        time.sleep(1)
        total_seconds -= 1
    print()

def main():
    init_data_list = read_data('data.txt')
    total_accounts = len(init_data_list)
    print(f"Total accounts: {total_accounts}")

    for i, init_data in enumerate(init_data_list):
        username = extract_username(init_data)
        print(f"Processing account {i+1}/{total_accounts} ({username})")
        status_code, response_json = send_request(init_data)
        
        if status_code == 200:
            # Display key info from the response
            keys_to_display = ['some_key1', 'some_key2']  # replace with actual keys you want to display
            display_info = {key: response_json.get(key, 'N/A') for key in keys_to_display}
            display_info_text = ', '.join([f"{key}: {value}" for key, value in display_info.items()])
            print(f"Successful claim on Username: {username}. {display_info_text}")
        else:
            print(f"Failed to process account {username}. Status Code: {status_code}")

        time.sleep(5)

    print("All accounts processed. Starting 15-minute countdown...")
    countdown(15)
    print("Restarting process...")
    main()

if __name__ == "__main__":
    main()

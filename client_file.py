import os
import time
import csv
import sys
from client import InventoryClient

def main(input_path, sleep_time_ms):
    server_url = os.getenv("SERVER_URL", "http://server:5000")
    client = InventoryClient(server_url)
    if os.path.isfile(input_path) and input_path.endswith('.csv'):
        process_file(client, input_path, sleep_time_ms)
    elif os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.endswith('.csv'):
                input_file_path = os.path.join(input_path, filename)
                process_file(client, input_file_path, sleep_time_ms)
    else:
        print(f"Error: The path '{input_path}' is not a valid CSV file or directory.")

def process_file(client, input_file_path, sleep_time_ms):
    print(f"Processing file: {input_file_path}")

    with open(input_file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            api_name = row[0]
            parameters = row[1:]

            try:
                if api_name == "define_stuff":
                    output = client.define_stuff(parameters[0], parameters[1])
                elif api_name == "undefine":
                    output = client.undefine(parameters[0])
                elif api_name == "add":
                    output = client.add(int(parameters[0]), parameters[1])
                elif api_name == "remove":
                    output = client.remove(int(parameters[0]), parameters[1])
                elif api_name == "get_count":
                    output = client.get_count(parameters[0])
                elif api_name == "save_data":
                    output = client.save_data()
                elif api_name == "load_data":
                    output = client.load_data(parameters[0])
                elif api_name == "delete_data":
                    output = client.delete_data(parameters[0])
                else:
                    print(f"Unknown API name: {api_name}")
                    continue

                print(f"R1-LOG:{api_name},OUTPUT:{output}")

            except Exception as e:
                print(f"Error processing {api_name} with parameters {parameters}: {e}")

    
            time.sleep(sleep_time_ms / 1000.0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python client_file.py <input_path> <sleep_time_ms>")
        sys.exit(1)

    input_path = sys.argv[1]
    sleep_time_ms = int(sys.argv[2])
    main(input_path, sleep_time_ms)

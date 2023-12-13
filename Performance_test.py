from MRTD import *
import json
import time
import csv


def test_performance(decode_func, encode_func, json_file, csv_filename):
    with open(json_file) as file:
        data = json.load(file)

    # Use 'records_encoded' as the key if the file contains encoded records
    key_name = 'records_encoded' if 'records_encoded' in data else 'records_decoded'

    header = ['# of lines read', 'Execution time w/o tests', 'Execution time w/ tests']
    value = []

    for k in range(100, 10001, 1000):
        subset_data = {key_name: data[key_name][:k]}  # Assuming each item in the list is a dictionary

        # Measure execution time without tests
        start = time.perf_counter()
        decode_func(subset_data[key_name])
        end = time.perf_counter()
        no_test_time = end - start

        # Measure execution time with tests
        start = time.perf_counter()
        encode_func(subset_data)
        end = time.perf_counter()
        with_test_time = end - start

        value.append([k, no_test_time, with_test_time])

    # Write to CSV
    with open(csv_filename, 'w', encoding='UTF8') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(value)


# Example usage for decoding performance
test_performance(decode_mrz_recs, encode_mrz_recs, "records_encoded.json", "performance_encoded.csv")

# Example usage for decoding performance
test_performance(decode_mrz_recs, encode_mrz_recs, "records_decoded.json", "performance_decoded.csv")




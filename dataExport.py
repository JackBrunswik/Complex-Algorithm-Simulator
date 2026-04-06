import csv
from datetime import datetime

def export_csv(data, headers, filename_prefix):
    filename = f"{filename_prefix}_{timestamp()}.csv"

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(data)

    return filename

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")
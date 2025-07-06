import os
import csv
import logging
import pydicom
from PIL import Image
import numpy as np
from typing import Optional, List, Tuple

class FileProcessor:
    def __init__(self, base_path: str, log_file: str):
        self.base_path = base_path
        logging.basicConfig(filename=log_file, level=logging.ERROR)
        self.logger = logging.getLogger(__name__)

    def list_folder_contents(self, folder_name: str, details: bool = False):
        path = os.path.join(self.base_path, folder_name)
        try:
            items = os.listdir(path)
            print(f"Folder: {path}")
            print(f"Number of elements: {len(items)}")
            files = []
            folders = []
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isfile(full_path):
                    size = os.path.getsize(full_path) / (1024 * 1024)
                    mod_time = os.path.getmtime(full_path)
                    files.append((item, size, mod_time))
                else:
                    mod_time = os.path.getmtime(full_path)
                    folders.append((item, mod_time))
            print("Files:")
            for f in files:
                if details:
                    print(f" - {f[0]} ({f[1]:.2f} MB, Last Modified: {f[2]})")
                else:
                    print(f" - {f[0]}")
            print("Folders:")
            for d in folders:
                print(f" - {d[0]} (Last Modified: {d[1]})")
        except FileNotFoundError:
            self.logger.error(f"Folder {folder_name} does not exist.")

    def read_csv(self, filename: str, report_path: Optional[str] = None, summary: bool = False):
        path = os.path.join(self.base_path, filename)
        try:
            with open(path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                rows = list(reader)
                num_rows = len(rows)
                columns = reader.fieldnames
                numeric_stats = {}
                non_numeric_summary = {}

                for col in columns:
                    values = [row[col] for row in rows]
                    try:
                        numeric_values = [float(v) for v in values]
                        avg = sum(numeric_values) / num_rows
                        std_dev = (sum((x - avg)**2 for x in numeric_values) / num_rows)**0.5
                        numeric_stats[col] = {"avg": avg, "std_dev": std_dev}
                    except ValueError:
                        unique_vals = {}
                        for val in values:
                            unique_vals[val] = unique_vals.get(val, 0) + 1
                        non_numeric_summary[col] = unique_vals

                print(f"Columns: {columns}")
                print(f"Rows: {num_rows}")
                print("Numeric Columns:")
                for col, stats in numeric_stats.items():
                    print(f" - {col}: Average = {stats['avg']:.2f}, Std Dev = {stats['std_dev']:.2f}")

                if summary:
                    print("Non-Numeric Summary:")
                    for col, counts in non_numeric_summary.items():
                        print(f" - {col}: Unique Values = {len(counts)}")

                if report_path:
                    with open(os.path.join(report_path, "report.txt"), 'w') as f:
                        for col, stats in numeric_stats.items():
                            f.write(f"{col}: Avg={stats['avg']}, StdDev={stats['std_dev']}\n")
                        print(f"Saved summary report to {report_path}")
        except Exception as e:
            self.logger.error(f"Error reading CSV: {str(e)}")

    def read_dicom(self, filename: str, tags: Optional[List[Tuple[int, int]]] = None, extract_image: bool = False):
        path = os.path.join(self.base_path, filename)
        try:
            ds = pydicom.dcmread(path)
            print(f"Patient Name: {ds.PatientName}")
            print(f"Study Date: {ds.StudyDate}")
            print(f"Modality: {ds.Modality}")

            if tags:
                for tag in tags:
                    value = ds[tag].value
                    print(f"Tag {tag}: {value}")

            if extract_image:
                pixel_array = ds.pixel_array
                image = Image.fromarray(pixel_array)
                image.save(os.path.join(self.base_path, filename.replace(".dcm", ".png")))
                print(f"Extracted image saved to {filename.replace('.dcm', '.png')}")
        except Exception as e:
            self.logger.error(f"Error reading DICOM: {str(e)}")

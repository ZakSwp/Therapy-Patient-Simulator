import os
import csv
import json
import traceback
from datetime import datetime
import ast
import logging
from pathlib import Path

def log_usage(user, n): #Method for logging API usage
    file_exists = os.path.isfile("usageStats.csv")  
    with open("usageStats.csv", mode='a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['datetime', 'user', 'token_count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            'datetime': datetime.now().isoformat(),
            'user': user,
            'token_count': n
        })
def log_crash(data: dict, filepath: str = "CrashLog"): #Method for logging crashlogs
    """
    Logs crash information to a text file, appending to existing logs.
    Args:
        error_data (dict): Dictionary containing error information
        filepath (str): Path of the log file (default: "CrashLog.text")
    """
    try:
        # Convert to basic Python types
        simplified = {
            'timestamp': datetime.now().isoformat(),
            'model_version': data.get('model_version'),
            'usage_metadata': {
                'total_token_count': data.get('usage_metadata').total_token_count if hasattr(data.get('usage_metadata'), 'total_token_count') else None,
                'prompt_token_count': data.get('usage_metadata').prompt_token_count if hasattr(data.get('usage_metadata'), 'prompt_token_count') else None,
                'candidates_token_count': data.get('usage_metadata').candidates_token_count if hasattr(data.get('usage_metadata'), 'candidates_token_count') else None
            },
            'response_text': data['candidates'][0].content.parts[0].text if data.get('candidates') else None,
            'finish_reason': str(data['candidates'][0].finish_reason) if data.get('candidates') else None
        }
        filepath = filepath + str(datetime.now())
        with open(filepath, 'w') as f:
            json.dump(simplified, f, indent=2)
            
    except Exception as e:
        print(f"Failed to write crash log: {str(e)}")
        # Fallback to string representation
        with open(filepath + ".txt", 'w') as f:
            f.write(str(data))

def load_dict(filepath: str):
    loaded_data = {}
    with open(filepath, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) >= 2:  # Ensure row has key + value
                loaded_data[row[0]] = row[1]
    return(loaded_data)

def save_dict(filepath:str, data):
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for key, value in data.items():
            writer.writerow([key, value])

def get_session_number(session_text: str):
    # Split into lines and look for "session X" pattern
    first_line = session_text.strip().split('\n')[0]
    import re
    match = re.search(r'session\s+(\d+)', first_line, re.IGNORECASE)
    if match:
        return int(match.group(1))
    return None

def string_to_dict(string: str):
    dict_string = string.split("Chain Of Thoughts")[0].strip()
    try:
        parsed_dict = ast.literal_eval(dict_string)
        for key in ['Control', 'Self-Efficacy', 'Awareness', 'Recall', 'Cooperation Level']:
            parsed_dict[key] = float(parsed_dict[key])
        return(parsed_dict)
    except:
        print(f"Error parsing dict from:\n{dict_string}")



def copy_file_contents(source_path, destination_path):
    try:
        with open(source_path, 'r', encoding='utf-8') as src:
            content = src.read()

        with open(destination_path, 'w', encoding='utf-8') as dest:
            dest.write(content)

        #print(f"Contents copied from '{source_path}' to '{destination_path}' successfully.")
    except FileNotFoundError:
        print(f"Error: The file '{source_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def reset_patient_state(patient_name: str):
    last = f"Summaries/Backups/{patient_name}Last_Backup.txt"
    globl = f"Summaries/Backups/{patient_name}Global_Backup.txt"
    model = f"Summaries/Backups/{patient_name}Model_Backup.csv"

    lastDest = f"Summaries/{patient_name}Last.txt"
    globlDest = f"Summaries/{patient_name}Global.txt"
    modelDest = f"Persona/{patient_name}Model.csv"

    copy_file_contents(last,lastDest )
    copy_file_contents(globl,globlDest )
    copy_file_contents(model,modelDest )
    print("Patient state reset.\n")

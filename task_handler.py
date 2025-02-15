import os
import subprocess
import json
import re
from datetime import datetime
from collections import Counter
import sqlite3
from llm_utils import extract_email, extract_credit_card, find_similar_comments

def execute_task(task_desc):
    # Mapping task descriptions to functions
    if "install uv" in task_desc and "datagen.py" in task_desc:
        return run_datagen()
    elif "format" in task_desc.lower():
        return format_markdown()
    elif  "wednesdays" in task_desc.lower():
        return count_wednesdays()
    elif "contacts" in task_desc.lower():
        return sort_contacts()
    elif "logs-recent" in task_desc:
        return process_logs()
    elif "docs" in task_desc.lower():
        return index_markdown()
    elif "email" in task_desc.lower():
        return extract_sender_email()
    elif "credit card" in task_desc.lower():
        return extract_credit_card_number()
    elif "comments" in task_desc.lower():
        return find_similar_comments()
    elif "tickets" in task_desc.lower():
        return calculate_ticket_sales()
    else:
        raise ValueError("Unknown task description")

def run_datagen():
    subprocess.run(["uv", "--version"], check=False)  # Install uv if needed
    subprocess.run(["python", "-m", "pip", "install", "uv"], check=False)
    subprocess.run(["python", "datagen.py", "user@example.com"])
    return "Data generation completed."

def format_markdown():
    subprocess.run(["npx", "prettier@3.4.2", "--write", "/data/format.md"], check=True)
    return "Markdown file formatted."

def count_wednesdays():
    count = 0
    with open("./data/dates.txt", "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  # Skip empty lines
            
            # Possible date formats in your file
            date_formats = [
                "%Y/%m/%d %H:%M:%S",  # 2014/10/29 18:44:24
                "%Y-%m-%d",           # 2002-04-27
                "%b %d, %Y",          # Oct 31, 2002
                "%d-%b-%Y",           # 09-Oct-2022
                "%d-%b-%Y",           # 16-Sep-2019
                "%Y/%m/%d",           # 2010/02/24
            ]
            
            # Try parsing the date with multiple formats
            for fmt in date_formats:
                try:
                    date_obj = datetime.strptime(line, fmt)
                    if date_obj.weekday() == 2:  # Wednesday = 2
                        count += 1
                    break  # Exit loop once successfully parsed
                except ValueError:
                    continue  # Try next format
        
    # Save the count to a file
    with open("./data/dates-wednesdays.txt", "w") as f:
        f.write(str(count))

    return "Wednesdays counted"

def sort_contacts():
    with open("./data/contacts.json", "r") as f:
        contacts = json.load(f)
    contacts.sort(key=lambda c: (c["last_name"], c["first_name"]))
    with open("./data/contacts-sorted.json", "w") as f:
        json.dump(contacts, f, indent=4)
    return "Contacts sorted."

def process_logs():
    logs = sorted(os.listdir("./data/logs"), key=lambda f: os.path.getmtime(f"/data/logs/{f}"), reverse=True)
    logs = [f for f in logs if f.endswith(".log")][:10]

    with open("./data/logs-recent.txt", "w") as out_file:
        for log in logs:
            with open(f"./data/logs/{log}", "r") as f:
                first_line = f.readline().strip()
                out_file.write(first_line + "\n")

    return "Recent log lines extracted."

def index_markdown():
    index = {}
    for root, _, files in os.walk("./data/docs"):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), "r") as f:
                    for line in f:
                        if line.startswith("# "):
                            index[file] = line.strip("# ").strip()
                            break

    with open("./data/docs/index.json", "w") as f:
        json.dump(index, f, indent=4)
    return "Markdown files indexed."

def extract_sender_email():
    with open("./data/email.txt", "r") as f:
        email_text = f.read()
    sender_email = extract_email(email_text)
    with open("./data/email-sender.txt", "w") as f:
        f.write(sender_email)
    return "Sender email extracted."

def extract_credit_card_number():
    card_number = extract_credit_card("./data/credit_card.png")
    with open("./data/credit-card.txt", "w") as f:
        f.write(card_number)
    return "Credit card number extracted."

def calculate_ticket_sales():
    conn = sqlite3.connect("./data/ticket-sales.db")
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(units * price) FROM tickets WHERE type = 'Gold'")
    total_sales = cursor.fetchone()[0] or 0
    with open("./data/ticket-sales-gold.txt", "w") as f:
        f.write(str(total_sales))
    conn.close()
    return "Total ticket sales calculated."

import re
import io
import pandas as pd
from datetime import datetime

def parse_chat(file_path_or_buffer):
    
    # Updated pattern to capture:
    #  - Date: one or two digits for day and month, and two or four digits for the year.
    #  - Time: HH:MM (optionally with :SS)
    #  - AM/PM (optional, e.g., "pm")
    #  - Sender (optional; if missing, it's treated as a system message)
    #  - Message

    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s+(\d{1,2}:\d{2}(?::\d{2})?)\s*([apAP][mM])?\s*-\s*(?:(.*?):\s)?(.*)$'
    data = []

    if isinstance(file_path_or_buffer, str):
        f = open(file_path_or_buffer, encoding="utf-8")
    else:
        if hasattr(file_path_or_buffer, "getvalue"):
            text = file_path_or_buffer.getvalue().decode("utf-8")
            f = io.StringIO(text)
        else:
            f = file_path_or_buffer

    with f as file:
        for line in file:
            line = line.strip()
            match = re.match(pattern, line)
            if match:
                date_str = match.group(1)            # e.g., "10/12/22"
                time_str = match.group(2)            # e.g., "8:56" (or "8:56:30")
                ampm = match.group(3) or ""          # e.g., "pm" (if present)
                sender = match.group(4) or "System"  # If no sender is provided, treat as system message.
                message = match.group(5).strip()     # The rest of the message

                dt_str = f"{date_str} {time_str} {ampm}".strip()
                dt = None

                date_formats = []
                if len(date_str.split('/')[-1]) == 2:
                    if ampm:
                        date_formats.append("%d/%m/%y %I:%M %p")
                        date_formats.append("%d/%m/%y %I:%M:%S %p")
                    else:
                        date_formats.append("%d/%m/%y %H:%M")
                        date_formats.append("%d/%m/%y %H:%M:%S")
                else:
                    if ampm:
                        date_formats.append("%d/%m/%Y %I:%M %p")
                        date_formats.append("%d/%m/%Y %I:%M:%S %p")
                    else:
                        date_formats.append("%d/%m/%Y %H:%M")
                        date_formats.append("%d/%m/%Y %H:%M:%S")

                for fmt in date_formats:
                    try:
                        dt = datetime.strptime(dt_str, fmt)
                        break
                    except ValueError:
                        continue

                data.append({
                    "datetime": dt,
                    "sender": sender,
                    "message": message
                })

    df = pd.DataFrame(data)
    if "datetime" in df.columns:
        df.dropna(subset=["datetime"], inplace=True)
    return df

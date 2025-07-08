import re
import json

def parse_month_to_number(month_name_ru):
    """Converts Russian month name to month number."""
    months = {
        "января": "01", "февраля": "02", "марта": "03", "апреля": "04",
        "мая": "05", "июня": "06", "июля": "07", "августа": "08",
        "сентября": "09", "октября": "10", "ноября": "11", "декабря": "12"
    }
    return months.get(month_name_ru.lower())

def extract_protocol_data(filepath="ano_governance/Protocol_Founding_Meeting.md"):
    """
    Parses the protocol Markdown file to extract specific information.
    Scope: Meeting date, location, first attendee, and first decision.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return {"error": f"File not found: {filepath}"}

    data = {
        "source_document": filepath,
        "meeting_info": {},
        "attendees": [],
        "decisions": []
    }

    # 1. Extract Meeting Date and Location
    # Looking for section "1. Время и место проведения собрания"
    section1_match = re.search(r"##\s*1\.\s*Время и место проведения собрания\s*([\s\S]*?)(?=\n##\s*\d+\.|\Z)", content)
    if section1_match:
        section1_content = section1_match.group(1)

        date_match = re.search(r"Дата проведения:\s*\"(\d{2})\"\s*([а-яА-Я]+)\s*(\d{4})\s*г\.", section1_content)
        if date_match:
            day, month_ru, year = date_match.groups()
            month_num = parse_month_to_number(month_ru)
            if month_num:
                data["meeting_info"]["date"] = f"{year}-{month_num}-{day}"
            else:
                data["meeting_info"]["date_raw"] = date_match.group(0) # Store raw if parsing failed

        location_match = re.search(r"Место проведения:\s*(.+)", section1_content)
        if location_match:
            data["meeting_info"]["location"] = location_match.group(1).strip()

    # 2. Extract First Attendee
    # Looking for section "2. Присутствовали"
    section2_match = re.search(r"##\s*2\.\s*Присутствовали\s*([\s\S]*?)(?=\n##\s*\d+\.|\Z)", content)
    if section2_match:
        section2_content = section2_match.group(1)
        attendee_match = re.search(r"-\s*([А-ЯЁ][а-яёА-ЯЁ\s]+?)\s*\(паспорт:", section2_content) # Get name before passport
        if attendee_match:
            data["attendees"].append({"name": attendee_match.group(1).strip()})

    # 3. Extract First Decision (related to the first agenda item)
    # Looking for section "4. По вопросам повестки дня принято следующее"
    # Then specifically "4.1. По первому вопросу"
    section4_1_match = re.search(r"###\s*4\.1\.\s*По первому вопросу\s*([\s\S]*?)(?=\n###\s*4\.\d+\.|\Z)", content)
    if section4_1_match:
        section4_1_content = section4_1_match.group(1)
        decision_text_match = re.search(r"\*\*Решили:\*\*\s*([\s\S]+)", section4_1_content)
        if decision_text_match:
            decision_text = decision_text_match.group(1).strip().replace('\n', ' ') # Clean up
            data["decisions"].append({
                "agenda_item_reference": "1", # Hardcoded for "По первому вопросу"
                "decision_text": decision_text
            })

    return data

if __name__ == "__main__":
    extracted_data = extract_protocol_data()
    print(json.dumps(extracted_data, ensure_ascii=False, indent=2))

    # Example for a different file if needed for testing
    # extracted_data_test = extract_protocol_data("path/to/your/test_protocol.md")
    # print(json.dumps(extracted_data_test, ensure_ascii=False, indent=2))

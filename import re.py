import re

def normalise_phone(raw_phone):
    if not raw_phone:
        return ""
    digits = re.sub(r"\D", "", raw_phone)
    return digits[-10:] if len(digits) >= 10 else digits

def normalise_name(raw_name):
    if not raw_name:
        return "Unknown"
    cleaned = re.sub(r"^(dr|mr|mrs|ms)\.?\s+", "", raw_name.strip(), flags=re.IGNORECASE)
    return cleaned.strip().title()

def merge_contacts(sources):
    merged = {}
    for source in sources:
        for entry in source:
            norm_num = normalise_phone(entry.get("phone", ""))
            if not norm_num:
                continue

            name = normalise_name(entry.get("name", ""))
            email = entry.get("email", "").strip().lower()

            if norm_num not in merged:
                merged[norm_num] = {
                    "name": name,
                    "phones": set(),
                    "emails": set()
                }
            elif len(name) > len(merged[norm_num]["name"]) and name != "Unknown":
                merged[norm_num]["name"] = name

            merged[norm_num]["phones"].add(entry["phone"].strip())
            if email:
                merged[norm_num]["emails"].add(email)

    return list(merged.values())

# Verification test
phone1 = [{"name": "Dr. Ravi", "phone": "+91 98400 12345", "email": "ravi@work.com"}]
sim = [{"name": "ravi kumar", "phone": "9840012345", "email": "ravi.k@gmail.com"}]
print(merge_contacts([phone1, sim]))
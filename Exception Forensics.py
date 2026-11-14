import os
import csv


class InvalidRegistrationError(Exception):
  """Raised when a registration line is malformed or invalid."""
  pass


class DuplicateRecordError(Exception):
  """Raised when a register number appears more than once."""
  pass


def validate_email(email):
  """Validates email format using string methods."""
  email = email.strip()
  if email.count("@") != 1:
    return False
  user, domain = email.split("@")
  if not user or not domain or "." not in domain:
    return False
  if domain.startswith(".") or domain.endswith(".") or " " in email:
    return False
  return True


def parse_registration(line):
  """Parses and validates a single fest registration line."""
  parts = [p.strip() for p in line.strip().split(",")]
  if len(parts) < 5:
    raise InvalidRegistrationError(f"Expected at least 5 fields, found {len(parts)}")

  reg_no, name, dept, email, events_raw = parts[:5]

  if not reg_no or not name:
    raise InvalidRegistrationError("Register number or name cannot be empty")

  if not validate_email(email):
    raise InvalidRegistrationError(f"Invalid email format: '{email}'")

  events = [e.strip() for e in events_raw.split(";") if e.strip()]
  if not events:
    raise InvalidRegistrationError("At least one event must be chosen")

  return {"reg": reg_no, "name": name, "dept": dept, "email": email, "events": events}


def process_fest_desk(file_paths, output_dir="fest_output"):
  os.makedirs(output_dir, exist_ok=True)
  seen_regs = set()
  master_records = []
  error_logs = []
  event_participants = {}
  total_processed = 0

  for path in file_paths:
    if not os.path.exists(path):
      error_logs.append((path, 0, "N/A", "Department file not found"))
      continue

    try:
      with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
          if not line.strip():
            continue
          total_processed += 1
          try:
            record = parse_registration(line)
            if record["reg"] in seen_regs:
              raise DuplicateRecordError(f"Duplicate reg number '{record['reg']}'")

            seen_regs.add(record["reg"])
            master_records.append(record)

            for event in record["events"]:
              event_participants.setdefault(event, []).append(record)

          except (InvalidRegistrationError, DuplicateRecordError) as e:
            error_logs.append((path, line_no, line.strip(), str(e)))

    except PermissionError:
      error_logs.append((path, 0, "N/A", "Permission denied"))

  # 1. Write Master List CSV
  with open(os.path.join(output_dir, "master_registrations.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Register Number", "Name", "Department", "Email", "Events"])
    for r in master_records:
      writer.writerow([r["reg"], r["name"], r["dept"], r["email"], ";".join(r["events"])])

  # 2. Write Event-wise Participant Lists
  for event, participants in event_participants.items():
    with open(os.path.join(output_dir, f"event_{event}.csv"), "w", newline="", encoding="utf-8") as f:
      writer = csv.writer(f)
      writer.writerow(["Register Number", "Name", "Department", "Email"])
      for p in participants:
        writer.writerow([p["reg"], p["name"], p["dept"], p["email"]])

  # 3. Write Error Audit Log
  with open(os.path.join(output_dir, "error_audit.log"), "w", encoding="utf-8") as f:
    for err in error_logs:
      f.write(f"File: {err[0]} | Line: {err[1]} | Content: {err[2]} | Error: {err[3]}\n")

  # 4. Write Summary Report
  with open(os.path.join(output_dir, "fest_summary.txt"), "w", encoding="utf-8") as f:
    f.write("=== College Fest Registration Summary ===\n")
    f.write(f"Total Lines Processed: {total_processed}\n")
    f.write(f"Valid Unique Registrations: {len(master_records)}\n")
    f.write(f"Errors & Duplicates Logged: {len(error_logs)}\n")
    f.write(f"Total Events Hosted: {len(event_participants)}\n")

  print(f"[Success] Fest processing complete. Outputs written to '{output_dir}/'.")


if __name__ == "__main__":
  # Quick test execution
  dept_file = "dept_cse.txt"
  sample_data = (
      "192311001, Aarav Kumar, CSE, aarav@college.edu, Coding;Quiz\n"
      "192311002, Priya Sharma, ECE, priya@college.edu, Robotics\n"
      "192311001, Aarav Kumar, CSE, aarav@college.edu, Coding\n"  # Duplicate
      "192311003, Rahul, MECH, invalid-email, Quiz\n"  # Bad email
  )
  with open(dept_file, "w", encoding="utf-8") as f:
    f.write(sample_data)

  process_fest_desk([dept_file])
  
  if os.path.exists(dept_file):
    os.remove(dept_file)
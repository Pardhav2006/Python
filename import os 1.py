import os
import csv


class InvalidRecordError(Exception):
  """Raised when a registration line is malformed or invalid."""

  pass


class DuplicateRecordError(Exception):
  """Raised when a register number has already been processed."""

  pass


def validate_email(email):
  """Validates email using string methods."""
  email = email.strip()
  if email.count("@") != 1:
    return False
  user_part, domain_part = email.split("@")
  if not user_part or not domain_part:
    return False
  if "." not in domain_part or domain_part.startswith(".") or domain_part.endswith("."):
    return False
  if " " in email:
    return False
  return True


def parse_registration_line(line):
  """Parses and validates a single registration line."""
  parts = [p.strip() for p in line.strip().split(",")]
  if len(parts) < 5:
    raise InvalidRecordError(f"Expected at least 5 fields, found {len(parts)}")

  reg_no, name, dept, email, events_raw = parts[:5]

  if not reg_no or not name:
    raise InvalidRecordError("Register number or name cannot be empty")

  if not validate_email(email):
    raise InvalidRecordError(f"Invalid email format: '{email}'")

  events = [e.strip() for e in events_raw.split(";") if e.strip()]
  if not events:
    raise InvalidRecordError("At least one event must be chosen")

  return {"reg": reg_no, "name": name, "dept": dept, "email": email, "events": events}


def process_fest_registrations(file_paths, output_dir="output"):
  os.makedirs(output_dir, exist_ok=True)
  seen_regs = set()
  master_records = []
  error_logs = []
  event_participants = {}

  total_lines_processed = 0

  for file_path in file_paths:
    if not os.path.exists(file_path):
      error_logs.append((file_path, 0, "N/A", "File not found"))
      continue

    try:
      with open(file_path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
          if not line.strip():
            continue
          total_lines_processed += 1
          try:
            record = parse_registration_line(line)
            if record["reg"] in seen_regs:
              raise DuplicateRecordError(f"Duplicate reg number {record['reg']}")

            seen_regs.add(record["reg"])
            master_records.append(record)

            for event in record["events"]:
              event_participants.setdefault(event, []).append(record)

          except (InvalidRecordError, DuplicateRecordError) as e:
            error_logs.append((file_path, line_no, line.strip(), str(e)))

    except PermissionError:
      error_logs.append((file_path, 0, "N/A", "Permission denied"))

  # Write Master Clean List
  master_csv_path = os.path.join(output_dir, "master_registrations.csv")
  with open(master_csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Register Number", "Name", "Department", "Email", "Events"])
    for r in master_records:
      writer.writerow([r["reg"], r["name"], r["dept"], r["email"], ";".join(r["events"])])

  # Write Event-wise Files
  for event, participants in event_participants.items():
    event_file_path = os.path.join(output_dir, f"event_{event}.csv")
    with open(event_file_path, "w", newline="", encoding="utf-8") as f:
      writer = csv.writer(f)
      writer.writerow(["Register Number", "Name", "Department", "Email"])
      for p in participants:
        writer.writerow([p["reg"], p["name"], p["dept"], p["email"]])

  # Write Error Log
  error_log_path = os.path.join(output_dir, "error_audit.log")
  with open(error_log_path, "w", encoding="utf-8") as f:
    for err in error_logs:
      f.write(f"File: {err[0]} | Line: {err[1]} | Content: {err[2]} | Error: {err[3]}\n")

  # Write Summary Report
  summary_path = os.path.join(output_dir, "fest_summary.txt")
  with open(summary_path, "w", encoding="utf-8") as f:
    f.write("=== College Fest Registration Summary Report ===\n")
    f.write(f"Total Lines Processed: {total_lines_processed}\n")
    f.write(f"Valid Unique Registrations: {len(master_records)}\n")
    f.write(f"Errors & Duplicates Logged: {len(error_logs)}\n")
    f.write(f"Total Events Hosted: {len(event_participants)}\n")

  print(f"[Success] Processing complete. Check output directory: {output_dir}")


if __name__ == "__main__":
  # Example test run with mock department file
  sample_data = (
      "192311001, Alice Smith, CSE, alice@college.edu, Coding;Quiz\n"
      "192311002, Bob Jones, ECE, bob.jones@college.edu, Robotics\n"
      "192311001, Alice Smith, CSE, alice@college.edu, Coding\n"  # Duplicate
      "192311003, Charlie, MECH, invalid-email, Quiz\n"  # Bad email
      "192311004, Diana, EEE, diana@college.edu\n"  # Missing events
  )
  test_file = "dept_cse.txt"
  with open(test_file, "w", encoding="utf-8") as f:
    f.write(sample_data)

  process_fest_registrations([test_file])
  if os.path.exists(test_file):
    os.remove(test_file)
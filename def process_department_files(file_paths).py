import csv
import os


class InvalidRecordError(Exception):
  """Raised when a registration record is malformed or invalid."""

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


def validate_and_parse(line):
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


def write_outputs(master_records, event_dict, error_log, output_dir="output"):
  """Writes master records, event files, and error logs to disk."""
  os.makedirs(output_dir, exist_ok=True)

  # 1. Master CSV
  with open(
      os.path.join(output_dir, "master_registrations.csv"),
      "w",
      newline="",
      encoding="utf-8",
  ) as f:
    writer = csv.writer(f)
    writer.writerow(["Register Number", "Name", "Department", "Email", "Events"])
    for r in master_records:
      writer.writerow(
          [r["reg"], r["name"], r["dept"], r["email"], ";".join(r["events"])]
      )

  # 2. Event CSVs
  for event, participants in event_dict.items():
    with open(
        os.path.join(output_dir, f"event_{event}.csv"),
        "w",
        newline="",
        encoding="utf-8",
    ) as f:
      writer = csv.writer(f)
      writer.writerow(["Register Number", "Name", "Department", "Email"])
      for p in participants:
        writer.writerow([p["reg"], p["name"], p["dept"], p["email"]])

  # 3. Error Audit Log
  with open(
      os.path.join(output_dir, "error_audit.log"), "w", encoding="utf-8"
  ) as f:
    for err in error_log:
      f.write(
          f"File: {err[0]} | Line: {err[1]} | Content: {err[2]} | Error:"
          f" {err[3]}\n"
      )


def process_department_files(file_paths):
  seen_regs = set()
  master_records = []
  error_log = []
  event_dict = {}

  for path in file_paths:
    try:
      with open(path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
          if not line.strip():
            continue
          try:
            record = validate_and_parse(line)
            if record["reg"] in seen_regs:
              raise DuplicateRecordError("Duplicate register number")
            seen_regs.add(record["reg"])
            master_records.append(record)
            for event in record["events"]:
              event_dict.setdefault(event, []).append(record)
          except (InvalidRecordError, DuplicateRecordError) as e:
            error_log.append((path, line_no, line.strip(), str(e)))
    except (FileNotFoundError, PermissionError) as e:
      error_log.append((path, 0, "", str(e)))

  write_outputs(master_records, event_dict, error_log)
  print(f"[Success] Processed files. Outputs generated in 'output/' directory.")


if __name__ == "__main__":
  # Example test run
  sample_file = "dept_cse.txt"
  sample_data = (
      "192311001,Aarav Kumar,CSE,aarav@college.edu,Coding;Quiz\n"
      "192311002,Priya Sharma,ECE,priya@college.edu,Robotics\n"
      "192311001,Aarav Kumar,CSE,aarav@college.edu,Coding\n"  # Duplicate
      "192311003,Rahul,MECH,invalid-email,Quiz\n"  # Bad email
  )
  with open(sample_file, "w", encoding="utf-8") as f:
    f.write(sample_data)

  process_department_files([sample_file])

  if os.path.exists(sample_file):
    os.remove(sample_file)
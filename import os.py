import os
import csv
import tempfile


# ==========================================
# TASK 1: Mess Bill Processor
# ==========================================
def process_mess_bills(file_path):
  """Safely processes mess bills line by line, handling exceptions and logging rejected rows."""
  total_collection = 0.0
  report_lines = []
  rejected_records = []

  try:
    with open(file_path, "r", encoding="utf-8") as f:
      for line_num, line in enumerate(f, 1):
        line_stripped = line.strip()
        if not line_stripped:  # Skip empty/blank lines
          continue

        parts = line_stripped.split(",")
        if len(parts) != 3:
          rejected_records.append(
              (line_num, line_stripped, "Expected 3 fields, found incorrect count")
          )
          continue

        reg_no, name, amount_str = [p.strip() for p in parts]

        try:
          amount = float(amount_str)  # Supports paise / decimals
          total_collection += amount
          report_lines.append(f"{name} ({reg_no}): ₹{amount:.2f}")
        except ValueError:
          rejected_records.append(
              (line_num, line_stripped, f"Invalid numerical amount '{amount_str}'")
          )

  except FileNotFoundError:
    print(f"[Error] The file '{file_path}' was not found.")
    return
  except PermissionError:
    print(f"[Error] Permission denied when accessing '{file_path}'.")
    return
  except UnicodeDecodeError:
    print(f"[Error] Encoding error encountered while reading '{file_path}'.")
    return

  # Print Report
  print("--- Mess Bill Summary Report ---")
  print("\n".join(report_lines))
  print("-" * 30)
  print(f"Total Collection: ₹{total_collection:.2f}")

  if rejected_records:
    print(f"\n[Audit Log] Rejected {len(rejected_records)} malformed line(s):")
    for r in rejected_records:
      print(f"  Line {r[0]}: '{r[1]}' -> Reason: {r[2]}")


# ==========================================
# TASK 3: Attendance Processor & Custom Exception
# ==========================================
class InvalidRecord(Exception):
  """Raised when a line of the attendance file is not in the expected format."""
  pass


def parse_attendance_line(line):
  """Parses a single attendance line."""
  parts = [p.strip() for p in line.strip().split(",")]
  if len(parts) != 3:
    raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
  
  reg, date, status = parts
  if status not in ("P", "A"):
    raise InvalidRecord(f"invalid status '{status}'")
    
  return (reg, date, status)


def summarise_attendance(path):
  present, absent = 0, 0
  errors = []
  
  try:
    with open(path, "r", encoding="utf-8") as f:
      for line_no, line in enumerate(f, 1):
        if not line.strip():
          continue
        try:
          reg, date, status = parse_attendance_line(line)
          if status == "P":
            present += 1
          elif status == "A":
            absent += 1
        except InvalidRecord as e:
          errors.append((line_no, str(e)))
  except FileNotFoundError:
    errors.append((0, f"File not found: {path}"))
  except PermissionError:
    errors.append((0, f"Permission denied: {path}"))

  return present, absent, errors


# ==========================================
# TASK 6: College Fest Registration Desk
# ==========================================
class InvalidRegistrationError(Exception):
  """Raised when a registration record is malformed."""
  pass


class DuplicateRecordError(Exception):
  """Raised when a register number appears more than once."""
  pass


def validate_email(email):
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


def parse_fest_line(line):
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


def process_fest_registrations(file_paths, output_dir="fest_output"):
  os.makedirs(output_dir, exist_ok=True)
  seen_regs = set()
  master_records = []
  error_logs = []
  event_participants = {}
  total_lines = 0

  for file_path in file_paths:
    if not os.path.exists(file_path):
      error_logs.append((file_path, 0, "N/A", "File not found"))
      continue

    try:
      with open(file_path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
          if not line.strip():
            continue
          total_lines += 1
          try:
            record = parse_fest_line(line)
            if record["reg"] in seen_regs:
              raise DuplicateRecordError(f"Duplicate registration for {record['reg']}")

            seen_regs.add(record["reg"])
            master_records.append(record)

            for event in record["events"]:
              event_participants.setdefault(event, []).append(record)

          except (InvalidRegistrationError, DuplicateRecordError) as e:
            error_logs.append((file_path, line_no, line.strip(), str(e)))

    except PermissionError:
      error_logs.append((file_path, 0, "N/A", "Permission denied"))

  # Write Master CSV
  with open(os.path.join(output_dir, "master_registrations.csv"), "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Register Number", "Name", "Department", "Email", "Events"])
    for r in master_records:
      writer.writerow([r["reg"], r["name"], r["dept"], r["email"], ";".join(r["events"])])

  print(f"[Fest Module] Processed {total_lines} lines. Valid records: {len(master_records)}")


# ==========================================
# Execution Block & Testing
# ==========================================
if __name__ == "__main__":
  print("=== Running Task 1 Test ===")
  mess_data = (
      "192311001,Aarav Kumar,1250\n"
      "192311002,Priya Sharma,1420.75\n"
      "192311003,Rahul\n"
  )
  with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as tmp:
    tmp.write(mess_data)
    tmp_mess_path = tmp.name

  process_mess_bills(tmp_mess_path)
  os.remove(tmp_mess_path)

  print("\n=== Running Task 3 Test ===")
  attendance_data = (
      "192311001,2026-10-08,P\n"
      "192311002,2026-10-08,A\n"
      "192311003,2026-10-08,L\n"
  )
  with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
    tmp.write(attendance_data)
    tmp_att_path = tmp.name

  print("Attendance Summary Result:", summarise_attendance(tmp_att_path))
  os.remove(tmp_att_path)
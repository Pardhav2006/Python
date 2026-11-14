import os
import tempfile


class InvalidRecord(Exception):
  """Raised when a line of the attendance file is not in the expected format."""

  pass


def parse_line(line):
  """Parses a single line: '192311001,2026-10-08,P' -> ('192311001', '2026-10-08', 'P')"""
  parts = [p.strip() for p in line.strip().split(",")]
  
  # TODO 1: Validate exact field count and valid status
  if len(parts) != 3:
    raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
  
  reg, date, status = parts
  if status not in ("P", "A"):
    raise InvalidRecord(f"invalid status '{status}'")
    
  return (reg, date, status)


def summarise(path):
  present, absent = 0, 0
  errors = []
  
  # TODO 2: Open file safely with context manager and handle exceptions
  try:
    with open(path, "r", encoding="utf-8") as f:
      for line_no, line in enumerate(f, 1):
        if not line.strip():
          continue
        try:
          reg, date, status = parse_line(line)
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


# Test Execution block matching expected output
if __name__ == "__main__":
  data = (
      "192311001,2026-10-08,P\n"
      "192311002,2026-10-08,A\n"
      "192311003,2026-10-08\n"
      "192311004,2026-10-08,L\n"
  )
  with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8") as tmp:
    tmp.write(data)
    tmp_name = tmp.name

  print(summarise(tmp_name))
  os.remove(tmp_name)
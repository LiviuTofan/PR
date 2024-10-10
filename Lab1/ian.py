from datetime import datetime, timezone, timedelta

local_timezone = timezone(timedelta(hours=3))

# Get the current time in your local timezone
local_timestamp = datetime.now(local_timezone).isoformat()
print("Local Timestamp:", local_timestamp)
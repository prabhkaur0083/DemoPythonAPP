from datetime import datetime, timezone

# Convert expiration time to a datetime object

def convertTimeIntoSeconds(expiration_time_str):
    expiration_time = datetime.fromisoformat(expiration_time_str.replace("Z", "+00:00"))
    current_time = datetime.now(timezone.utc)

    # Calculate TTL in seconds
    ttlSeconds = int((expiration_time - current_time).total_seconds())

    return ttlSeconds

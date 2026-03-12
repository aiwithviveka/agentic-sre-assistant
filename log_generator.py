import time
import random
from datetime import datetime

LOG_FILE = "sre_logs.log"

SCENARIOS = [
    "INFO: API Gateway heartbeat stable.",
    "ERROR: 500 Internal Server Error - Backend 'auth-service' timed out.",
    "WARNING: Memory usage at {value}% in 'api-gateway' pod.",
    "CRITICAL: Database connection pool exhausted - max_connections reached.",
    "ALERT: {value} failed login attempts detected from IP 192.168.1.{ip_end}.",
    "DEBUG: Disk I/O wait time higher than 500ms on /dev/sda1.",
    "INFO: New deployment 'payment-v3' completed successfully."
]

def generate_log():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Pick a random scenario and fill in random values if needed
    message = random.choice(SCENARIOS).format(
        value=random.randint(85, 99),
        ip_end=random.randint(2, 254)
    )
    
    log_entry = f"{timestamp} {message}\n"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
        
    print(f"📝 Logged: {log_entry.strip()}")

if __name__ == "__main__":
    print(f"🚀 Log Generator started. Writing to {LOG_FILE} every 30 seconds...")
    print("Press Ctrl+C to stop.\n")
    
    try:
        while True:
            generate_log()
            time.sleep(30)
    except KeyboardInterrupt:
        print("\nStopping Log Generator...")
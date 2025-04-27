import RPi.GPIO as GPIO
import time
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta

# Email Configuration
from_email_addr = "fei87283@gmail.com"  # Sender Gmail
from_email_pass = "ailw kzyq tjsk grcr"  # Gmail App Password
to_email_addr = "1712633125@qq.com"  # Recipient QQ email
smtp_server = "smtp.gmail.com"  # Gmail SMTP server
smtp_port = 587  # TLS port

# GPIO Setup
moisture_sensor_channel = 4
GPIO.setmode(GPIO.BCM)
GPIO.setup(moisture_sensor_channel, GPIO.IN)


def send_email(needs_water):
    """Send email notification"""
    msg = EmailMessage()
    msg['From'] = from_email_addr
    msg['To'] = to_email_addr
    msg['Subject'] = "Plant Watering Alert"

    body = "ALERT: Water needed! Soil is too dry!" if needs_water else "Status OK: Soil moisture is sufficient, no watering needed."
    msg.set_content(body)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email_addr, from_email_pass)
            server.send_message(msg)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


def check_moisture():
    """Check soil moisture, returns True if watering is needed"""
    return GPIO.input(moisture_sensor_channel)  # LOW signal means dry


def calculate_next_run():
    """Calculate next run time (every 4 hours on the hour)"""
    now = datetime.now()
    next_run = now + timedelta(hours=4)
    # Align to nearest 4-hour mark (00:00, 04:00, 08:00...)
    next_run = next_run.replace(minute=0, second=0, microsecond=0)
    return next_run


def main():
    try:
        print("Plant monitoring system starting...")
        while True:
            # Check soil moisture
            needs_water = check_moisture()
            status = "DRY" if needs_water else "OK"
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Soil status: {status}")

            # Send email notification
            send_email(needs_water)

            # Calculate and wait for next check
            next_run = calculate_next_run()
            wait_seconds = (next_run - datetime.now()).total_seconds()
            print(f"Next check at: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
            time.sleep(wait_seconds)

    except KeyboardInterrupt:
        print("\nProgram terminated")
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()

import pytz
from datetime import datetime
import sys

def convert_timezone(dt_str, from_tz_name, to_tz_name, dt_format="%Y-%m-%d %H:%M:%S"):
    """
    this converts a datetime string from one timezone to another.
    """
    try:
        # 1. define the timezones
        from_tz = pytz.timezone(from_tz_name)
        to_tz = pytz.timezone(to_tz_name)
    except pytz.exceptions.UnknownTimeZoneError as e:
        print(f"\n Error: Unknown timezone name provided. {e}")
        print("Please use standard names like 'America/New_York' or 'Asia/Kolkata'.")
        return

    try:
        # 2. parses the input datetime string
        naive_dt = datetime.strptime(dt_str, dt_format)
        
        # 3. localises the naive datetime object (make it timezone-aware)
        localized_dt = from_tz.localize(naive_dt)
        
        # 4. convert to the target timezone
        converted_dt = localized_dt.astimezone(to_tz)
        
        print("\n Conversion Result ")
        print(f"Original Time: {localized_dt.strftime(dt_format)} ({from_tz_name})")
        print(f"Converted Time: {converted_dt.strftime(dt_format)} ({to_tz_name})")

    except ValueError:
        print(f"\n Error: Time string '{dt_str}' does not match expected format '{dt_format}'.")
    except Exception as e:
        print(f"\n An unexpected error occurred: {e}")

if __name__ == "__main__":
    print("✨ Python Timezone Converter ✨")
    
    # simple check for dependencies
    try:
        pytz.timezone('UTC') # checks if pytz is available
    except NameError:
        print("\nFATAL ERROR: 'pytz' library is not installed.")
        print("Please run: pip install pytz\n")
        sys.exit(1)
        
    # the default values for interactive mode
    default_format = "%Y-%m-%d %H:%M:%S"
    
    time_str = input(f"Enter time (e.g., 2023-10-27 15:30:00): ").strip()
    from_tz = input("Enter source timezone (e.g., Asia/Kolkata): ").strip()
    to_tz = input("Enter target timezone (e.g., Europe/London): ").strip()

    if time_str and from_tz and to_tz:
        convert_timezone(time_str, from_tz, to_tz, default_format)
    else:
        print("All fields are required. Exiting.")
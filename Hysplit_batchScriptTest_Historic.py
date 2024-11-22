import os
from datetime import datetime, timedelta

# Define paths (adjust as per your system)
hysplit_path = "/path/to/hysplit"  # Path to HYSPLIT installation
working_dir = "/path/to/working/directory"  # Working directory for the script
meteo_dir = "/path/to/hrrr/data"  # Directory containing HRRR meteorological data

# Define parameters
start_date = datetime(2022, 9, 7)  # Start date
end_date = datetime(2022, 9, 19)  # End date
interval_hours = 1  # Trajectory start time interval (hours)
runtime_hours = 24  # Trajectory runtime in hours
latitude = 40.0  # Starting latitude (example value)
longitude = -105.0  # Starting longitude (example value)
altitude = 500  # Starting altitude (meters)

# Create working directory if it doesn't exist
if not os.path.exists(working_dir):
    os.makedirs(working_dir)

# Function to generate CONTROL file
def write_control_file(start_time):
    control_file = os.path.join(working_dir, "CONTROL")
    with open(control_file, "w") as f:
        f.write(f"{start_time.strftime('%y %m %d %H')}\n")  # Start time
        f.write(f"1\n")  # Number of starting locations
        f.write(f"{latitude:.2f} {longitude:.2f} {altitude}\n")  # Starting location
        f.write(f"{runtime_hours}\n")  # Runtime (hours)
        f.write(f"0\n")  # Forward trajectory (use -1 for backward)
        f.write(f"{meteo_dir}\n")  # Meteorology files path
        f.write(f"{working_dir}/\n")  # Working directory for output
        f.write(f"tdump\n")  # Output file name

# Function to run HYSPLIT
def run_hysplit():
    os.chdir(hysplit_path)
    os.system("./hyts_std")

# Loop through each hour in the date range
current_time = start_date
while current_time <= end_date:
    print(f"Running trajectory for {current_time}...")
    write_control_file(current_time)  # Write CONTROL file
    run_hysplit()  # Run HYSPLIT
    # Move output file to avoid overwriting
    output_file = os.path.join(working_dir, "tdump")
    new_output_file = os.path.join(working_dir, f"tdump_{current_time.strftime('%Y%m%d%H')}")
    os.rename(output_file, new_output_file)
    current_time += timedelta(hours=interval_hours)

print("Trajectory simulations complete.")
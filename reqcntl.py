import os               # Provides functions for interacting with the operating system (e.g., file paths, renaming)
import datetime         # Used to generate timestamps for logging
import glob             # Used to find files matching a pattern (e.g., *.txt)

# Function to log messages with a timestamp
def log(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current time in readable format
    #print "[%s] %s" % (timestamp, message)  # Print the message with timestamp (Python 2 style)

# Function to parse store codes from the input text file
def parse_store_codes(input_file):
    store_codes = []  # Initialize empty list to hold store codes
    try:
        with open(input_file, "r") as f:  # Open the input file in read mode
            for line in f:  # Read each line from the file
                line = line.strip()  # Remove leading/trailing whitespace
                # Process only lines that start with "Store" or have leading spaces before "Store"
                if line.startswith("Store") or line.startswith("  Store"):
                    parts = line.split()  # Split the line into words
                    if len(parts) >= 3:  # Ensure there are enough parts to extract store number and location
                        store_num = parts[1]  # Extract store number
                        location = parts[2]  # Extract location (Primary or Secondary)
                        # Append appropriate suffix based on location
                        suffix = "D100" if location.lower() == "primary" else "D101"
                        store_code = store_num.zfill(5) + suffix  # Combine store number and suffix
                        store_codes.append(store_code)  # Add to list
    except Exception as e:
        log("Error reading input file: %s" % str(e))  # Log any error encountered while reading the file
    return store_codes  # Return the list of parsed store codes

# Function to rename REQCNTL.NEW to REQCNTL.dat for each store code
def rename_reqcntl_files(store_codes):
    failed_stores = []  # List to track stores where renaming failed
    for code in store_codes:  # Loop through each store code
        # Construct UNC path to the store's data folder
        path = r"\\%s\c$\Chainlnk\data" % code
        source_file = os.path.join(path, "REQCNTL.NEW")  # Full path to source file
        target_file = os.path.join(path, "REQCNTL.dat")  # Full path to target file

        try:
            if os.path.exists(source_file):  # Check if source file exists
                os.rename(source_file, target_file)  # Rename the file
                log("Renamed for %s" % code)  # Log success
            else:
                log("REQCNTL.NEW not found for %s" % code)  # Log missing file
                failed_stores.append(code)  # Track failed store
        except Exception as e:
            log("Error for %s: %s" % (code, str(e)))  # Log any error during renaming
            failed_stores.append(code)  # Track failed store

    # Write all failed store codes to a separate file
    try:
        with open("failed_stores.txt", "w") as f:  # Open file in write mode
            for code in failed_stores:  # Loop through failed stores
                f.write(code + "\n")  # Write each code on a new line
        log("Failed store codes written to failed_stores.txt")  # Log completion
    except Exception as e:
        log("Error writing failed_stores.txt: %s" % str(e))  # Log any error during file writing

# Main execution block
if __name__ == "__main__":
    anyFile = glob.glob('*.txt')  # Find all .txt files in the current directory
    input_file = anyFile[1]  # Select the second file in the list (risky if only one file exists)
    # Alternative: use a fixed path or safer indexing
    # input_file = r"C:\Users\admin-dks0614473\Desktop\New Script\Reqcntl Automation\store_input.txt"
    store_codes = parse_store_codes(input_file)  # Parse store codes from the input file
    rename_reqcntl_files(store_codes)  # Attempt to rename files for each store
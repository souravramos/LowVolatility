import logging

from win32netcon import LG_INCLUDE_INDIRECT

from file_paths import LOG_FILE_PATH

def configure_logger():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,  # Set the log level
        format="%(asctime)s - %(levelname)s - %(message)s",  # Log message format
        handlers=[
            logging.FileHandler(LOG_FILE_PATH),  # Log to file
            logging.StreamHandler()  # Log to console
        ]
    )

with open(LOG_FILE_PATH, "w") as file:
    file.truncate(0)

# Function call to configure the logger when the module is imported
configure_logger()


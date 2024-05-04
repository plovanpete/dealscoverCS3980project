import os

# Set the path to your service account JSON key file
key_file_path = "dealicious-locator-e4b133b45869"

# Set the environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_file_path

# Now you can import and use Google Cloud libraries
from google.cloud import storage

# Continue with your script logic...

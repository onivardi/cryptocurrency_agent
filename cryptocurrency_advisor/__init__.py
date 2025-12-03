from . import agent
from dotenv import load_dotenv
from pathlib import Path

# 1. Define the base directory. 
# We look for the .env file in the PARENT directory of 'cryptocurrency_advisor'.
# The path to the .env file, based on your image, is:
# cryptocurrency_agent/.env
BASE_DIR = Path(__file__).resolve().parent.parent 
dotenv_path = BASE_DIR / '.env'

# 2. Load the environment variables explicitly using the calculated path
load_dotenv(dotenv_path=dotenv_path)

# 3. Define the key

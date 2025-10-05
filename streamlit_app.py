# Streamlit Cloud Entry Point
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'frontend'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

# Import the main app
from frontend.app import main

if __name__ == "__main__":
    main()
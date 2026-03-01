# Community Pollution Forum

## Setup Instructions

1. Create a virtual environment:
   ```
   python -m venv .venv
   ```

2. Activate the virtual environment:
   - On Windows: `.venv\Scripts\activate`
   - On macOS/Linux: `source .venv/bin/activate`

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Initialize the database:
   ```
   flask shell
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

5. Run the application:
   ```
   flask run
   ```

## Features

- Map UI with pollution data
- Community forum for discussions
- Event management system
- Contact government page
# CardioTrack

CardioTrack is a Django-based application for recording and managing patient health data, including heartbeat, sugar, and cholesterol levels. It supports audit trails, user roles, and organizational linkage.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/rohitrkvarathe111/CardioTrack.git
cd CardioTrack
```

2. Create a virtual environment:
```bash
python -m venv venv
# On Linux/macOS
source venv/bin/activate
# On Windows
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply migrations:
```bash
python manage.py makemigrations

python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the server:
```bash
python manage.py runserver
```

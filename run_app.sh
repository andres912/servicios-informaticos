docker-compose up -d
source venv/bin/activate
pip install -r requirements.txt
flask db upgrade
flask run --port=8000
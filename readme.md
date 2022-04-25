## Repositorio de Heroku para la materia Servicios Informáticos

### Tecnologías utilizadas:
- Python
- Heroku
- Flask
- SQLAlchemy
- PostgreSQL
- Docker Compose

### Requisitos:
(Además de las tecnologías mencionadas)
- Crear una base de datos en PostgreSQL (los datos tienen que ser de acuerdo a lo que figura en .env.dev)
- (Librería no relacionada a Python): libpq-dev (sudo apt-get install libpq-dev) -> necesaria para instalar psycopg2
   
### Preparación (ubuntu):
```sh
sudo apt install libpq-dev
python3 -m venv venv
```

### Ejecución:
Correr el script `run_app.sh` o, en su defecto:  

- (Terminal 1): 
    - docker-compose up db
- (Terminal 2):
    - source venv/bin/activate (levanta un entorno virtual)
    - pip install -r requirements.txt (instalar las dependencias) (instalar libpq-dev antes de este paso)
    - flask db upgrade (actualizar la base de datos)
    - flask run --port=8000 (correr el servidor en el puerto 8000, se puede omitir el puerto)
    
Intentar pegarle a los endpoints de la API para ver si todo funciona bien

### Aclaraciones:
- Se puede ejecutar flask run, dejarlo corriendo y hacer cambios en el código. Se deberían detectar automáticamente y reiniciar la corrida.
- Las migraciones deberían crearse corriendo flask db migrate, luego de agregar nuevas clases. Los cambios en las clases se detectan (indirectamente) a través de la cadena de imports que empieza en los blueprints importados en el archivo __init__.py. 

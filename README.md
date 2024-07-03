# INFORCE-PYTHON-TASK



### How to run:
- Copy .env.sample -> .env and populate with all required data
- `docker-compose up --build`
- Create admin user (Optional)
- `docker-compose exec -ti api python manage.py createsuperuser`
- Load db data from file (Optional)
- `docker-compose exec -ti api python manage.py loaddata db.yaml`
- Create schedule in admin panel for running task 'Choose Winner Cafe' in DB (Optional)

Test admin user:
username: `test_admin`
password: `1111`

![img_1.png](media/img_1.png)
![img.png](demo/img.png)
![img_2.png](demo/img_2.png)
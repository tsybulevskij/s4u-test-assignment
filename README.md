# eglobal-s4u

**Main requirements:**
- python 3.5
- django 1.11
- angular 1.6
- bootstrap 3.3


### Deploy
Clone repository

**Backend:**
```
virtualenv env -p python3.5
. env/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py collectstatic
```

**Frontend:**
```
cd frontend/
npm install
```

**Run:**
server will be started by default on 127.0.0.1:8000
```
./manage.py runserver
```

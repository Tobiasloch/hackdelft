
Create and activate virtual env
```
python -m venv venv
source venv/bin/activate

```
run
```
pip install -r requirements.txt
```

to install all the dependencies and then run:

```
uvicorn app.src.main:app --reload
```

to start the server.

# chetter

Llama server submodule:
    
- To add: `git submodule add https://github.com/IshanG97/llama_server.git llama_server`
    
- To update when cloning Chetter for the first time: `git submodule update --init --recursive`

mongodb (macOS):
    
- start mongodb: `brew services start mongodb/brew/mongodb-community`
    
- go into mongo shell (also check if it's running): `mongosh`
    
- stop mongodb: `brew services stop mongodb/brew/mongodb-community`
   
- save mongodb: `mongodump --db your_database_name --out /path/to/dump`
    
- restore mongodb: `mongorestore --db your_database_name /path/to/dump/your_database_name`

start backend server: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`
    
- `main` is the `main.py` file
    
- `app` is the `app=FastApi()` bit
    
- `host 0.0.0.0` makes the server available to all devices on the network (subnet mask)
    
- `port 8000` is the exposed port on the service the files are served on
    
- `reload` is for hot reloading

Testing:
    
- post user: `curl -X POST http://localhost:8000/create_user/ -H "Content-Type: application/json" -d @tamika.json`
    
- post cheet: `curl -X POST http://localhost:8000/create_cheet/ -H "Content-Type: application/json" -d @gigacheet.json`

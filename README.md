# setup
```
cd OCapp
docker compose up --build -d
```

# set your OPENAI API KEY
```
docker exec -it [YOUR_BACKEND_CONTAINER_ID] bash
```
```
export OPENAI_API_KEY = "[YOUR_OPENAI_API_KEY]"
exit
```

#### praktikum_new_diplom  
# Foodgram - «Продуктовый помощник» 

мои настройки на винде пайтон 3.9 (пробую 3.11)  
дома пайтон 3.10.7  

чтобы добраться до редока надо:  
`sudo docker-compose up`  

### Установка: 
#### Windows
`python -m venv venv `  
`venv/Scripts/activate `  
`python -m pip install --upgrade pip `

перейти в дирректорию backend  

`pip install -r requirements.txt `

#### Linux
`python3 -m venv venv `  
`source venv/bin/activate`  
`python -m pip install --upgrade pip `  
`pip install --upgrade setuptools ` опционально...  
`python -m pip install --upgrade pip setuptools` либо так)  

перейти в дирректорию backend  

`pip install -r requirements.txt `

Регистрация нового пользователя:
```
POST /api/v1/auth/signup/

{
  "email": "string",
  "username": "string"
}
```

Получение JWT-токена:
```
POST api/auth/token/login/

{
  "email": "string",
  "password": "string"
}
```

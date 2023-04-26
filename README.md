# fastAPI_Chat
### Stack:
_Backend_
+ FastAPI
+ SQLAlchemy
+ MongoDB

_Frontend_
+ HTML(Jinja2), CSS
+ JS(JQuery)

### Functional:
1. Registration and Login with hash password and OAuth2 with custom cookie. 
2. WebSoket chats with private messages
   + Send text
   + Receive text
   + Save chat history

### How are you can launch this:
1. Clone git repository: https://github.com/Inott-git/fastApi_Chat.git
2. Download requirements -> _pip install -r requirements.txt_
3. Get connection link for MongoDB(for example, from [MongoDB Compass](https://www.mongodb.com/try/download/compass))
![](image/connectionlink.png?raw=true)
4. Start app -> _uvicorn main:root --reload_
5. You can see endpoint -> [Docs](http://127.0.0.1:8000/docs)
![](image/docs.png?raw=true)
6. The chat(first login or register) itself -> [Home](http://127.0.0.1:8000/)
7. You can register 2 users(and add by id(number of account) in menu)
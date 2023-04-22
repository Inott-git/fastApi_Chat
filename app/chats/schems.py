from pydantic import BaseModel

class ChatUser(BaseModel):
    uid: int
    username: str


class Msg(BaseModel):
    user_id: int
    msg: str


class Chat(BaseModel):
    users: list[ChatUser]
    msgs: list[Msg] = []



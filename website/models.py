# datetime : 현재 시간을 0000-00-00T00:00:00.000000 의 형태로 저장
# certifi :mongoDB의 보안관련 클래스
from datetime import datetime
from . import db
from pymongo import MongoClient
import certifi

#####################################################################################

ca = certifi.where()
client = MongoClient(
    "mongodb+srv://joonyeol:1234@sparta.afgjtfy.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=ca,
)
db = client.dbsparta

#####################################################################################

# 미리 알고갈 지식들
# class : 쉽게 생각하면 함수 모음, 일반적으로 class는 함수와의 구분을 위해
# camel 표기법으로 이름을 만듭니다. camel타입은 단어의 첫글자를 대문자로 적는것
# ex) class TeamProject
# 다른 표기법으로는 snake 표기법이 있음 보통 변수나 함수에 많이 사용
# ex) def team_member_joonyeol

#####################################################################################

# 게임리뷰 관련 클래스


class Gamepost:
    # 너무 길어서 보기좋게 바꿈
    def __init__(
        self,
        post_title,
        nickname,
        password,
        content,
        image_url=None,
        main_url=None
    ):
        self.post_title = post_title
        self.nickname = nickname
        self.password = password
        self.content = content
        self.image_url = image_url
        self.main_url = main_url
        self.date = datetime.now()

    # 저장함수
    def save(self):
        postlist_data = {
            "post_title": self.post_title,
            "nickname": self.nickname,
            "password": self.password,
            "content": self.content,
            "image_url": self.image_url,
            "main_url": self.main_url,
            "date": self.date
        }
        # DB에 저장
        db.gameposts.insert_one(postlist_data)

        # mongoDB에 저장될 때 objectid 형태로 저장되기 때문에 실제 사용할 때 불편함
        # objectid를 str형태로 바꿔서 DB에 업데이트
        post_id = str(postlist_data['_id'])
        db.gameposts.update_one({'_id': postlist_data['_id']}, {
                                '$set': {'post_id': post_id}})

    def find(post_id):
        return db.gameposts.find_one({'post_id': post_id})

    def all():
        return list(db.gameposts.find({}))

    # 업데이트함수

    def update(post_id, post_title=None, content=None, image_url=None, main_url=None):

        # 유효성검사
        if post_title == "":
            pass
        else:
            db.gameposts.update_one(
                {'post_id': post_id}, {'$set': {'post_title': post_title}})
        if content == "":
            pass
        else:
            db.gameposts.update_one(
                {'post_id': post_id}, {'$set': {'content': content}})
        if image_url == "":
            pass
        else:
            db.gameposts.update_one(
                {'post_id': post_id}, {'$set': {'image_url': image_url}})
        if main_url == "":
            pass
        else:
            db.gameposts.update_one(
                {'post_id': post_id}, {'$set': {'main_url': main_url}})

    # 삭제함수
    def delite(post_id):
        db.gameposts.delete_one({'post_id': post_id})

# 댓글 관련 클래스, 작성중


class Comment:
    def __init__(
        self,
        nickname,
        comment,
        post_id
    ):
        self.nickname = nickname
        self.comment = comment
        self.post_id = post_id
        self.date = datetime.now()

    def save(self):
        comment_data = {
            "nickname": self.nickname,
            "comment": self.comment,
            "post_id": self.post_id,
            "date": self.date
        }
        db.gamecomments.insert_one(comment_data)
        comment_id = str(comment_data['_id'])
        db.gamecomments.update_one({'_id': comment_data['_id']}, {
                                   '$set': {'post_id': comment_id}})

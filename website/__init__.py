# Flask 앱을 만들기 위해 flask 모듈을 참조
# 플라스크 APP을 초기화 하는 함수를 만듭니다. 인자는 __name__ 변수
# __name__ 은 현재 __name__이 작성된 파일명을 문자열로 저장하고 있거나 __main__이란 문자열 값을 저장
# certifi :mongoDB의 보안관련 클래스
from flask import Flask
from pymongo import MongoClient
import certifi

ca = certifi.where()
client = MongoClient(
    'mongodb+srv://joonyeol:1234@sparta.afgjtfy.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'nebecamp-miniproject-16team'

    # url_prefix : url접두사. 해당 블루프린트를 이용할 때 기본적으로 붙을 url을 적음
    # 블루프린트 인스턴스 가져오기
    from .views import views

    # 플라스크 앱에 등록하기
    app.register_blueprint(views, url_prefix='/')

    return app

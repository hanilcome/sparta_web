# pip install flask pymongo certifi
# flask app을 생성합니다.
# 플라스크 앱, 즉 서버를 실행하는데 디버그 모드를 활성화하여 실행
from website import create_app
app = create_app()

# 해당 파이썬 파일이 참조될 때는 실행하지 않고, 프로젝트의시작 파일일때만 실행
if __name__ == "__main__":
    app.run('0.0.0.0', port=5000, debug=True)

'''
+ 폴더 파일 설명
website : 구현할 웹 사이트의 모든 코드가 저장
main.py : 웹 서버가 시작(run)시키는 코드
__init__.py : website 폴더를 웹 사이트 관련 폴더로 인식시키기 위해서 생성. 패키지화.
static, templates : 웹 페이지를 구성하는 파일(html, css, js)들을 놓아두고 서버가 활용하도록 함
views.py : 클라이언트가 요청해서 서버가 웹 사이트를 보여주기위해 응답하는 과정의 모든 데이터의 요청과 응답을 관여

+ 일어난 일의 순서
1. 웹 브라우저에서 url 접속을 함
2. Flask 서버에 클라이언트 요청이 전달
3. Flask APP에서 일치하는 url을 탐색
4. Blueprint 'views'를 이용하여 Flask APP의 라우팅 시스템(Routing System)에 url을 등록해놨음
	Route는 외부에서 웹 서버로 접근 시 사용한 url을 확인하여 매핑된 함수를 실행하고, 그 결과를 돌려주는 역할을 한다.
5. 따라서 views.py의 home함수가 실행되고
6. 그 return값을 받고 렌더링하여 클라이언트에게 응답
'''

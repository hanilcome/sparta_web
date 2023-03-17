# 각 import들이 하는 일
# Blueprint : 플라스크 app의 모든 url을 한 곳에서 관리하지 않아도 됨
# 여러곳에 뿌려진 url의 정의를 수집하여 한 곳을 모아줌
# redirect : 웹 브라우저가 요청한 URL을 다른 URL로 자동으로 전환해줌
# render_template : HTML을 렌더링하기 위해 필요한 데이터를 전달 후 렌더링한 결과를 반환
# request : 클라이언트가 전송한 HTTP 요청 메시지에 포함된 데이터를 읽을 수 있음
# url_for : URL을 동적으로 생성할 때 라우트 함수의 이름을 사용
from flask import Blueprint, request, jsonify, render_template, redirect, url_for

# models.py에서 정의한 class 내부의 함수를 불러옴
from .models import Gamepost as gp

# init.py에서 정의한 db를 불러옴 init.py는 최상위 실행 파일이므로 from . 만 적어도 된다
from . import db

import random
#####################################################################################

# Blueprint에 view.py를 정의하여 보여질 페이지와 경로를 정의
# 기존엔 app.py에서 app.route만 썼으나 여러 페이지를 사용하기 때문에
# route를 Blueprint에 저장 후 Blueprint에서 처리함
# '클라이언트 요청 > 서버의 응답'을 과정을 세부적이게 구현할 필요가 없음
# 반드시 Blueprint 등록 후엔 init.py에 가서 다음 코드를 적어야 한다
# from .views import views
# app.register_blueprint(views, url_prefix='/')
views = Blueprint("views", __name__)

#####################################################################################

# 메인페이지(/)


@views.route("/", methods=["GET", "POST"])
def home():
    posts = gp.all()
    posts.reverse()
    count = 0
    # 최신포스트면 <div class="carousel-item active"> 가게 하려고 만듬
    for post in posts:
        count += 1
        post['count'] = count
    return render_template("home.html", posts=posts)

#####################################################################################

# 상세페이지(/detail)


@views.route("/detail", methods=["GET", "POST"])
def gamepost():
    if request.method == "POST":
        post_title = request.form["post_title"]
        nickname = request.form["nickname"]
        password = request.form["password"]
        content = request.form["content"]
        image_url = request.form["image_url"]
        main_url = request.form["main_url"]

        # 유효성 검사
        if len(post_title) < 1 or len(nickname) < 1 or len(content) < 1 or len(password) < 1:
            return jsonify({"msg": "공백이 있습니다. 내용을 모두 채워주세요"})
        elif len(post_title) > 30 or len(nickname) > 30 or len(password) > 30:
            return jsonify({"msg": "너무 깁니다. 30자 이내로 적어주세요"})
        elif len(content) > 1000:
            return jsonify({"msg": "내용이 너무 많습니다. 1000자 이내로 적어주세요"})
        elif image_url == "":
            image_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQkAAAC4CAMAAADHV+kyAAAAM1BMVEX////MzMyrq6vX19fq6urv7+/Y2NjAwMD19fX5+fmxsbHQ0NDf39+1tbXl5eXc3Ny7u7tOeLhWAAADrElEQVR4nO2b2WKjIBRAFTSiGMn/f+1wWdSYNtOxaTPiOQ+NEUzhyGVxqSoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACiQfrroXVym/t1lfym9rneji1Lh9ouoa/fu0r8S+x0T9t2lfyWxmV/+mRhU7y79K9ndyF2JJto9B7aYSGAic2YTfeO0m6dTJzbRxAHXTvHreU008ywiqjitCbOaUIX8pzUxrkxcZMdZTfTrWbmVXvO0Ju7WG6bCBCaq9WWMU0dHNa1MhBXbaU2su0wJjrOYMKNrNrvaWUVMOYcJI7UetzsvwYNOuU9hIkXCVkVlpmma857CRB4npmcHnsHEcrn7mYoTmFiPl9tuc0X5Jpp6zSppc5uneBPm/gaIzWmNtfexUrqJfnsnyIZpVAyZOxWlm7jUW0RF7x570MJNjA8i5MLlNC+/Vj1o2SamD0Tcs6go2kT7VxErayWbMF+5b27vtL2t2D/AYuJh2PhERRxMSjbxOGw8VVGuiY+GjU9UhNlmsSb+Pmws6JKvY35l2FiQWz+FmvjSsLHClWri3x9FdIWa2PEo4lSkiV0Pp+oSTezn3aV/JZjIYCKDiQwmMpjIYCLDWw0Z3nTJ8PbTDG/EAQAAAAAAAPwuWocn9Y3W8tG7uqtdvyQaSUmXH5zW8TmzlDlsuq7rnAl5I+YXC/9SlFLy1ESjlP87DUoY2jmxkRQVZfmNaMClPWEroMMPBZ484f1/48veVcmEGdTVn9VBDSYniomruskXO5u4xmO8ORUOuCkneeujt4mrnMZgolaDxEE/qDonionuFprN1ecMJlq/oUKFr8lIk/IeGn8q1TWZGFS8Rm1lT0wMJpzsn1TXRRO1sp20AomXafVDhzfh6+OiiVyxMXQa1WzCqEHqPyYTg2rH4Mof1K9+6PAmfBMY+mQiVqbZmKg6NfbeRjQhFvrQz8Z8nbD0mG+ryXfxRff9gn5uYooREk10EiuddCUxX6q/Urfk5KBIJWRUfBYdsbc00YRJ535YouNO42EJlZaKKvnIPeYtJyYTOoybwUSeQvgpRZvUFWSiiQ38s1E0NIQxmbjFbrOLTeXWV0WZ8PVKM6vBarudWUnot00VTbRpKjHKp8ysrNZdNBFnVof1EU206slse+4ExUSOHN9w3BIqq7FDP/yLg5AWU2NagY22s+NmBTa/TD36E+7ySR/DfuP8AeEN87wCO2ybAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAf5w/pNR2oA/UcowAAAABJRU5ErkJggg=="
        elif main_url == "":
            main_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQkAAAC4CAMAAADHV+kyAAAAM1BMVEX////MzMyrq6vX19fq6urv7+/Y2NjAwMD19fX5+fmxsbHQ0NDf39+1tbXl5eXc3Ny7u7tOeLhWAAADrElEQVR4nO2b2WKjIBRAFTSiGMn/f+1wWdSYNtOxaTPiOQ+NEUzhyGVxqSoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACiQfrroXVym/t1lfym9rneji1Lh9ouoa/fu0r8S+x0T9t2lfyWxmV/+mRhU7y79K9ndyF2JJto9B7aYSGAic2YTfeO0m6dTJzbRxAHXTvHreU008ywiqjitCbOaUIX8pzUxrkxcZMdZTfTrWbmVXvO0Ju7WG6bCBCaq9WWMU0dHNa1MhBXbaU2su0wJjrOYMKNrNrvaWUVMOYcJI7UetzsvwYNOuU9hIkXCVkVlpmma857CRB4npmcHnsHEcrn7mYoTmFiPl9tuc0X5Jpp6zSppc5uneBPm/gaIzWmNtfexUrqJfnsnyIZpVAyZOxWlm7jUW0RF7x570MJNjA8i5MLlNC+/Vj1o2SamD0Tcs6go2kT7VxErayWbMF+5b27vtL2t2D/AYuJh2PhERRxMSjbxOGw8VVGuiY+GjU9UhNlmsSb+Pmws6JKvY35l2FiQWz+FmvjSsLHClWri3x9FdIWa2PEo4lSkiV0Pp+oSTezn3aV/JZjIYCKDiQwmMpjIYCLDWw0Z3nTJ8PbTDG/EAQAAAAAAAPwuWocn9Y3W8tG7uqtdvyQaSUmXH5zW8TmzlDlsuq7rnAl5I+YXC/9SlFLy1ESjlP87DUoY2jmxkRQVZfmNaMClPWEroMMPBZ484f1/48veVcmEGdTVn9VBDSYniomruskXO5u4xmO8ORUOuCkneeujt4mrnMZgolaDxEE/qDonionuFprN1ecMJlq/oUKFr8lIk/IeGn8q1TWZGFS8Rm1lT0wMJpzsn1TXRRO1sp20AomXafVDhzfh6+OiiVyxMXQa1WzCqEHqPyYTg2rH4Mof1K9+6PAmfBMY+mQiVqbZmKg6NfbeRjQhFvrQz8Z8nbD0mG+ryXfxRff9gn5uYooREk10EiuddCUxX6q/Urfk5KBIJWRUfBYdsbc00YRJ535YouNO42EJlZaKKvnIPeYtJyYTOoybwUSeQvgpRZvUFWSiiQ38s1E0NIQxmbjFbrOLTeXWV0WZ8PVKM6vBarudWUnot00VTbRpKjHKp8ysrNZdNBFnVof1EU206slse+4ExUSOHN9w3BIqq7FDP/yLg5AWU2NagY22s+NmBTa/TD36E+7ySR/DfuP8AeEN87wCO2ybAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIAf5w/pNR2oA/UcowAAAABJRU5ErkJggg=="
        else:
            # gamepost 인스턴스 생성 -> DB에 저장
            new_post = gp(post_title=post_title,
                          nickname=nickname,
                          password=password,
                          content=content,
                          image_url=image_url,
                          main_url=main_url
                          )
            new_post.save()
            return redirect(url_for("views.gamepost"), jsonify({"msg": "새 게시글 작성 완료!"}))

    # 포스트 리스트 반전 = 최신이 처음에 옴
    posts = gp.all()
    posts.reverse()
    # 포스트 갯수 count해서 홀수면 image우측, 짝수면 image좌측
    count = 0
    colors = ['#FECCBE', '#FEEBB6', '#94DEFF', '#E0BFE6', '#595959']
    for post in posts:
        count += 1
        post['count'] = count
        post['color'] = random.choice(colors)
    return render_template("detail.html", posts=posts)


@views.route("/detail/update", methods=["GET", "POST"])
def gamepost_update():
    post_id = request.args.get("post_id")
    if request.method == "POST":
        post_title = request.form["post_title"]
        content = request.form["content"]
        image_url = request.form["image_url"]
        main_url = request.form["main_url"]
        post_id = request.form["post_id"]

        gp.update(post_id=post_id,
                post_title=post_title,
                content=content,
                image_url=image_url,
                main_url=main_url
        )
        
        return redirect(url_for("views.gamepost"))
    post = gp.find(post_id)
    return render_template("detail_update.html", post=post)


@views.route("/detail/check_pw", methods=["POST"])
def check_pw():
    check_password = request.form["check_password"]
    post_id = request.form["post_id"]
    print(post_id)
    if check_password == gp.find(post_id)['password']:
        return jsonify({"msg": "success"})
    else:
        return jsonify({"msg": "비밀번호가 일치하지 않습니다."})
    

@views.route("/detail/del_post", methods=["POST"])
def del_post():
    check_password = request.form["check_password"]
    post_id = request.form["post_id"]

    if check_password == gp.find(post_id)['password']:
        gp.delite(post_id)
        return jsonify({"msg": "success"})
    else:
        return jsonify({"msg": "비밀번호가 일치하지 않습니다."})

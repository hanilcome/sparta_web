// 게임추천 저장 함수
function save_post() {
    let post_title = $("#post_title").val();
    let nickname = $("#post_nickname").val();
    let password = $("#post_password").val();
    let content = $("#post_content").val();
    let image_url = $("#post_image_url").val();
    let main_url = $("#post_main_url").val();

    let formData = new FormData();
    formData.append("post_title", post_title);
    formData.append("nickname", nickname);
    formData.append("password", password);
    formData.append("content", content);
    formData.append("image_url", image_url);
    formData.append("main_url", main_url);

    fetch("/detail", { method: "POST", body: formData })
      .then((response) => response.json())
      .then((data) => {
        alert(data["msg"]);
      });
      window.location.reload();
  }

// 게임 포스트 비번확인
function check_pw(post_id) {
  let check_password = $("#check_password_" + post_id).val();
  console.log(post_id)
  let formData = new FormData();
  formData.append("check_password",check_password);
  formData.append("post_id",post_id);
  fetch("/detail/check_pw", { method: "POST", body: formData })
    .then((response) => response.json())
    .then((data) => {
      if (data["msg"] === "success") {
        window.location.href = "/detail/update" + "?post_id=" + post_id;
      } else {
        alert(data["msg"]);
      }
    });
}

// 게임 포스트 업데이트
function update_post(post_id) {
    let post_title = $("#post_title").val();
    let content = $("#post_content").val();
    let image_url = $("#post_image_url").val();
    let main_url = $("#post_main_url").val();

    let formData = new FormData();
    formData.append("post_title", post_title);
    formData.append("content", content);
    formData.append("image_url", image_url);
    formData.append("main_url", main_url);
    formData.append("post_id", post_id);


    fetch("/detail/update", { method: "POST", body: formData })
    .then((response) => response.json())
    .then((data) => {
      if (data["msg"] === "success") {
        window.location.href = "/detail"
      } 
});
}

function del_post(post_id) {
    let check_password = $("#check_password_" + post_id).val();
  
    let formData = new FormData();
    formData.append("check_password",check_password);
    formData.append("post_id",post_id);
    fetch("/detail/del_post", { method: "POST", body: formData })
      .then((response) => response.json())
      .then((data) => {
        if (data["msg"] === "success") {
          window.location.reload();
        } else {
          alert(data["msg"]);
        }
      });
  }

// 댓글 저장 함수
function save_comment(post_id) {
    let nickname = $("#myo_floatingTextarea").val();
    let comment = $("#myo_floatingTextarea").val();

    let formData = new FormData();
    formData.append("nickname", nickname);
    formData.append("comment", comment);
    formData.append("post_id", post_id);
    fetch("/create_comment", { method: "POST", body: formData })
      .then((response) => response.json())
      .then((data) => {
        alert(data["msg"]);
        window.location.reload();
      });
  }

// GamePost 오픈 클로즈 버튼함수
function open_gpbox(){
  $('#gpbox_cj').show();
}
function close_gpbox(){
  $('#gpbox_cj').hide();
}
function open_gpbox(){
  $("#gpbox_cj").toggle(); // show -> hide , hide -> show
}

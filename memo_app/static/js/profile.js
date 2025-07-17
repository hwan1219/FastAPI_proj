const updateForm = document.getElementById("updateForm");
const passwordForm = document.getElementById("passwordForm");
const goHomeBtn = document.getElementById("goHomeBtn");

// 개인정보 수정
updateForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const usernameInput = document.getElementById("username");
  const emailInput = document.getElementById("email");

  const username = usernameInput.value.trim();
  const email = emailInput.value.trim();

  // 사용자 이름은 필수, 3자 이상
  if (!username) {
    alert("아이디는 필수 입력 항목입니다.");
    usernameInput.focus();
    return;
  }

  if (username.length < 3) {
    alert("아이디는 최소 3자 이상이어야 합니다.");
    usernameInput.focus();
    return;
  }

  // 이메일이 입력된 경우, 형식이 올바른지 정규식으로 검사 (선택적)
  if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    alert("올바른 이메일 형식이 아닙니다.");
    emailInput.focus();
    return;
  }

  // 서버에 보낼 데이터 구성 (email은 있을 때만 포함)
  const updateData = { username };
  if (email) {
    updateData.email = email;
  }

  try {
    const res = await fetch("/auth/infoupdate", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(updateData),
      credentials: "include"
    });

    if (res.ok) {
      alert("회원정보가 수정되었습니다.");
      updateForm.reset();
    } else {
      const err = await res.json();
      alert("수정 실패: " + (err.detail || "서버 오류"));
    }
  } catch (err) {
    console.error("정보 수정 오류:", err);
    alert("정보 수정 중 문제가 발생했습니다.");
  }
});

// 비밀번호 변경
passwordForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const current_password = document.getElementById("current_password").value.trim();
  const new_password = document.getElementById("new_password").value.trim();

  if (!current_password || !new_password) {
    alert("현재 비밀번호와 새 비밀번호를 모두 입력해주세요.");
    return;
  }

  try {
    const res = await fetch("/auth/passwordupdate", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ current_password, new_password }),
      credentials: "include"
    });

    if (res.ok) {
      alert("비밀번호가 변경되었습니다.");
      passwordForm.reset();
    } else {
      const err = await res.json();
      alert("비밀번호 변경 실패: " + (err.detail || "서버 오류"));
    }
  } catch (err) {
    console.error("비밀번호 변경 오류:", err);
    alert("비밀번호 변경 중 문제가 발생했습니다.");
  }
});

// 메인 페이지로 이동
goHomeBtn.addEventListener("click", () => {
  location.href = "/";
});
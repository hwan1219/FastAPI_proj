const loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", async (e) => {
  e.preventDefault(); // 폼 기본 제출 막기

  const formData = new FormData(loginForm);
  const username = formData.get("username").trim();
  const password = formData.get("password").trim();

  if (!username || !password) {
    alert("아이디와 비밀번호를 모두 입력해주세요.");
    return;
  }

  try {
    const response = await fetch("/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username, password }),
      credentials: "include"
    });

    if (response.ok) {
      alert("로그인 성공!");
      location.href = "/";
    } else {
      const errorData = await response.json();
      alert("로그인 실패: " + (errorData.detail || "아이디 또는 비밀번호를 확인하세요."));
    }
  } catch (error) {
    console.error("로그인 중 오류:", error);
    alert("로그인 처리 중 오류가 발생했습니다.");
  }
});
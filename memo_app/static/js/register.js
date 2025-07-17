const registerForm = document.getElementById("registerForm");
const usernameInput = document.getElementById("username");
const passwordInput = document.getElementById("password");

registerForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = usernameInput.value.trim();
  const password = passwordInput.value;

  // 유효성 검사
  if (username.length < 3) {
    alert("아이디는 3자 이상이어야 합니다.");
    usernameInput.focus();
    return;
  }

  if (password.length < 6) {
    alert("비밀번호는 6자 이상이어야 합니다.");
    passwordInput.focus();
    return;
  }

  try {
    const res = await fetch("/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username, password })
    });

    if (res.status === 201) {
      alert("회원가입이 완료되었습니다. 로그인해주세요.");
      location.href = "/login";
    } else {
      const data = await res.json();
      alert(data.detail || "회원가입에 실패했습니다.");
    }
  } catch (err) {
    console.error("회원가입 오류:", err);
    alert("서버 오류가 발생했습니다.");
  }
});
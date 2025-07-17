const memoForm = document.getElementById("memoForm");

memoForm.addEventListener("submit", async (e) => {
  e.preventDefault(); // 폼 기본 제출 막기

  const title = memoForm.title.value.trim();
  const content = memoForm.content.value.trim();

  if (!title || !content) {
    alert("제목과 내용을 모두 입력해주세요.");
    return;
  }

  try {
    const response = await fetch("/memos", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ title, content }),
      credentials: "include"
    });

    if (response.ok) {
      alert("메모가 저장되었습니다.");
      location.href = "/"; // 저장 성공 후 메인으로 이동
    } else {
      const errorData = await response.json();
      alert("저장 실패: " + (errorData.detail || "서버 오류"));
    }
  } catch (error) {
    console.error("메모 저장 중 오류:", error);
    alert("메모 저장 중 오류가 발생했습니다.");
  }
});
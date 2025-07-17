const urlParams = new URLSearchParams(window.location.search);
const memoId = urlParams.get("id");

const form = document.getElementById("editMemoForm");
const titleInput = document.getElementById("title");
const contentInput = document.getElementById("content");
const cancelBtn = document.getElementById("cancelBtn");

if (!memoId) {
  alert("잘못된 접근입니다.");
  location.href = "/";
}

// 기존 메모 불러오기
fetch(`/memos/${memoId}`, {
  credentials: "include"
})
  .then(res => {
    if (!res.ok) throw new Error("불러오기 실패");
    return res.json();
  })
  .then(memo => {
    titleInput.value = memo.title;
    contentInput.value = memo.content;
  })
  .catch(err => {
    alert("메모를 불러오지 못했습니다.");
    console.error(err);
    location.href = "/";
  });

// 수정 요청
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const updatedTitle = titleInput.value.trim();
  const updatedContent = contentInput.value.trim();

  if (!updatedTitle || !updatedContent) {
    alert("제목과 내용을 모두 입력해주세요.");
    return;
  }

  try {
    const res = await fetch(`/memos/${memoId}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: updatedTitle,
        content: updatedContent
      }),
      credentials: "include"
    });

    if (!res.ok) {
      throw new Error("수정 실패");
    }

    // 수정 성공 시 상세페이지로 이동
    alert("메모가 수정 되었습니다.");
    location.href = `/memo_detail?id=${memoId}`;
  } catch (err) {
    alert("메모 수정 중 오류가 발생했습니다.");
    console.error(err);
  }
});

// 돌아가기
cancelBtn.addEventListener("click", () => {
  location.href = `/memo_detail.html?id=${memoId}`;
});
const urlParams = new URLSearchParams(window.location.search);
const memoId = urlParams.get("id");

const titleEl = document.getElementById("memoTitle");
const contentEl = document.getElementById("memoContent");
const editBtn = document.getElementById("editBtn");
const deleteBtn = document.getElementById("deleteBtn");
const backBtn = document.getElementById("backBtn");

if (!memoId) {
  titleEl.textContent = "잘못된 접근입니다.";
} else {
  fetch(`/memos/${memoId}`, {
    credentials: "include"
  })
    .then(res => {
      if (!res.ok) throw new Error("조회 실패");
      return res.json();
    })
    .then(memo => {
      titleEl.textContent = memo.title;
      contentEl.textContent = memo.content;
    })
    .catch(err => {
      titleEl.textContent = "메모를 불러오는 데 실패했습니다.";
      console.error(err);
    });
}

// 메모 수정
editBtn.addEventListener("click", () => {
  location.href = `/memo_edit?id=${memoId}`;
});

// 메모 삭제
deleteBtn.addEventListener("click", async () => {
  const confirmed = confirm("정말 삭제하시겠습니까?");
  if (!confirmed) return;

  try {
    const res = await fetch(`/memos/${memoId}`, {
      method: "DELETE",
      credentials: "include"
    });

    if (res.status === 204) {
      alert("삭제되었습니다.");
      location.href = "/";
    } else {
      alert("삭제 실패");
    }
  } catch (err) {
    alert("삭제 중 오류 발생");
    console.error(err);
  }
});

// 뒤로가기 버튼 클릭 이벤트 처리
backBtn.addEventListener("click", () => {
  location.href = "/";
});
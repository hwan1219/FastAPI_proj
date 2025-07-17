const memoList = document.getElementById("memoList");
const logoutBtn = document.getElementById("logoutBtn");
const createMemoBtn = document.getElementById("createMemoBtn");

// 메모 목록 불러오기
let currentPage = 1;
const limit = 10;
let totalCount = 0;

async function fetchTotalCount() {
  try {
    const res = await fetch("/memos/count", {
      credentials: "include"
    });
    const data = await res.json();     // ← 여기서 서버 응답(body)을 JSON으로 파싱
    totalCount = data.count;           // ← 이때 data는 { count: 숫자 } 형태라고 가정
  } catch (err) {
    console.error("전체 메모 수 불러오기 실패:", err);
  }
}

async function fetchMemos(page = 1) {
  const skip = (page - 1) * limit;

  try {
    // 전체 개수 먼저 갱신
    await fetchTotalCount();

    const res = await fetch(`/memos/?skip=${skip}&limit=${limit}`, {
      credentials: "include"
    });

    if (!res.ok) {
      throw new Error("메모 불러오기 실패");
    }

    const memos = await res.json();
    renderMemos(memos);

    renderPagination();
  } catch (err) {
    memoList.innerHTML = "<p>메모를 불러오는 중 문제가 발생했습니다.</p>";
    console.error(err);
  }
}

function renderPagination() {
  const pagination = document.getElementById("pagination");
  pagination.innerHTML = "";

  const totalPages = Math.ceil(totalCount / limit);
  const pageGroupSize = 5;

  // 현재 페이지 그룹 계산
  const currentGroup = Math.floor((currentPage - 1) / pageGroupSize);
  const groupStart = currentGroup * pageGroupSize + 1;
  const groupEnd = Math.min(groupStart + pageGroupSize - 1, totalPages);

  // 이전 그룹 버튼
  if (groupStart > 1) {
    const prevBtn = document.createElement("button");
    prevBtn.textContent = "◀ 이전";
    prevBtn.addEventListener("click", () => {
      currentPage = groupStart - 1;
      fetchMemos(currentPage);
    });
    pagination.appendChild(prevBtn);
  }

  // 페이지 번호 버튼들
  for (let i = groupStart; i <= groupEnd; i++) {
    const pageBtn = document.createElement("button");
    pageBtn.textContent = i;
    if (i === currentPage) {
      pageBtn.disabled = true;
      pageBtn.style.fontWeight = "bold";
    }
    pageBtn.addEventListener("click", () => {
      currentPage = i;
      fetchMemos(currentPage);
    });
    pagination.appendChild(pageBtn);
  }

  // 다음 그룹 버튼
  if (groupEnd < totalPages) {
    const nextBtn = document.createElement("button");
    nextBtn.textContent = "다음 ▶";
    nextBtn.addEventListener("click", () => {
      currentPage = groupEnd + 1;
      fetchMemos(currentPage);
    });
    pagination.appendChild(nextBtn);
  }
}

// 메모 렌더링 (제목만 ul > li > a 구조)
function renderMemos(memos) {
  if (memos.length === 0) {
    memoList.innerHTML = "<p>작성된 메모가 없습니다.</p>";
    return;
  }

  // ul 요소 생성 및 초기화
  const ul = document.createElement("ul");
  ul.classList.add("memo-list");

  memos.forEach((memo) => {
    const li = document.createElement("li");

    li.innerHTML = `
      <a href="/memo_detail?id=${memo.id}" class="memo-title">${memo.title}</a>
      <button class="delete-btn" data-id="${memo.id}">삭제</button>
    `;

    ul.appendChild(li);
  });

  // 기존 내용 지우고 ul 추가
  memoList.innerHTML = "";
  memoList.appendChild(ul);

  document.querySelectorAll(".delete-btn").forEach((btn) => {
    btn.addEventListener("click", async (e) => {
      e.preventDefault();
      const memoId = e.target.dataset.id;
      const ok = confirm("정말 삭제하시겠습니까?");
      if (!ok) return;

      try {
        const delRes = await fetch(`/memos/${memoId}`, {
          method: "DELETE",
          credentials: "include"
        });

        if (delRes.status === 204) {
          fetchMemos(); // 삭제 후 목록 갱신
        } else {
          alert("삭제 실패");
        }
      } catch (err) {
        alert("삭제 중 오류 발생");
        console.error(err);
      }
    });
  });
}

// 새 메모 작성 페이지로 이동
createMemoBtn.addEventListener("click", () => {
  location.href = "/new_memo";
});

// 로그아웃 처리
logoutBtn.addEventListener("click", async () => {
  try {
    const res = await fetch("/auth/logout", {
      method: "POST",
      credentials: "include"
    });

    if (res.ok) {
      location.href = "/login";
    } else {
      alert("로그아웃에 실패했습니다.");
    }
  } catch (err) {
    console.error("로그아웃 실패:", err);
  }
});

// 회원 탈퇴
const deleteBtn = document.getElementById("deleteAccountBtn");

deleteBtn.addEventListener("click", async () => {
  const ok = confirm("정말 회원 탈퇴 하시겠습니까? 이 작업은 되돌릴 수 없습니다.");
  if (!ok) return;

  try {
    const res = await fetch("/auth/delete", {
      method: "DELETE",
      credentials: "include"
    });

    if (res.ok) {
      alert("회원 탈퇴가 완료되었습니다.");
      location.href = "/login";  // 탈퇴 후 로그인 페이지 이동
    } else {
      alert("회원 탈퇴에 실패했습니다.");
    }
  } catch (err) {
    alert("회원 탈퇴 중 오류가 발생했습니다.");
    console.error(err);
  }
});

// 초기 실행
fetchMemos();
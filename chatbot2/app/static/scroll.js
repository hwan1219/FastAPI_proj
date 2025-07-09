// 새 메시지 입력 시 스크롤 하단 이동

window.addEventListener('DOMContentLoaded', function() {
  const chatBox = document.getElementById('chat-box');
  chatBox.scrollTop = chatBox.scrollHeight;
});
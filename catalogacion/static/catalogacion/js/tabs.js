function showTab(tabId, el) {
    document.querySelectorAll('.tab-content').forEach(div => div.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(btn => btn.classList.remove('active'));
    document.getElementById(tabId).classList.add('active');
    el.classList.add('active');
}
function hideAll() {
    document.querySelectorAll('.tab-content').forEach(div => div.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(btn => btn.classList.remove('active'));
}
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}
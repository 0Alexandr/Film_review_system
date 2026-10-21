// Текущий год в подвале страницы.
const yearElement = document.getElementById("current-year");

if (yearElement) {
  yearElement.textContent = new Date().getFullYear();
}

// Подсветка пункта меню текущего раздела: выбирается ссылка с самым
// длинным совпадающим адресом (/reviews/statistics/ важнее /reviews/).
const currentPath = window.location.pathname;
let activeLink = null;
let activeLength = 0;

document.querySelectorAll(".site-header .nav-link").forEach((link) => {
  const linkPath = new URL(link.href).pathname;
  const matches = linkPath === "/"
    ? currentPath === "/"
    : currentPath.startsWith(linkPath);
  if (matches && linkPath.length > activeLength) {
    activeLink = link;
    activeLength = linkPath.length;
  }
});

if (activeLink) {
  activeLink.classList.add("active");
}

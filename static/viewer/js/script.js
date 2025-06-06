const menuAction = (action) => {
  console.log(action + ' from function');
};

const dropdowns = Array.from(document.querySelectorAll('.dropdown'));

dropdowns.forEach(dropdown => {
  dropdown.addEventListener('click', (e) => {
    if (e.target.classList.contains('dropdown-title')) {
      dropdown.querySelector('ul').classList.toggle('hidden');
    }
  });
});

const lis = Array.from(document.querySelectorAll('.dropdown ul li'));
lis.forEach(li => {
  li.addEventListener('click', () => {
    menuAction(li.dataset.action);
  });
});

document.addEventListener('click', (event) => {
  dropdowns.forEach(dropdown => {
    if (!dropdown.contains(event.target)) {
      dropdown.querySelector('ul').classList.add('hidden');
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("myModal");
  const closeBtn = modal?.querySelector(".close");

  closeBtn?.addEventListener("click", function () {
    modal.classList.remove("visible");
    document.body.classList.remove("modal-open");
  });
});

document.addEventListener("DOMContentLoaded", function () {
  const closeBtn = document.getElementById("modal-close");
  const redirectUrl = closeBtn.getAttribute("data-redirect-url");

  closeBtn.addEventListener("click", function () {
    window.location.href = redirectUrl;
  });
});
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
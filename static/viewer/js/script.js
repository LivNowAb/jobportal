//dropdown:

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


// modal:

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

// validation:

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("responseForm");
  if (!form) return;

  const fullnameInput = document.getElementById('fullname');
  const errorMsg = document.getElementById('fullnameError');
  const emailInput = document.getElementById('email');
  const emailError = document.getElementById('emailError');
  const msgInput = document.getElementById('message');
  const msgError = document.getElementById('msgError');
  const cvInput = document.getElementById('cv');
  const cvError = document.getElementById('cvError');

  function validateFullname() {
    const value = fullnameInput.value.trim();
    errorMsg.textContent = '';

    fullnameInput.classList.remove('error-message');

    if (value.length > 100) {
      errorMsg.textContent = 'Jméno a příjmení nesmí přesáhnout 100 znaků';
      fullnameInput.classList.add('error-message');
      return false;
    }

    if (value.length < 5) {
      errorMsg.textContent = 'Zadejte skutečné jméno a příjmení';
      fullnameInput.classList.add('error-message');
      return false;
    }

    if (!value.includes(' ')) {
      errorMsg.textContent = 'Zadejte jméno a příjmení oddělené mezerou.'
      fullnameInput.classList.add('error-message');
      return false;
    }

    const validFullname = /^[A-Za-zÁÉÍÓÚÝČĎĚŇŘŠŤŽáéíóúýčďěňřšťž]+([ -][A-Za-zÁÉÍÓÚÝČĎĚŇŘŠŤŽáéíóúýčďěňřšťž]+)*$/u;

    if (!validFullname.test(value)) {
      errorMsg.textContent = 'Jméno a příjmení mohou obsahovat pouze písmena, mezery a pomlčky.';
      fullnameInput.classList.add('error-message');
      return false;
    }

    return true;
  }

  function validateEmail() {
    const value = emailInput.value.trim();
    emailError.textContent = '';
    emailInput.classList.remove('error-message');

    const validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
    if (!validEmail.test(value)) {
      emailError.textContent = 'Zadejte platnou e-mailovou adresu.';
      emailInput.classList.add('error-message');
      return false;
    }

    return true;
  }

  function validateMsg() {
    const value = msgInput.value.trim();
    msgError.textContent = '';
    msgInput.classList.remove('error-message');


    if (value.length < 30) {
      msgError.textContent = 'Zpráva musí mít alespoň 30 znaků';
      msgInput.classList.add('error-message');
      return false;
    }

    return true;
  }

  function validateCv() {
    cvError.textContent = '';
    cvInput.classList.remove('error-message');

    if (!cvInput.files || cvInput.files.length === 0) {
      return true;
    }

  const file = cvInput.files[0];
  const allowedTypes = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'image/jpeg',
    'image/png'
  ];

  if (!allowedTypes.includes(file.type)) {
    cvError.textContent = "Nepodporovaný formát. Povolené formáty: PDF, DOC, DOCX, JPG, PNG."
    cvInput.classList.add('error-message');
    return false;
  }

  const maxSize = 10 * 1024 * 1024;
  if (file.size > maxSize) {
    cvError.textContent = "Soubor je příliš velký (max. 10 MB).";
    cvInput.classList.add('error-message');
    return false;
  }

  return true;
}

  fullnameInput.addEventListener('blur', validateFullname);
  emailInput.addEventListener('blur', validateEmail);
  msgInput.addEventListener('blur', validateMsg);
  cvInput.addEventListener('blur', validateCv);

  form.addEventListener("submit", function (event) {
    const isFullnameValid = validateFullname();
    const isEmailValid = validateEmail();
    const isMsgValid = validateMsg();
    const isCvValid = validateCv();

    if (!isFullnameValid || !isEmailValid || !isMsgValid || !isCvValid) {
      event.preventDefault();
    }

  });
});


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

// filters

document.addEventListener('DOMContentLoaded', function () {
    const regionSelect = document.getElementById('region');
    const districtSelect = document.getElementById('district');
    const allDistrictOptions = Array.from(districtSelect.options).slice(1);

    function filterDistrictByRegion(regionId) {
        districtSelect.innerHTML = `<option value="">-- Vyberte okres --</option>`;
        if (!regionId) return;

        const filteredOptions = allDistrictOptions.filter(
            option => option.dataset.region === regionId
        );
        filteredOptions.forEach(option => districtSelect.appendChild(option));
    }

    regionSelect.addEventListener('change', function () {
        filterDistrictByRegion(this.value);
    });
    const selectedRegion = regionSelect.value;
    if (selectedRegion) {
        filterDistrictByRegion(selectedRegion);
    }
});

// show only active ads (14 days)

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.ad-item').forEach(ad => {
        const createdStr = ad.dataset.created;
        const createdDate = new Date(createdStr);
        const today = new Date();
        const diff = (today - createdDate) / (1000 * 60 * 60 * 24);

        if (diff > 5) {
            ad.classList.add('inactive');
            const status = ad.querySelector('.status');
            if (status) {
                status.textContent = " (Neaktivní)";
            }
        }
    });
});

// text content - show more

document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".read-more").forEach(span => {
        span.addEventListener('click', function () {
            const container = this.parentElement;
            const fullText = container.dataset.full;
            container.innerHTML = fullText;
        });
    });
});


// hamburger

function toggleMenu() {
    const menu = document.getElementById('nav-menu');
    menu.classList.toggle('show');
}


// payment

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("paymentForm");

    form.addEventListener("submit", function (event) {
        let isValid = true;
        let messages = [];

        const cardNumber = form.querySelector('input[name="card_number"]');
        const cardholderName = form.querySelector('input[name="cardholder_name"]');
        const expiryDate = form.querySelector('input[name="expiry_date"]');
        const cvv = form.querySelector('input[name="cvv"]');


        form.querySelectorAll('.form-error').forEach(el => el.remove());


        const cardRegex = /^\d{16}$/;
        if (!cardRegex.test(cardNumber.value.replace(/\s/g, ''))) {
            showError(cardNumber, "Zadejte platné číslo karty (16 číslic)");
            isValid = false;
        }


        if (cardholderName.value.trim().length < 2) {
            showError(cardholderName, "Zadejte jméno držitele karty");
            isValid = false;
        }

        const expiryRegex = /^(0[1-9]|1[0-2])\/\d{2}$/;
        if (!expiryRegex.test(expiryDate.value)) {
            showError(expiryDate, "Zadejte datum ve formátu MM/YY");
            isValid = false;
        } else {
            const [monthStr, yearStr] = expiryDate.value.split("/");
            const month = parseInt(monthStr, 10);
            const year = parseInt("20" + yearStr, 10);

            const now = new Date();
            const currentMonth = now.getMonth() + 1;
            const currentYear = now.getFullYear();

            if (year < currentYear || (year === currentYear && month < currentMonth)) {
                showError(expiryDate, "Karta již expirovala");
                isValid = false;
            }
        }


        const cvvRegex = /^\d{3}$/;
        if (!cvvRegex.test(cvv.value)) {
            showError(cvv, "Zadejte CVC kód (3 číslice)");
            isValid = false;
        }

        if (!isValid) {
            event.preventDefault();
        }

        function showError(input, message) {
            const error = document.createElement("div");
            error.className = "form-error";
            error.style.color = "red";
            error.style.fontSize = "0.9em";
            error.textContent = message;
            input.parentNode.appendChild(error);
        }
    });
});
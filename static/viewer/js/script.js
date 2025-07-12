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
    const closeBtn = document.getElementById("modal-close");

    if (closeBtn) {
        closeBtn.addEventListener("click", function () {
            const redirectUrl = closeBtn.dataset.next || "/";
            window.location.href = redirectUrl;
        });
    }
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
        districtSelect.innerHTML = `<option value="">-- Vyberte okres --</option>`; //reset when region changed
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
        const publishedStr = ad.dataset.published;
        const publishedDate = new Date(publishedStr);
        const today = new Date();
        const diff = (today - publishedDate) / (1000 * 60 * 60 * 24);

        if (diff > 14) {
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
            container.innerHTML = container.dataset.full;
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
            showError(expiryDate, "Zadejte datum ve formátu MM/RR");
            isValid = false;
        }

        if (expiryRegex.test(expiryDate.value)) {
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
            error.textContent = message;
            input.parentNode.appendChild(error);
        }
    });
});

// registration validation

document.addEventListener("DOMContentLoaded", function () {
    const fields = {
        username: document.getElementById("id_username"),
        email: document.getElementById("id_email"),
        password1: document.getElementById("id_password1"),
        password2: document.getElementById("id_password2"),
        business_name: document.getElementById("id_business_name"),
        business_type: document.getElementById("id_business_type"),
        vat: document.getElementById("id_VAT_number"),
        address: document.getElementById("id_address"),
        city: document.getElementById("id_city"),
        district: document.getElementById("id_district"),
        contact_email: document.getElementById("id_contact_email"),
        phone: document.getElementById("id_contact_phone"),
        logo: document.getElementById("id_logo")
    };

    function showError(input, message) {
        removeError(input);
        const error = document.createElement("div");
        error.className = "form-error";
        error.textContent = message;
        input.parentNode.appendChild(error);
    }

    function removeError(input) {
        const existing = input.parentNode.querySelector(".form-error");
        if (existing) {
            existing.remove();
        }
    }

    fields.username.addEventListener("blur", function () {
        const val = this.value.trim();
        const usernameRegex = /^[\w.@+-]{4,150}$/;
        if (!val) {
            showError(this, "Uživatelské jméno je povinné.");
        } else if (!usernameRegex.test(val)) {
            showError(this, "Povoleno: písmena, čísla a znaky @/./+/-/_, celkem alespoň 4 znaky.");
            return;
        }
        removeError(this);
    });

    fields.email.addEventListener("blur", function () {
        const val = this.value.trim();
        const emailRegex = /^\S+@\S+\.\S+$/;
        if (!val || !emailRegex.test(val)) {
            showError(this, "Zadejte platný e-mail.");
            return;
        }
        removeError(this);
    });

    fields.password1.addEventListener("blur", function () {
        const val = this.value;
        if (val.length < 8) {
            showError(this, "Heslo musí mít alespoň 8 znaků.");
            return;
        }
        if (/^\d+$/.test(val)) {
            showError(this, "Heslo nesmí být pouze čísla.");
            return;
        }
        removeError(this);
    });

    fields.password2.addEventListener("blur", function () {
        if (this.value !== fields.password1.value) {
            showError(this, "Hesla se neshodují.");
            return;
        }
        removeError(this);
    });

    fields.business_name.addEventListener("blur", function () {
        if (!this.value.trim()) {
            showError(this, "Zadejte název podniku.");
            return;
        }
        removeError(this);
    });

    fields.business_type.addEventListener("blur", function () {
        if (!this.value || this.value === "") {
            showError(this, "Vyberte typ provozovny.");
            return;
        }
        removeError(this);
    });

    fields.vat.addEventListener("blur", function () {
        const val = this.value.trim().toUpperCase();

        const icoRegex = /^\d{8}$/;
        const dicRegex = /^CZ\d{8,10}$/;

        if (!val) {
            showError(this, "Zadejte alespoň IČO nebo DIČ.");
            return;
        }

        if (!icoRegex.test(val) && !dicRegex.test(val)) {
            showError(this, "Zadejte platné IČO (8 číslic) nebo DIČ (např. CZ12345678).");
            return;
        }

        removeError(this);

    });

    fields.address.addEventListener("blur", function () {
        if (!this.value.trim()) {
            showError(this, "Zadejte adresu.");
            return;
        }
        removeError(this);
    });

    fields.city.addEventListener("blur", function () {
        if (!this.value.trim()) {
            showError(this, "Zadejte město.");
            return;
        }
        removeError(this);
    });

    fields.district.addEventListener("blur", function () {
        if (!this.value || this.value === "") {
            showError(this, "Vyberte okres.");
            return;
        }
        removeError(this);
    });

    fields.contact_email.addEventListener("blur", function () {
        const val = this.value.trim();
        const emailRegex = /^\S+@\S+\.\S+$/;
        if (!val || !emailRegex.test(val)) {
            showError(this, "Zadejte platný kontaktní e-mail.");
            return;
        }
        removeError(this);

    });

    fields.phone.addEventListener("blur", function () {
        const val = this.value.trim();
        if (!/^\d{9,15}$/.test(val)) {
            showError(this, "Zadejte platné telefonní číslo (9–15 číslic).");
            return;
        }
        removeError(this);
    });

    fields.logo.addEventListener("change", function () {
        removeError(this);
        const file = this.files[0];

        if (!file) return; // logo není povinné

        const allowedTypes = ["image/jpeg", "image/png", "image/webp", "image/svg+xml"];

        if (!allowedTypes.includes(file.type)) {
            showError(this, "Povolené formáty loga jsou JPG, PNG, WebP nebo SVG.");
            return;
        }
        removeError(this);
    });

    const form = document.querySelector("form");

    form.addEventListener("submit", function (e) {
        let isValid = true;


        Object.keys(fields).forEach((key) => {
            const input = fields[key];
            input.dispatchEvent(new Event("blur"));
            const error = input.parentNode.querySelector(".form-error");
            if (error) {
                isValid = false;
            }
        });

        if (!isValid) {
            e.preventDefault();
        }
    });

});

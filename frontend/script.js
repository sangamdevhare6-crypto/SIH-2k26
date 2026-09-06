/* VARSHA KRITRIMA BUDHHIH - Django-backed authentication. */

const roles = {
    citizen: {
        title: 'Citizen Login',
        welcome: 'Welcome Citizen!',
        icon: '👥',
        desc: 'Access rainfall alerts, safe routes and weather updates.',
        features: [
            '🌧️ Live Rainfall Alerts',
            '📍 Safety & Route Guidance',
            '🌊 Inundation Updates',
            '☁️ Weather Forecast'
        ],
        color: 'linear-gradient(100deg,#12a8ed,#167ff0)'
    },

    admin: {
        title: 'Administrator Login',
        welcome: 'Welcome Administrator!',
        icon: '⚙️',
        desc: 'Manage users, monitoring sources, configuration and system access.',
        features: [
            '👥 User Management',
            '⚙️ System Configuration',
            '📡 Data Sources',
            '🔐 Audit & Access Control'
        ],
        color: 'linear-gradient(100deg,#7b61e8,#5367e8)'
    }
};


const params = new URLSearchParams(location.search);
const role = params.get('role');


if (role && roles[role]) {

    const c = roles[role];

    const set = (id, value) => {

        const element = document.getElementById(id);

        if (element) {
            element.textContent = value;
        }
    };

    set('roleTitle', c.title);
    set('welcome', c.welcome);
    set('roleIcon', c.icon);
    set('roleDesc', c.desc);

    const button = document.getElementById('roleButton');

    if (button) {
        button.style.background = c.color;
    }

    const features = document.getElementById('roleFeatures');

    if (features) {

        features.innerHTML = c.features
            .map(x => `<div>${x}</div>`)
            .join('');
    }
}


async function api(path, payload) {

    const response = await fetch(path, {
        method: 'POST',

        headers: {
            'Content-Type': 'application/json'
        },

        body: JSON.stringify(payload)
    });

    let data = {};

    try {
        data = await response.json();
    } catch {}

    if (!response.ok) {

        throw new Error(
            data.message || 'Request failed.'
        );
    }

    return data;
}


/* ===============================
   LOGIN REDIRECT
   =============================== */

function redirectToDashboard(role) {

    if (role === 'admin') {

        location.href = 'admin-dashboard.html';

    } else if (role === 'citizen') {

        location.href = 'authority-dashboard.html';

    } else {

        location.href = 'authority-dashboard.html';
    }
}


/* ===============================
   CREATE ACCOUNT
   =============================== */

async function createAccount(event) {

    event.preventDefault();

    const form = event.target;

    const inputs = form.querySelectorAll('input');

    const roleSelect = form.querySelector('select');

    const selectedRole = roleSelect
        ? roleSelect.value
        : 'citizen';


    const data = {

        fullName: inputs[0]
            ? inputs[0].value.trim()
            : '',

        email: inputs[1]
            ? inputs[1].value.trim().toLowerCase()
            : '',

        mobile: inputs[2]
            ? inputs[2].value.trim()
            : '',

        password: inputs[3]
            ? inputs[3].value
            : '',

        confirm: inputs[4]
            ? inputs[4].value
            : '',

        role: selectedRole
    };


    if (data.password !== data.confirm) {

        return alert(
            'Passwords do not match.'
        );
    }


    if (data.password.length < 6) {

        return alert(
            'Password must contain at least 6 characters.'
        );
    }


    try {

        await api(
            '/api/signup/',
            data
        );

        alert(
            'Account created successfully! Please login.'
        );

        location.href =
            `role-login.html?role=${selectedRole}`;

    } catch (error) {

        alert(error.message);
    }
}


/* ===============================
   NORMAL LOGIN
   =============================== */

async function login(event) {

    event.preventDefault();

    const form = event.target;

    try {

        const emailInput =
            form.querySelector('input[type=email]');

        const passwordInput =
            form.querySelector('input[type=password]');


        const data = await api(
            '/api/login/',
            {

                email: emailInput
                    ? emailInput.value.trim().toLowerCase()
                    : '',

                password: passwordInput
                    ? passwordInput.value
                    : ''
            }
        );


        redirectToDashboard(
            data.user.role
        );

    } catch (error) {

        alert(error.message);
    }
}


/* ===============================
   ROLE LOGIN
   =============================== */

async function roleLogin(event) {

    event.preventDefault();

    const form = event.target;

    try {

        const emailInput =
            form.querySelector('input[type=email]');

        const passwordInput =
            form.querySelector('input[type=password]');


        const data = await api(
            '/api/login/',
            {

                email: emailInput
                    ? emailInput.value.trim().toLowerCase()
                    : '',

                password: passwordInput
                    ? passwordInput.value
                    : ''
            }
        );


        if (
            role &&
            data.user.role !== role
        ) {

            return alert(
                `This account is registered as ${data.user.role}.`
            );
        }


        redirectToDashboard(
            data.user.role
        );

    } catch (error) {

        alert(error.message);
    }
}


/* ===============================
   RESET PASSWORD
   =============================== */

async function resetPassword(event) {

    event.preventDefault();

    const newPassword =
        document.getElementById('newPassword').value;

    const confirmPassword =
        document.getElementById('confirmNewPassword').value;


    if (newPassword !== confirmPassword) {

        return alert(
            'Passwords do not match.'
        );
    }


    try {

        await api(
            '/api/reset-password/',
            {

                email: document
                    .getElementById('resetEmail')
                    .value
                    .trim()
                    .toLowerCase(),

                newPassword: newPassword
            }
        );


        alert(
            'Password reset successfully. Please login again.'
        );


        location.href =
            'role-login.html';

    } catch (error) {

        alert(error.message);
    }
}


/* ===============================
   LOGOUT
   =============================== */

async function logout() {

    try {

        await api(
            '/api/logout/',
            {}
        );

    } finally {

        location.href =
            'index.html';
    }
}


/* ===============================
   DASHBOARD PROTECTION
   =============================== */

async function protectDashboard(requiredRole) {

    try {

        const response =
            await fetch('/api/me/');


        if (!response.ok) {

            throw 0;
        }


        const data =
            await response.json();


        const user =
            data.user;


        if (
            requiredRole &&
            user.role !== requiredRole
        ) {

            return redirectToDashboard(
                user.role
            );
        }


        let id;


        if (requiredRole === 'admin') {

            id = 'adminName';

        } else {

            id = 'citizenName';
        }


        const element =
            document.getElementById(id);


        if (element) {

            element.textContent =
                user.name;
        }


        return user;

    } catch {

        alert(
            'Please login first.'
        );

        location.href =
            'index.html';
    }
}


/* ===============================
   OLD DASHBOARD PROTECTION
   =============================== */

if (
    document.body.classList.contains(
        'dashboard-page'
    )
) {

    const isAdmin =
        document.title
            .toLowerCase()
            .includes('administrator');


    protectDashboard(
        isAdmin
            ? 'admin'
            : 'citizen'
    );
}


/* ===============================
   AUTHORITY DASHBOARD PROTECTION
   =============================== */

if (
    document.body.classList.contains(
        'authority-page'
    )
) {

    protectDashboard('citizen')
        .then(user => {

            if (!user) {
                return;
            }


            const name =
                document.getElementById(
                    'profileName'
                );


            const email =
                document.getElementById(
                    'profileEmail'
                );


            const emailInput =
                document.getElementById(
                    'profileEmailInput'
                );


            const fullName =
                document.getElementById(
                    'profileFullName'
                );


            if (name) {

                name.textContent =
                    user.name;
            }


            if (email) {

                email.textContent =
                    user.email;
            }


            if (emailInput) {

                emailInput.value =
                    user.email;
            }


            if (fullName) {

                fullName.value =
                    user.name;
            }


            const avatar =
                document.querySelector(
                    '.user-avatar'
                );


            if (avatar) {

                avatar.textContent =
                    (user.name || 'A')
                        .charAt(0)
                        .toUpperCase();
            }

        });
}


/* ===============================
   ADMIN SIDEBAR PAGES
   =============================== */

if (
    document.body.classList.contains(
        'admin-page'
    )
) {

    protectDashboard('admin')
        .then(user => {

            if (!user) {
                return;
            }


            const name =
                document.getElementById(
                    'profileName'
                );


            const email =
                document.getElementById(
                    'profileEmail'
                );


            const emailInput =
                document.getElementById(
                    'profileEmailInput'
                );


            const fullName =
                document.getElementById(
                    'profileFullName'
                );


            if (name) {

                name.textContent =
                    user.name;
            }


            if (email) {

                email.textContent =
                    user.email;
            }


            if (emailInput) {

                emailInput.value =
                    user.email;
            }


            if (fullName) {

                fullName.value =
                    user.name;
            }


            const avatar =
                document.querySelector(
                    '.user-avatar'
                );


            if (avatar) {

                avatar.textContent =
                    (user.name || 'A')
                        .charAt(0)
                        .toUpperCase();
            }

        });
}


/* ===============================
   ALERT MANAGEMENT
   =============================== */

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const typeFilter =
            document.getElementById(
                "alertTypeFilter"
            );


        const riskFilter =
            document.getElementById(
                "riskFilter"
            );


        const statusFilter =
            document.getElementById(
                "statusFilter"
            );


        const filterBtn =
            document.getElementById(
                "filterBtn"
            );


        const clearBtn =
            document.getElementById(
                "clearFilters"
            );


        const rows =
            document.querySelectorAll(
                "#alertsTableBody tr"
            );


        const countText =
            document.getElementById(
                "alertsCount"
            );


        const footerText =
            document.getElementById(
                "footerText"
            );


        function applyFilters() {

            if (
                !typeFilter ||
                !riskFilter ||
                !statusFilter
            ) {

                return;
            }


            const type =
                typeFilter.value;


            const risk =
                riskFilter.value;


            const status =
                statusFilter.value;


            let visible = 0;


            rows.forEach(function (row) {

                const rowType =
                    row.dataset.type;


                const rowRisk =
                    row.dataset.risk;


                const rowStatus =
                    row.dataset.status;


                const typeMatch =
                    type === "all" ||
                    rowType === type;


                const riskMatch =
                    risk === "all" ||
                    rowRisk === risk;


                const statusMatch =
                    status === "all" ||
                    rowStatus === status;


                if (
                    typeMatch &&
                    riskMatch &&
                    statusMatch
                ) {

                    row.style.display = "";

                    visible++;

                } else {

                    row.style.display =
                        "none";
                }

            });


            if (countText) {

                countText.textContent =
                    "Showing " +
                    visible +
                    " alerts";
            }


            if (footerText) {

                footerText.textContent =
                    "Showing 1 to " +
                    visible +
                    " of 78 alerts";
            }
        }


        if (filterBtn) {

            filterBtn.addEventListener(
                "click",
                applyFilters
            );
        }


        if (typeFilter) {

            typeFilter.addEventListener(
                "change",
                applyFilters
            );
        }


        if (riskFilter) {

            riskFilter.addEventListener(
                "change",
                applyFilters
            );
        }


        if (statusFilter) {

            statusFilter.addEventListener(
                "change",
                applyFilters
            );
        }


        if (clearBtn) {

            clearBtn.addEventListener(
                "click",
                function () {

                    if (typeFilter) {
                        typeFilter.value = "all";
                    }

                    if (riskFilter) {
                        riskFilter.value = "all";
                    }

                    if (statusFilter) {
                        statusFilter.value = "all";
                    }

                    applyFilters();
                }
            );
        }


        document
            .querySelectorAll(".view-alert")
            .forEach(function (button) {

                button.addEventListener(
                    "click",
                    function () {

                        const row =
                            button.closest("tr");


                        if (!row) {
                            return;
                        }


                        const alertNameElement =
                            row.querySelector(
                                ".alert-name strong"
                            );


                        const alertName =
                            alertNameElement
                                ? alertNameElement.textContent
                                : "Unknown Alert";


                        alert(
                            "Alert Details:\n" +
                            alertName
                        );
                    }
                );
            });


        const notificationBtn =
            document.getElementById(
                "notificationBtn"
            );


        if (notificationBtn) {

            notificationBtn.addEventListener(
                "click",
                function () {

                    alert(
                        "You have new alerts."
                    );
                }
            );
        }

    }
);
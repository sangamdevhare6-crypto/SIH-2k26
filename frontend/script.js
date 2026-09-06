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


function redirectToDashboard(role) {

    location.href =
        role === 'admin'
            ? 'admin-dashboard.html'
            : 'citizen-dashboard.html';
}


async function createAccount(event) {

    event.preventDefault();

    const form = event.target;

    const inputs = form.querySelectorAll('input');

    const role = form
        .querySelector('select')
        .value;

    const data = {

        fullName: inputs[0].value.trim(),

        email: inputs[1]
            .value
            .trim()
            .toLowerCase(),

        mobile: inputs[2]
            .value
            .trim(),

        password: inputs[3].value,

        confirm: inputs[4].value,

        role: role
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
            `role-login.html?role=${role}`;

    } catch (error) {

        alert(error.message);
    }
}


async function login(event) {

    event.preventDefault();

    const form = event.target;

    try {

        const data = await api(
            '/api/login/',
            {
                email: form
                    .querySelector('input[type=email]')
                    .value
                    .trim()
                    .toLowerCase(),

                password: form
                    .querySelector('input[type=password]')
                    .value
            }
        );

        redirectToDashboard(
            data.user.role
        );

    } catch (error) {

        alert(error.message);
    }
}


async function roleLogin(event) {

    event.preventDefault();

    const form = event.target;

    try {

        const data = await api(
            '/api/login/',
            {
                email: form
                    .querySelector('input[type=email]')
                    .value
                    .trim()
                    .toLowerCase(),

                password: form
                    .querySelector('input[type=password]')
                    .value
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

        const id =
            requiredRole === 'admin'
                ? 'adminName'
                : 'citizenName';

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


/* Shared protection for the administrator sidebar pages. */

if (
    document.body.classList.contains(
        'admin-page'
    )
) {

    protectDashboard('admin')
        .then(user => {

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
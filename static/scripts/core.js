const themeButton = document.querySelector('#theme-button');
const themeModal = document.querySelector('.customize-theme');
const fontSize = document.querySelectorAll('.choose-size span');
const colorPalette = document.querySelectorAll('.choose-color span');
const Bg1 = document.querySelector('.bg-1');
const Bg2 = document.querySelector('.bg-2');
const Bg3 = document.querySelector('.bg-3');

const root = document.querySelector(':root');

document.addEventListener('DOMContentLoaded', () => {
    fetchThemePreferences()
        .then(() => {
            document.body.style.display = 'block';
        });
});

// Function for loading theme preference
function fetchThemePreferences() {
    return fetch('/accounts/get-theme-preferences/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Bad response: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            applyThemePreferences(data);
        })
        .catch(error => {
            console.error('Failed to retrieve theme preferences: ', error);
        });
}

// Applying the received theme settings
function applyThemePreferences(data) {
    console.log('Received theme preferences:', data);

    root.style.fontSize = data.font_size;
    root.style.setProperty('--primary-color-hue', data.primary_color);

    const theme = data.theme;
    let lightColorLightness, whiteColorLightness, darkColorLightness;
    
    if (theme === "light") {
        lightColorLightness = '95%';
        whiteColorLightness = '100%';
        darkColorLightness = '0%';
    } else if (theme === "dim") {
        lightColorLightness = '15%';
        whiteColorLightness = '20%';
        darkColorLightness = '95%';
    } else if (theme === "dark") {
        lightColorLightness = '0%';
        whiteColorLightness = '10%';
        darkColorLightness = '95%';
    }

    root.style.setProperty('--light-color-lightness', lightColorLightness);
    root.style.setProperty('--white-color-lightness', whiteColorLightness);
    root.style.setProperty('--dark-color-lightness', darkColorLightness);

    console.log('Applied color lightness settings:', {
        lightColorLightness,
        whiteColorLightness,
        darkColorLightness
    });
    
    document.querySelectorAll('.choose-bg div').forEach(div => div.classList.remove('active'));
    const activeBg = document.querySelector(`.bg-${theme === "light" ? 1 : theme === "dim" ? 2 : 3}`);
    if (activeBg) {
        activeBg.classList.add('active');
    } else {
        console.error('No background active element found for theme: ' + theme);
    }
}

// Opens Modal
function openThemeModal() {
    themeModal.style.display = 'grid';
}

function closeThemeModal(e) {
    if (e.target.classList.contains('customize-theme')) {
        themeModal.style.display = 'none';
    }
}

themeButton.addEventListener('click', openThemeModal);
themeModal.addEventListener('click', closeThemeModal);

// Remove active class from spans or font size selectors
function removeSizeSelectors() {
    fontSize.forEach(size => {
        size.classList.remove('active');
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }

    return cookieValue;
}

// Send theme preferences to the server
function sendThemePreferences() {
    const activeBg = document.querySelector('.choose-bg .active');
    const theme = activeBg ? activeBg.dataset.theme : '';
    const fontSize = root.style.fontSize;
    const primaryColor = getComputedStyle(root).getPropertyValue('--primary-color-hue');
    const csrftoken = getCookie('csrftoken');

    fetch('/accounts/save-theme-preferences/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            theme: theme,
            font_size: fontSize,
            primary_color: primaryColor
        })
    }).then(response => {
        if (response.ok) {
            console.log('Theme preferences saved successfully.');
        } else {
            console.error('Failed to save theme preferences.');
        }
    });
};

// Event handler for changing font size
fontSize.forEach(size => {
    size.addEventListener('click', () => {
        removeSizeSelectors();
        let fontSize;
        size.classList.toggle('active');

        if (size.classList.contains('font-size-1')) {
            fontSize = '10px';
            root.style.setProperty('----sticky-top-left', '5.4rem');
            root.style.setProperty('----sticky-top-right', '5.4rem');
        } else if (size.classList.contains('font-size-2')) {
            fontSize = '13px';
            root.style.setProperty('----sticky-top-left', '5.4rem');
            root.style.setProperty('----sticky-top-right', '-7rem');
        } else if (size.classList.contains('font-size-3')) {
            fontSize = '16px';
            root.style.setProperty('----sticky-top-left', '-2rem');
            root.style.setProperty('----sticky-top-right', '-17rem');
        } else if (size.classList.contains('font-size-4')) {
            fontSize = '18px';
            root.style.setProperty('----sticky-top-left', '-5rem');
            root.style.setProperty('----sticky-top-right', '-25rem');
        }

        root.style.fontSize = fontSize;
        sendThemePreferences();
    });
});

function changeActiveColor() {
    colorPalette.forEach(colorPicker => {
        colorPicker.classList.remove('active');
    });
}

colorPalette.forEach(color => {
    color.addEventListener('click', () => {
        let primaryHue;
        changeActiveColor();

        if (color.classList.contains('color-1')) {
            primaryHue = 252;
        } else if (color.classList.contains('color-2')) {
            primaryHue = 52;
        } else if (color.classList.contains('color-3')) {
            primaryHue = 352;
        } else if (color.classList.contains('color-4')) {
            primaryHue = 152;
        } else if (color.classList.contains('color-5')) {
            primaryHue = 202;
        }

        color.classList.add('active');
        root.style.setProperty('--primary-color-hue', primaryHue);
        sendThemePreferences();
    });
});

function changeBackground(lightColorLightness, whiteColorLightness, darkColorLightness) {
    root.style.setProperty('--light-color-lightness', lightColorLightness);
    root.style.setProperty('--white-color-lightness', whiteColorLightness);
    root.style.setProperty('--dark-color-lightness', darkColorLightness);
}

Bg1.addEventListener('click', () => {
    Bg1.classList.add('active');
    Bg2.classList.remove('active');
    Bg3.classList.remove('active');
    changeBackground('95%', '98%', '0%');
    sendThemePreferences();
});

Bg2.addEventListener('click', () => {
    Bg2.classList.add('active');
    Bg1.classList.remove('active');
    Bg3.classList.remove('active');
    changeBackground('15%', '20%', '95%');
    sendThemePreferences();
});

Bg3.addEventListener('click', () => {
    Bg3.classList.add('active');
    Bg1.classList.remove('active');
    Bg2.classList.remove('active');
    changeBackground('0%', '10%', '95%');
    sendThemePreferences();
});
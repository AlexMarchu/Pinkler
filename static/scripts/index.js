// Sidebar
const menuItems = document.querySelectorAll('.item');

// Theme
const theme = document.querySelector('#theme');
const themeModal = document.querySelector('.customize-theme');
const fontSize = document.querySelectorAll('.choose-size span');
var root = document.querySelector(':root');
const colorPalette = document.querySelectorAll('.choose-color span');
const Bg1 = document.querySelector('.bg-1');
const Bg2 = document.querySelector('.bg-2');
const Bg3 = document.querySelector('.bg-3');

document.addEventListener('DOMContentLoaded', () => {
    fetchThemePreferences()
        .then(() => {
            document.body.style.visibility = 'visible';
        });
});

// Function for loading theme settings
function fetchThemePreferences() {
    return fetch('/accounts/get-theme-preference/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            applyThemePreferences(data);
        })
        .catch(error => {
            console.error('Failed to retrieve theme preferences:', error);
        });
}

// Applying the received theme settings
function applyThemePreferences(data) {
    console.log('Received theme preferences:', data);

    
    document.querySelector('html').style.fontSize = data.font_size;
    document.documentElement.style.setProperty('--primary-color-hue', data.primary_color);

    const theme = data.theme;
    let lightColorLightness, whiteColorLightness, darkColorLightness;

    
    if (theme === "light") {
        lightColorLightness = '95%';
        whiteColorLightness = '98%';
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

    
    document.documentElement.style.setProperty('--light-color-lightness', lightColorLightness);
    document.documentElement.style.setProperty('--white-color-lightness', whiteColorLightness);
    document.documentElement.style.setProperty('--dark-color-lightness', darkColorLightness);

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
        console.warn('No active background element found for theme:', theme);
    }
}





// ============== THEME / DISPLAY CUSTOMIZATION ==============

// Opens Modal
const openThemeModal = () => {
    themeModal.style.display = 'grid';
}

const closeThemeModal = (e) => {
    if (e.target.classList.contains('customize-theme')) {
        themeModal.style.display = 'none';
    }
}

theme.addEventListener('click', openThemeModal);
themeModal.addEventListener('click', closeThemeModal);

// ============== FONT SIZE ==============

// remove active class from spans or font size selectors
const removeSizeSelectors = () => {
    fontSize.forEach(size => {
        size.classList.remove('active');
    });
}

// Send theme preferences to the server
const sendThemePreferences = () => {
    const activeBg = document.querySelector('.choose-bg .active');
    const theme = activeBg ? activeBg.dataset.theme : '';
    const fontSize = document.querySelector('html').style.fontSize;
    const primaryColor = getComputedStyle(document.documentElement).getPropertyValue('--primary-color-hue');

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

    const csrftoken = getCookie('csrftoken');

    fetch('/accounts/save-theme-preference/', {
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
            console.log('Theme preferences saved successfully');
        } else {
            console.error('Failed to save theme preferences');
        }
    });
};

// Обработчики событий для изменения размера шрифта
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
            fontSize = '19px';
            root.style.setProperty('----sticky-top-left', '-5rem');
            root.style.setProperty('----sticky-top-right', '-25rem');
        } else if (size.classList.contains('font-size-5')) {
            fontSize = '22px';
            root.style.setProperty('----sticky-top-left', '-12rem');
            root.style.setProperty('----sticky-top-right', '-35rem');
        }

        // Изменяем размер шрифта корневого HTML элемента
        document.querySelector('html').style.fontSize = fontSize;
        sendThemePreferences();
    });
});

const changeActiveColorClass = () => {
    colorPalette.forEach(colorPicker => {
        colorPicker.classList.remove('active');
    });
}

colorPalette.forEach(color => {
    color.addEventListener('click', () => {
        let primaryHue;
        changeActiveColorClass();

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

let lightColorLightness;
let whiteColorLightness;
let darkColorLightness;

const changeBG = () => {
    root.style.setProperty('--light-color-lightness', lightColorLightness);
    root.style.setProperty('--white-color-lightness', whiteColorLightness);
    root.style.setProperty('--dark-color-lightness', darkColorLightness);
}

Bg1.addEventListener('click', () => {
    lightColorLightness = '95%';
    whiteColorLightness = '98%';
    darkColorLightness = '0%';
    Bg1.classList.add('active');
    Bg2.classList.remove('active');
    Bg3.classList.remove('active');
    changeBG(); // Обновите светлоту
    sendThemePreferences();
});

Bg2.addEventListener('click', () => {
    darkColorLightness = '95%';
    whiteColorLightness = '20%';
    lightColorLightness = '15%';
    Bg2.classList.add('active');
    Bg1.classList.remove('active');
    Bg3.classList.remove('active');
    changeBG();
    sendThemePreferences();
});

Bg3.addEventListener('click', () => {
    darkColorLightness = '95%';
    whiteColorLightness = '10%';
    lightColorLightness = '0%';
    Bg3.classList.add('active');
    Bg1.classList.remove('active');
    Bg2.classList.remove('active');
    changeBG();
    sendThemePreferences();
});

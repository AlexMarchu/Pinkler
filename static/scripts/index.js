const theme = document.querySelector('#theme-button');
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

// Function for loading theme settings
function fetchThemePreferences() {
    return fetch('/accounts/get-theme-preference/')
        .then(response => {
            if (!response.ok) {
                throw new Error('Theme response was bad: ' + response.statusText);
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

    const themeMappings = {
        light: { lightness: ['95%', '100%', '0%'] },  // [lightColorLightness, whiteColorLightness, darkColorLightness]
        dim: { lightness: ['15%', '20%', '95%'] },
        dark: { lightness: ['0%', '10%', '95%'] },
    };

    const { lightness } = themeMappings[data.theme] || themeMappings.light; // default to light if theme not found
    root.style.setProperty('--light-color-lightness', lightness[0]);
    root.style.setProperty('--white-color-lightness', lightness[1]);
    root.style.setProperty('--dark-color-lightness', lightness[2]);

    console.log('Applied color lightness settings:', { lightness });

    document.querySelectorAll('.choose-bg div').forEach(div => div.classList.remove('active'));
    const activeBg = document.querySelector(`.bg-${data.theme === "light" ? 1 : data.theme === "dim" ? 2 : 3}`);
    if (activeBg) {
        activeBg.classList.add('active');
    } else {
        console.warn('No active background element found for theme:', data.theme);
    }
}

// Opens Modal and closes
function openThemeModal() {
    themeModal.style.display = 'grid';
}

function closeThemeModal(e) {
    if (e.target.classList.contains('customize-theme')) {
        themeModal.style.display = 'none';
    }
}

// Handle theme font size
fontSize.forEach(size => {
    size.addEventListener('click', () => {
        removeSizeSelectors();
        size.classList.toggle('active'); // Toggle active class

        const fontSizeMappings = {
            'font-size-1': '10px',
            'font-size-2': '13px',
            'font-size-3': '16px',
            'font-size-4': '18px',
        };

        const newFontSize = Object.entries(fontSizeMappings).find(([className]) => size.classList.contains(className));
        if (newFontSize) {
            root.style.fontSize = newFontSize[1];
            // Set sticky positions based on size
            const stickyPositions = {
                'font-size-1': ['5.4rem', '5.4rem'],
                'font-size-2': ['5.4rem', '-7rem'],
                'font-size-3': ['-2rem', '-17rem'],
                'font-size-4': ['-5rem', '-25rem']
            };
            const positions = stickyPositions[newFontSize[0]];
            if (positions) {
                root.style.setProperty('----sticky-top-left', positions[0]);
                root.style.setProperty('----sticky-top-right', positions[1]);
            }

            sendThemePreferences();
        }
    });
});

// Color palette handling
colorPalette.forEach(color => {
    color.addEventListener('click', () => {
        changeActiveColor();

        const primaryHueMappings = {
            'color-1': 252,
            'color-2': 52,
            'color-3': 352,
            'color-4': 152,
            'color-5': 202
        };

        const selectedColor = Object.keys(primaryHueMappings).find(classKey => color.classList.contains(classKey));
        if (selectedColor) {
            root.style.setProperty('--primary-color-hue', primaryHueMappings[selectedColor]);
            color.classList.add('active');
            sendThemePreferences();
        }
    });
});

// Background change handling
const backgrounds = {
    Bg1: { lightness: ['95%', '98%', '0%'], element: Bg1 },
    Bg2: { lightness: ['15%', '20%', '95%'], element: Bg2 },
    Bg3: { lightness: ['0%', '10%', '95%'], element: Bg3 },
};

Object.entries(backgrounds).forEach(([key, { lightness, element }]) => {
    element.addEventListener('click', () => {
        // Set active class
        Object.values(backgrounds).forEach(bg => bg.element.classList.remove('active'));
        element.classList.add('active');

        changeBackground(...lightness);
        sendThemePreferences();
    });
});

// Utility functions
function removeSizeSelectors() {
    fontSize.forEach(size => {
        size.classList.remove('active');
    });
}

function getCookie(name) {
    const cookieValue = document.cookie.split('; ').find(row => row.startsWith(name + '='));
    return cookieValue ? decodeURIComponent(cookieValue.split('=')[1]) : null;
}

// Send theme preferences to the server
function sendThemePreferences() {
    const activeBg = document.querySelector('.choose-bg .active');
    const theme = activeBg ? activeBg.dataset.theme : '';
    const fontSize = root.style.fontSize;
    const primaryColor = getComputedStyle(root).getPropertyValue('--primary-color-hue');
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
            console.log('Theme preferences saved successfully.');
        } else {
            console.error('Failed to save theme preferences.');
        }
    });
}

// Handling modal display
theme.addEventListener('click', openThemeModal);
themeModal.addEventListener('click', closeThemeModal);

document.addEventListener('DOMContentLoaded', () => {
    fetchThemePreferences().then(() => {
        document.body.style.display = 'block';
    });
});

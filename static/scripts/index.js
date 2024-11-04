// Sidebar
const menuItems = document.querySelectorAll('.item');

// Theme
const theme = document.querySelector('#theme');
const themeModal = document.querySelector('.customize-theme');
const fontSizeSelectors = document.querySelectorAll('.choose-size span');
const root = document.querySelector(':root');
const colorPalette = document.querySelectorAll('.choose-color span');
const backgrounds = document.querySelectorAll('.bg-option');

const setCssProperty = (property, value) => {
    root.style.setProperty(property, value);
}

const handleActiveClass = (elements, activeElement) => {
    elements.forEach(el => {
        el.classList.toggle('active', el === activeElement);
    });
}

// Open and close theme modal
theme.addEventListener('click', () => {
    themeModal.style.display = 'grid';
});

themeModal.addEventListener('click', (e) => {
    if (e.target.classList.contains('customize-theme')) {
        themeModal.style.display = 'none';
    }
});

// Font size customization
fontSizeSelectors.forEach(size => {
    size.addEventListener('click', () => {
        let fontSize;
        const sizeMap = {
            'font-size-1': { size: '10px', left: '5.4rem', right: '5.4rem' },
            'font-size-2': { size: '13px', left: '5.4rem', right: '-7rem' },
            'font-size-3': { size: '16px', left: '-2rem', right: '-17rem' },
            'font-size-4': { size: '19px', left: '-5rem', right: '-25rem' },
            'font-size-5': { size: '22px', left: '-12rem', right: '-35rem' },
        };

        handleActiveClass(fontSizeSelectors, size);
        const selectedSize = Object.keys(sizeMap).find(key => size.classList.contains(key));
        if (selectedSize) {
            fontSize = sizeMap[selectedSize].size;
            setCssProperty('----sticky-top-left', sizeMap[selectedSize].left);
            setCssProperty('----sticky-top-right', sizeMap[selectedSize].right);
            document.querySelector('html').style.fontSize = fontSize;
        }
    });
});

// Color customization
colorPalette.forEach(color => {
    color.addEventListener('click', () => {
        const hueMap = {
            'color-1': 252,
            'color-2': 52,
            'color-3': 352,
            'color-4': 152,
            'color-5': 202,
        };

        handleActiveClass(colorPalette, color);
        for (let className in hueMap) {
            if (color.classList.contains(className)) {
                setCssProperty('--primary-color-hue', hueMap[className]);
            }
        }
    });
});

// Background customization
backgrounds.forEach(bg => {
    bg.addEventListener('click', () => {
        handleActiveClass(backgrounds, bg);

        if (bg.classList.contains('bg-1')) {
            window.location.reload(); // Optional: Reload page for default setting
        } else if (bg.classList.contains('bg-2')) {
            setCssProperty('--light-color-lightness', '15%');
            setCssProperty('--white-color-lightness', '20%');
            setCssProperty('--dark-color-lightness', '95%');
        } else if (bg.classList.contains('bg-3')) {
            setCssProperty('--light-color-lightness', '0%');
            setCssProperty('--white-color-lightness', '10%');
            setCssProperty('--dark-color-lightness', '95%');
        }
    });
});

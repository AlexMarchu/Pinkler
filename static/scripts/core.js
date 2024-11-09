const defaultUrlItems = document.querySelectorAll('.url-item');
const content = document.querySelector('.middle');

function retrieveUrlDataAndReplaceContent(url) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const newDocument = parser.parseFromString(html, 'text/html');
            const newContent = newDocument.querySelector('.middle');

            document.title = newDocument.title;
            content.innerHTML = newContent.innerHTML;

            const scripts = newDocument.querySelectorAll('.middle script');
            scripts.forEach(script => {
                const newScript = content.createElement('script');
                newScript.textContent = script.textContent;
                newScript.src = script.src;
                content.appendChild(newScript);
            });

            const urlItems = newDocument.querySelectorAll('.middle .url-item');
            urlItems.forEach(urlItem => {
                urlItem.addEventListener('click', () => {
                    goToUrl(urlItem);
                });
            });
        })
        .catch(error => console.error(`Failed to retrieve ${url} data : `, error));
}

function goToUrl(url) {
    if (document.location.pathname == url) {
        return;
    }
    retrieveUrlDataAndReplaceContent(url);
    history.pushState({}, '', url);
}

function backToUrl(url) {
    retrieveUrlDataAndReplaceContent(url);
}

defaultUrlItems.forEach(urlItem => {
    urlItem.addEventListener('click', () => {
        goToUrl(urlItem.getAttribute('url'));
    });
});

window.addEventListener('popstate', (event) => {
    backToUrl(document.location.pathname);
});
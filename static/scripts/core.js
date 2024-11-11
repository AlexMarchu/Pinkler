const content = document.querySelector('.middle');
const globalSearchForm = document.querySelector('#global-search form');
const globalSearchInput = document.querySelector('#global-search input');

function retrieveUrlDataAndReplaceContent(url) {
    fetch(url)
        .then(response => response.text())
        .then(html => {
            const parser = new DOMParser();
            const newDocument = parser.parseFromString(html, 'text/html');
            const newContent = newDocument.querySelector('.middle');

            document.title = newDocument.title;
            content.innerHTML = newContent.innerHTML;

            const scripts = document.querySelectorAll('.middle script');
            scripts.forEach(script => {
                const newScript = content.createElement('script');
                newScript.textContent = script.textContent;
                newScript.src = script.src;
                content.appendChild(newScript);
            });

            const urlItems = document.querySelectorAll('.middle .url-item');
            urlItems.forEach(urlItem => {
                urlItem.addEventListener('click', () => {
                    goToUrl(urlItem.getAttribute('url'));
                });
            });
            setupFriendsEventListeners();
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

function acceptFriendRequestFromUser(userId) {
    console.log('User ID:', userId);

    fetch(`/friends/get-request-id/${userId}/`, {
        method: 'GET',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.request_id) {
            return fetch(`/friends/accept-request/${data.request_id}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': '{{ csrf_token }}',
                    'Content-Type': 'application/json'
                }
            });
        } else {
            throw new Error('Запрос не найден');
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.success);
            const button = document.querySelector(`.accept-friend-request-btn[user-id="${userId}"]`);
            button.textContent = 'Друзья';
            button.disabled = true;
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => console.error('Ошибка при принятии запроса:', error));
}


function rejectFriendRequestFromUser(userId) {
    console.log('reject');
}

function removeUserFromFriends(userId) {
    fetch(`/friends/remove-friend/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(data.success);
            document.querySelector(`button[user-id="${userId}"]`).closest('.friend-item').remove();
        } else {
            console.error(data.error);
        }
    })
    .catch(error => console.error('Ошибка при удалении друга:', error));
}

function addUserToFriends(userId) {
    fetch(`/friends/send-request/${userId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.success);
            const button = document.querySelector(`.add-friend-btn[user-id="${userId}"]`);
            button.textContent = 'Запрос отправлен';
            button.disabled = true;
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => console.error('Ошибка при отправке запроса:', error));
}

function cancelFriendRequestToUser(userId) {
    console.log('cancel');
}

function setupFriendsEventListeners() {
    document.querySelectorAll('.accept-friend-request-btn').forEach(button => {
        button.addEventListener('click', () => {
            const requestId = button.getAttribute('user-id');
            acceptFriendRequestFromUser(requestId);
        });
    });

    document.querySelectorAll('.reject-friend-request-btn').forEach(button => {
        button.addEventListener('click', () => {
            rejectFriendRequestFromUser(button.getAttribute('user-id'));
        });
    });

    document.querySelectorAll('.remove-friend-btn').forEach(button => {
        button.addEventListener('click', () => {
            removeUserFromFriends(button.getAttribute('user-id'));
        });
    });

    document.querySelectorAll('.cancel-friend-request-btn').forEach(button => {
        button.addEventListener('click', () => {
            cancelFriendRequestToUser(button.getAttribute('user-id'));
        });
    });

    document.querySelectorAll('.add-friend-btn').forEach(button => {
        button.addEventListener('click', () => {
            addUserToFriends(button.getAttribute('user-id'));
        });
    });
}

document.querySelectorAll('.url-item').forEach(urlItem => {
    urlItem.addEventListener('click', () => {
        goToUrl(urlItem.getAttribute('url'));
        globalSearchInput.value = '';
    });
});

window.addEventListener('popstate', (event) => {
    backToUrl(document.location.pathname);
});

globalSearchForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(globalSearchForm);
    const searchParams = new URLSearchParams(formData);
    goToUrl(`/search/?${searchParams.toString()}`);
});

setupFriendsEventListeners();

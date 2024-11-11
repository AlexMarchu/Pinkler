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
            setupChatItemListeners();
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
    console.log('accept');
}

function rejectFriendRequestFromUser(userId) {
    console.log('reject');
}

function removeUserFromFriends(userId) {
    console.log('remove');
}

function addUserToFriends(userId) {
    console.log('add');
}

function cancelFriendRequestToUser(userId) {
    console.log('cancel');
}

function setupFriendsEventListeners() {
    document.querySelectorAll('.accept-friend-request-btn').forEach(button => {
        button.addEventListener('click', () => {
            acceptFriendRequestFromUser(button.getAttribute('user-id'));
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

function setupChatItemListeners() {
    document.querySelectorAll('.chat-item').forEach(chatItem => {
        chatItem.addEventListener('click', () => {
            goToUrl('/chats/lobby/');
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
setupChatItemListeners();

// document.addEventListener('DOMContentLoaded', function () {
//     document.querySelector('.users-list').addEventListener('click', function (event) {
//         if (event.target && event.target.classList.contains('add-friend-button')) {
//             const userId = event.target.dataset.userId;

//             fetch(`/friends/send-request/${userId}/`, {
//                 method: 'POST',
//                 headers: {
//                     'X-CSRFToken': '{{ csrf_token }}',
//                     'Content-Type': 'application/json'
//                 },
//                 body: JSON.stringify({})
//             })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.success) {
//                     alert(data.success);
//                     event.target.textContent = 'Запрос отправлен';
//                     event.target.disabled = true;
//                 } else if (data.error) {
//                     alert(data.error);
//                 }
//             })
//             .catch(error => console.error('Ошибка при запросе:', error));
//         }

//         if (event.target && event.target.classList.contains('accept-friend-request-button')) {
//             const requestId = event.target.dataset.requestId;
//             console.log(event.target);
//             console.log(event.target.dataset);

//             if (!requestId) {
//                 console.error('Ошибка: requestId не задан или равен null/undefined');
//                 return;
//             }

//             console.log('RequestId:', requestId);

//             fetch(`/friends/accept-request/${requestId}/`, {
//                 method: 'POST',
//                 headers: {
//                     'X-CSRFToken': '{{ csrf_token }}',
//                     'Content-Type': 'application/json'
//                 },
//                 body: JSON.stringify({})
//             })
//             .then(response => {
//                 if (!response.ok) {
//                     throw new Error(`HTTP error! status: ${response.status}`);
//                 }
//                 return response.json();
//             })
//             .then(data => {
//                 if (data.success) {
//                     alert(data.success);
//                     event.target.textContent = 'Запрос принят';
//                     event.target.disabled = true;
//                 } else if (data.error) {
//                     alert(data.error);
//                 }
//             })
//             .catch(error => console.error('Ошибка при принятии запроса:', error));
//         }
//     });
// });
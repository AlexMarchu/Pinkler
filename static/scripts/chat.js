const roomName = JSON.parse(document.getElementById('room-name').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + roomName
    + '/'
);

function fetchMessages() {
    chatSocket.send(JSON.stringify({
        'command': 'fetch_messages'
    }));
}

chatSocket.onopen = function (e) {
    fetchMessages();
};

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    const chatLog = document.getElementById('chat-log');

    if (data.command === 'new_message') {
        const username = data.message.sender;
        const messageContent = data.message.content;
        const timestamp = data.message.timestamp;
        const image = data.message.image;

        const messageDiv = document.createElement('div');
        messageDiv.className = 'chat-message';
        messageDiv.classList.add(username === '{{ user.username }}' ? 'sent' : 'received');

        let messageText = `<div class="message">[${timestamp}] ${username}: ${messageContent}</div>`;
        messageDiv.innerHTML = messageText;

        if (image) {
            const imageDiv = document.createElement('div');
            imageDiv.className = 'message';
            imageDiv.innerHTML = `<img src="${image}" alt="Image" style="max-width: 100%; border-radius: 10px;"/>`;
            chatLog.appendChild(imageDiv);
        }

        chatLog.appendChild(messageDiv);
        chatLog.scrollTop = chatLog.scrollHeight;

    } else if (data.command === 'fetch_messages') {
        chatLog.innerHTML = '';
        data.messages.forEach(msg => {
            let messageDiv = document.createElement('div');
            messageDiv.className = 'chat-message';
            messageDiv.classList.add(msg.sender === '{{ user.username }}' ? 'sent' : 'received');

            messageDiv.innerHTML = `<div class="message">[${msg.timestamp}] ${msg.sender}: ${msg.content}</div>`;

            if (msg.image) {
                const imageDiv = document.createElement('div');
                imageDiv.className = 'message';
                imageDiv.innerHTML = `<img src="${msg.image}" alt="Image" style="max-width: 100%; border-radius: 10px;"/>`;
                chatLog.appendChild(imageDiv);
            }

            chatLog.appendChild(messageDiv);
        });

        chatLog.scrollTop = chatLog.scrollHeight;
    }
};


chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly :(');
};

document.getElementById('attachment-button').onclick = function () {
    document.getElementById('chat-image-input').click();
};

document.getElementById('chat-message-input').focus();
document.getElementById('chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // Enter (return key)
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    const imageInputDom = document.querySelector('#chat-image-input');
    const imageFile = imageInputDom.files[0];

    let imageData = '';
    if (imageFile) {
        const reader = new FileReader();
        reader.onloadend = function () {
            imageData = reader.result;
            chatSocket.send(JSON.stringify({
                'message': message,
                'image': imageData,
                'command': 'new_message',
            }));
            messageInputDom.value = '';
            imageInputDom.value = '';
        }

        reader.readAsDataURL(imageFile);
    } else {
        chatSocket.send(JSON.stringify({
            'message': message,
            'command': 'new_message',
        }));
        messageInputDom.value = '';
    }
};
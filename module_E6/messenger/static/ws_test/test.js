document.addEventListener('DOMContentLoaded', function() {
    const roomName = 'general';
    const chatSocket = new WebSocket('ws://' + window.location.hostname + ':8001/ws/chat/' + roomName + '/');

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        const messageElement = document.createElement('li');

        // Создаём элемент для аватара
        const avatar = document.createElement('img');
        avatar.src = data.avatar_url;  // URL аватара пользователя
        avatar.alt = 'User Avatar';
        avatar.style.width = '30px';
        avatar.style.height = '30px';
        avatar.style.borderRadius = '50%';
        avatar.style.marginRight = '10px';

        // Создаём элемент для имени пользователя
        const username = document.createElement('strong');
        username.textContent = data.username;  // Имя пользователя

        // Создаём элемент для сообщения
        const messageText = document.createElement('span');
        messageText.textContent = data.message;

        // Создаём все элементы в сообщение
        messageElement.appendChild(avatar);
        messageElement.appendChild(username);
        messageElement.appendChild(document.createTextNode(': '));
        messageElement.appendChild(messageText);

        // Добавляем сообщение в чат
        document.querySelector('#messages').appendChild(messageElement);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#message-input').focus();
    document.querySelector('#message-input').onkeyup = function(e) {
        if (e.keyCode === 13) {  // Enter key
            document.querySelector('#send-button').click();
        }
    };

    document.querySelector('#send-button').onclick = function(e) {
        const messageInputDom = document.querySelector('#message-input');
        const message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'message': message
        }));
        messageInputDom.value = '';
    };
});
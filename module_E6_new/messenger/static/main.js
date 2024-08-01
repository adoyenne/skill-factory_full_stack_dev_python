document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const messagesDiv = document.getElementById('messages');
    const usersDiv = document.getElementById('users');
    const chatsDiv = document.getElementById('chats');
    const authDiv = document.getElementById('auth');
    const chatAppDiv = document.getElementById('chatApp');
    const createChatForm = document.getElementById('createChatForm');
    const chatNameInput = document.getElementById('chatName');
    const chatTitle = document.getElementById('chatTitle'); // Новое поле для заголовка чата

    let token = '';
    let currentChatId = null;
    let socket = null;
    let currentUser = { username: 'Unknown', avatar: '/media/avatars/default-avatar.jpeg' };

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        fetch('/api/login/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.access) {
                token = data.access;
                authDiv.style.display = 'none';
                chatAppDiv.style.display = 'flex';
                fetchCurrentUser(); // Получаем данные о текущем пользователе
                loadUsers();
                loadChats(); // Загрузка чатов при входе
            } else {
                alert('Login failed: ' + (data.detail || 'Unknown error'));
            }
        })
        .catch(error => console.error('Error:', error));
    });

    registerForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const formData = new FormData();
        formData.append('username', document.getElementById('regUsername').value);
        formData.append('password', document.getElementById('regPassword').value);
        formData.append('first_name', document.getElementById('regFirstName').value);
        formData.append('last_name', document.getElementById('regLastName').value);
        formData.append('avatar', document.getElementById('regAvatar').files[0]);

        fetch('/api/users/register/', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            alert('User registered successfully');
        })
        .catch(error => console.error('Error:', error));
    });

    createChatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const chatName = chatNameInput.value.trim();

        if (chatName) {
            fetch('/api/chats/', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name: chatName })
            })
            .then(response => response.json())
            .then(chat => {
                if (chat.id) {
                    console.log('Chat created successfully:', chat);
                    loadChats(); // Обновление списка чатов после создания нового
                } else {
                    console.error('Failed to create chat:', chat);
                }
            })
            .catch(error => console.error('Error:', error));
        } else {
            console.error('Chat name is required.');
        }
    });

    function fetchCurrentUser() {
        console.log('Fetching current user...');
        fetch('/api/users/me/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            console.log('Response status:', response.status);
            return response.json();
        })
        .then(data => {
            console.log('Current user data:', data); // Проверьте данные
            currentUser = {
                username: data.username || 'Unknown',
                avatar: data.avatar || '/media/avatars/default-avatar.jpeg'
            };
        })
        .catch(error => {
            console.error('Error fetching current user:', error);
            currentUser = { username: 'Unknown', avatar: '/media/avatars/default-avatar.jpeg' };
        });
    }

    function loadUsers() {
        fetch('/api/users/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                usersDiv.innerHTML = '';
                data.forEach(user => {
                    const userDiv = document.createElement('div');
                    userDiv.textContent = user.username;
                    userDiv.onclick = () => openChat(user.id);
                    usersDiv.appendChild(userDiv);
                });
            } else {
                console.error('Failed to load users:', data);
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function loadChats() {
        fetch('/api/chats/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => response.json())
        .then(data => {
            if (Array.isArray(data)) {
                chatsDiv.innerHTML = '';
                data.forEach(chat => {
                    const chatDiv = document.createElement('div');
                    chatDiv.className = 'chat-item';
                    chatDiv.textContent = chat.name;
                    chatDiv.setAttribute('data-chat-id', chat.id);
                    chatDiv.onclick = () => openChat(chat.id);
                    chatsDiv.appendChild(chatDiv);
                });
            } else {
                console.error('Failed to load chats:', data);
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function openChat(chatId) {
        fetch(`/api/chats/${chatId}/messages/`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error('Failed to fetch messages');
            }
        })
        .then(data => {
            if (Array.isArray(data)) {
                currentChatId = chatId;

                // Найти информацию о чате в чате списка чатов
                const chat = document.querySelector(`.chat-item[data-chat-id="${chatId}"]`);
                if (chat) {
                    chatTitle.textContent = `Chat: ${chat.textContent}`;
                } else {
                    chatTitle.textContent = 'Chat: Unknown'; // Если не удалось найти название чата
                }

                messagesDiv.innerHTML = '';
                data.forEach(message => addMessage(message));
                connectWebSocket(currentChatId);
            } else {
                console.error('Failed to load messages:', data);
            }
        })
        .catch(error => console.error('Error:', error));
    }

    function addMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';

        const avatarImg = document.createElement('img');
        avatarImg.src = message.user.avatar || '/media/avatars/default-avatar.jpeg';
        avatarImg.alt = `${message.user.username}'s avatar`;
        avatarImg.width = 50;
        avatarImg.height = 50;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.innerHTML = `<div class="message-author">${message.user.username}</div><div>${message.content}</div>`;

        messageDiv.appendChild(avatarImg);
        messageDiv.appendChild(contentDiv);

        messagesDiv.prepend(messageDiv); // Добавляем сообщения в начало
    }

    function connectWebSocket(chatId) {
        if (socket) {
            socket.close(); // Закрыть существующее соединение
        }

        socket = new WebSocket(`ws://${window.location.hostname}:8001/ws/chat/${chatId}/`);

        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            addMessage({ user: currentUser, content: data.message });
        };

        socket.onclose = function(event) {
            console.error('Chat socket closed unexpectedly');
        };
    }

    sendButton.addEventListener('click', function() {
        const message = messageInput.value.trim();

        if (currentChatId && socket && message) {
            socket.send(JSON.stringify({ message: message }));
            messageInput.value = ''; // Очистить поле ввода после отправки
        } else {
            console.error('Cannot send message. Ensure you are connected to a chat and the message is not empty.');
        }
    });
});
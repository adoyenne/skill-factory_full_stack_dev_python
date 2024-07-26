document.addEventListener('DOMContentLoaded', function() {
    // Функция для получения значения cookie по имени
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.startsWith(name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Получаем токен доступа из cookies
    const accessToken = getCookie('access_token');

    if (!accessToken) {
        console.error('No access token found in cookies.');
        return;
    }

    console.log('Access token found:', accessToken); // Для отладки

    // Функция для получения списка комнат
    function fetchRooms() {
        fetch('http://' + window.location.hostname + ':8000/api/rooms/', {
            headers: {
                'Authorization': 'Bearer ' + accessToken,
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.status === 401) {
                throw new Error('Unauthorized');
            }
            if (!response.ok) {
                throw new Error('Failed to fetch rooms: ' + response.statusText);
            }
            return response.json();
        })
        .then(data => {
            const roomList = document.querySelector('#room-list');
            roomList.innerHTML = '';
            data.forEach(room => {
                const roomItem = document.createElement('li');
                roomItem.textContent = room.name;
                roomItem.onclick = () => {
                    window.location.href = '/chat/' + encodeURIComponent(room.name) + '/';
                };
                roomList.appendChild(roomItem);
            });
        })
        .catch(error => {
            console.error('Error fetching rooms:', error);
            alert('Failed to fetch rooms: ' + error.message);
        });
    }

    // Обработчик для кнопки создания комнаты
    document.querySelector('#create-room-button').onclick = function(e) {
        console.log('Create room button clicked'); // Для отладки
        const roomNameInput = document.querySelector('#room-name-input');
        const roomName = roomNameInput.value.trim();

        if (!roomName) {
            alert('Room name cannot be empty');
            return;
        }

        fetch('http://' + window.location.hostname + ':8000/api/rooms/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + accessToken
            },
            body: JSON.stringify({
                'name': roomName
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.id) {
                fetchRooms();  // Обновляем список комнат
            } else {
                alert('Failed to create room: ' + (data.detail || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error creating room:', error);
            alert('Failed to create room: ' + error.message);
        });
    };

    fetchRooms();
});
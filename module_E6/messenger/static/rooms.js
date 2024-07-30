document.addEventListener('DOMContentLoaded', function() {
    const accessToken = localStorage.getItem('access');

    if (!accessToken) {
        console.error('No access token found in localStorage.');
        return;
    }

    console.log('Access token found:', accessToken);

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
                return response.text().then(text => {
                    throw new Error('Failed to fetch rooms: ' + text);
                });
            }
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);

            // Проверяем, является ли data массивом
            if (Array.isArray(data)) {
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
            } else {
                console.error('Expected an array but got:', data);
                alert('Unexpected response format.');
            }
        })
        .catch(error => {
            console.error('Error fetching rooms:', error);
            alert('Failed to fetch rooms: ' + error.message);
        });
    }

    // Обработка нажатия кнопки создания комнаты
    document.querySelector('#create-room-button').onclick = function(e) {
        console.log('Create room button clicked');
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
        .then(response => {
            if (response.status === 401) {
                throw new Error('Unauthorized');
            }
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error('Failed to create room: ' + text);
                });
            }
            return response.json();
        })
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

    // Загрузка списка комнат при загрузке страницы
    fetchRooms();
});
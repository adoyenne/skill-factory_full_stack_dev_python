document.addEventListener('DOMContentLoaded', function() {
    const sendMessageButton = document.getElementById('send-message-button');
    const closeMessageButton = document.getElementById('close-message-button');
    const messageModal = document.getElementById('message-modal');
    const messageInput = document.getElementById('message-input');
    const messageRecipient = document.getElementById('message-recipient');
    let recipientId = null;

    // Assuming recipient ID is set through URL parameters or context
    const urlParams = new URLSearchParams(window.location.search);
    recipientId = urlParams.get('recipient_id');

    if (recipientId) {
        messageRecipient.textContent = `Sending to User ID: ${recipientId}`;
    }

    closeMessageButton.addEventListener('click', function() {
        window.location.href = '{% url "user_list" %}';
    });

    sendMessageButton.addEventListener('click', function() {
        if (recipientId) {
            const message = messageInput.value;
            if (message) {
                chatSocket.send(JSON.stringify({
                    'recipient': recipientId,
                    'message': message
                }));
                messageInput.value = '';
                window.location.href = '{% url "user_list" %}';
            }
        }
    });

    const roomName = 'private';
    const chatSocket = new WebSocket('ws://' + window.location.hostname + ':8001/ws/chat/' + roomName + '/');


    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);

    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
});
document.addEventListener('DOMContentLoaded', function() {
    const sendMessageButton = document.getElementById('send-message-button');
    const closeMessageButton = document.getElementById('close-message-button');
    const messageModal = document.getElementById('message-modal');
    const messageInput = document.getElementById('message-input');
    const messageRecipient = document.getElementById('message-recipient');
    let recipientId = null;

    document.querySelectorAll('a[href^="/send-message/"]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            recipientId = this.getAttribute('href').split('/').pop();
            messageRecipient.textContent = `Sending to User ID: ${recipientId}`;
            messageModal.style.display = 'block';
        });
    });

    closeMessageButton.addEventListener('click', function() {
        messageModal.style.display = 'none';
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
                messageModal.style.display = 'none';
            }
        }
    });

    const roomName = 'private';
    const chatSocket = new WebSocket('ws://' + window.location.hostname + ':8001/ws/chat/' + roomName + '/');


    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        // Handle incoming messages here
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };
});
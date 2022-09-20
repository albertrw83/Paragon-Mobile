
const notificationSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/notification/'
    + roomName
    + '/'
);

notificationSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    console.log(data)
    document.querySelector('#notification_count').innerText = data.message.count;
};

notificationSocket.onclose = function (e) {
    console.error('notification socket closed unexpectedly');
};

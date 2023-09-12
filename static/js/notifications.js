
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('notification-modal');
    const notificationList = document.getElementById('notification-list');
    const markAsViewedButtons = document.querySelectorAll('.mark-as-viewed');

    function getNotifications() {
        fetch('/get_notifications/')
        .then(response => response.json())
        .then(data => {
            notificationList.innerHTML = '';
            data.notifications.forEach(notification => {
                notificationList.innerHTML += `<li>${notification.message} <button class="mark-as-viewed" data-notification-id="${notification.id}">Mark as Viewed</button></li>`;
            });
        });
    }

    modal.addEventListener('show.bs.modal', getNotifications);

    markAsViewedButtons.forEach(button => {
        button.addEventListener('click', function() {
            const notificationId = this.dataset.notificationId;
            fetch(`/mark_notification_as_viewed/${notificationId}/`)
            .then(response => response.json())
            .then(data => {
                this.parentElement.style.display = 'none';
            });
        });
    });
});

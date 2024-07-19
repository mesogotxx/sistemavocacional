document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('editEventModal');
    var span = document.getElementsByClassName('close')[0];

    var editEventId = document.getElementById('edit-event-id');
    var editEventTitle = document.getElementById('edit-event-title');
    var editEventDescription = document.getElementById('edit-event-description'); // Corregido para que coincida con el ID del textarea

    // Function to open the modal and populate it with event data
    function openModal(event) {
        var eventId = event.getAttribute('data-event-id');
        var eventTitle = event.querySelector('h2').textContent;
        var eventDescription = event.querySelector('p').textContent;

        // Update the modal elements with the event data
        editEventId.value = eventId;
        editEventTitle.value = eventTitle;
        editEventDescription.value = eventDescription; // Usa value en lugar de textContent

        modal.style.display = 'block';
    }

    // Event listener to close the modal
    span.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }

    // Event listener to handle the form submission
    document.getElementById('edit-event-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        var formData = new FormData(this);

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest', // Indicates AJAX request
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value // CSRF token
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error:', data.error);
            } else {
                // Update the event in the list
                var eventItem = document.querySelector(`.event-item[data-event-id="${data.id}"]`);
                if (eventItem) {
                    eventItem.querySelector('h2').textContent = data.title;
                    eventItem.querySelector('p').textContent = data.description;
                }

                // Close the modal
                modal.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

    // Add event listeners to edit buttons
    document.querySelectorAll('.edit-event-btn').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent navigation
            openModal(this.closest('.event-item'));
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    // Selectors for main elements
    const selectBtn = document.getElementById('select-student-btn');
    const studentCards = document.querySelectorAll('.student-card');
    const modal = document.getElementById('selected-student-modal');
    const modalContent = document.getElementById('selected-student-name');
    const closeModal = document.getElementById('close-modal');

    // Control for selection in progress
    let selectionInProgress = false;

    // Event listener for "Select Student" button
    selectBtn.addEventListener('click', function () {
        initiateSelection();
    });

    // Initiates selection process by making a request to the server
    function initiateSelection() {
        fetch('/select_student', {
            method: 'POST'
        })
            .then(response => response.json())
            .then(data => {
                if (data.selected_student) {
                    simulateSelection(data.selected_student);
                } else {
                    alert(data.status);
                }
            });
    }

    // Animates the selection process on the student cards
    function simulateSelection(selectedStudent) {
        let index = 0;
        const totalStudents = studentCards.length;
        const interval = setInterval(() => {
            studentCards.forEach(card => card.classList.remove('active'));
            studentCards[index].classList.add('active');
            index = (index + 1) % totalStudents;
        }, 100);

        // Stop animation and highlight the selected student after 3 seconds
        setTimeout(() => {
            clearInterval(interval);
            studentCards.forEach(card => {
                if (card.getAttribute('data-name') === selectedStudent) {
                    card.classList.add('active');
                } else {
                    card.classList.remove('active');
                }
            });
            showModal(selectedStudent);
        }, 3000);
    }

    // Displays a modal with the selected student's name
    function showModal(name) {
        modalContent.textContent = `Selected Student: ${name}`;
        modal.style.display = 'block';
    }

    // Event listener to close modal
    closeModal.addEventListener('click', function () {
        modal.style.display = 'none';
    });

    // Closes modal when clicking outside of it
    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    };

    // Polls the server every 2 seconds to check if a selection is in progress
    setInterval(function () {
        fetch('/status')
            .then(response => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.text();
            })
            .then(text => {
                if (!text) {
                    throw new Error("Empty response from server");
                }
                return JSON.parse(text);
            })
            .then(data => {
                if (data.selection_in_progress && !selectionInProgress) {
                    selectionInProgress = true;
                    simulateSelectionFromPolling();
                } else if (!data.selection_in_progress && selectionInProgress) {
                    selectionInProgress = false;
                }
            })
            .catch(error => {
                console.error("Error in fetch:", error);
            });
    }, 2000);

    // Simulates selection animation based on polling result
    function simulateSelectionFromPolling() {
        let index = 0;
        const totalStudents = studentCards.length;
        const interval = setInterval(() => {
            studentCards.forEach(card => card.classList.remove('active'));
            studentCards[index].classList.add('active');
            index = (index + 1) % totalStudents;
        }, 100);

        // Continuously checks if selection has been completed by polling
        function checkSelection() {
            fetch('/status')
                .then(response => response.json())
                .then(data => {
                    if (!data.selection_in_progress && data.selected_student) {
                        clearInterval(interval);
                        studentCards.forEach(card => {
                            if (card.getAttribute('data-name') === data.selected_student) {
                                card.classList.add('active');
                            } else {
                                card.classList.remove('active');
                            }
                        });
                        showModal(data.selected_student);
                    } else {
                        setTimeout(checkSelection, 500);
                    }
                });
        }

        checkSelection();
    }
});

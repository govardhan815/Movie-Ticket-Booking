document.addEventListener('DOMContentLoaded', () => {
    const seatLayout = document.getElementById('seat-layout');
    const seats = [...'ABCD'].flatMap(row => Array.from({ length: 5 }, (_, i) => row + (i + 1)));

    const renderSeats = (booked) => {
        seatLayout.innerHTML = '';
        seats.forEach(seat => {
            const div = document.createElement('div');
            div.classList.add('seat');
            div.innerText = seat;
            if (booked.includes(seat)) {
                div.classList.add('booked');
            } else {
                div.addEventListener('click', () => {
                    div.classList.toggle('selected');
                });
            }
            seatLayout.appendChild(div);
        });
    };

    const loadSeats = () => {
        const date = document.getElementById('date').value;
        const time = document.getElementById('time').value;
        if (date && time) {
            fetch('/get_booked_seats', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ movie, date, time })
            })
            .then(res => res.json())
            .then(data => renderSeats(data.booked));
        }
    };

    document.getElementById('date').addEventListener('change', loadSeats);
    document.getElementById('time').addEventListener('change', loadSeats);

    document.querySelector('form').addEventListener('submit', function(e) {
        const selectedSeats = Array.from(document.querySelectorAll('.seat.selected')).map(div => div.innerText);
        if (selectedSeats.length === 0) {
            e.preventDefault();
            alert('Please select at least one seat.');
        } else {
            selectedSeats.forEach(seat => {
                const input = document.createElement('input');
                input.type = 'hidden';
                input.name = 'seats';
                input.value = seat;
                this.appendChild(input);
            });
        }
    });
});

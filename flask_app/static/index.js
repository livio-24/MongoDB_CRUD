$(document).ready(function () {
    $('#search').on('input', function () {
        var search_attr = $('#search-attribute').val();
        var query = $(this).val();
        $.get('/search', { query: query, search_attr: search_attr }, function (data) {
            $('#results').empty();
            data.forEach(function (hotel) {
                const html =
                    `<div class="col">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">${hotel._id}</h5>
                                <p class="card-text">Avg rating: ${hotel.average_value.toFixed(1)}</p>
                                <p class="card-text">${hotel.hotel_info.city}, ${hotel.hotel_info.address} (${hotel.hotel_info.province})</p>
                                <a href="/reviews/${hotel._id}" class="btn btn-primary">View reviews</a>
                            </div>
                        </div>
                    </div>`;
                // Aggiungi il blocco HTML al tuo contenitore
                $('#results').append(html);
            });
        });
    });
});
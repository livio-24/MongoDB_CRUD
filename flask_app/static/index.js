$(document).ready(function () {
    function handleInputChange() {
        var search_attr = $('#search-attribute').val();
        var query = $('#search').val();
        var sort_order = ($('#sort-order').val() === 'asc') ? 1 : -1;
        $.get('/search', { query: query, search_attr: search_attr, sort_order: sort_order }, function (data) {
            $('#results').empty();
            data.forEach(function (hotel) {
                var ratingInt = Math.floor(hotel.average_value);
                var ratingDecimal = (hotel.average_value - ratingInt).toFixed(1);

                var starsHTML = '';
                for (var i = 0; i < ratingInt; i++) {
                    starsHTML += '<i class="fas fa-star text-warning"></i>';
                }
                if (ratingDecimal >= 0.3 && ratingDecimal <= 0.7) {
                    starsHTML += '<i class="fas fa-star-half-alt text-warning"></i>';
                }
                if (ratingDecimal >= 0.8) {
                    starsHTML += '<i class="fas fa-star text-warning"></i>';
                }

                var hotelCardHTML = `
                    <div class="col">
                        <div class="card h-100">
                            <h5 class="card-header">${hotel._id}</h5>
                            <div class="card-body">
                                ${starsHTML}
                                <i>${hotel.average_value.toFixed(1)}</i>
                                <p class="card-text text-dark-emphasis">${hotel.hotel_info.city}, ${hotel.hotel_info.address} (${hotel.hotel_info.province})</p>
                                <a href="/reviews/${hotel._id}" class="btn btn-primary">View reviews</a>
                                <a href="/add/${hotel._id}" class="btn btn-secondary">Add review</a>
                            </div>
                        </div>
                    </div>
                `;

                // Aggiungi il blocco di codice HTML dell'hotel al contenitore
                $('#results').append(hotelCardHTML);
            });
        });
    }

    $('#search-button').on('click', handleInputChange)
    $('#search').on('input', handleInputChange);
    $('#sort-order').on('change', handleInputChange);
    $('#search-attribute').on('input', handleInputChange);


});

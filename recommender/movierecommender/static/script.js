$(document).ready(function() {
    var csrftoken = Cookies.get('csrftoken');
    var movieContainer = $('.row.justify-content-center'); // Reference to movie container
    
    // Function to update movie cards
    function updateMovieCards(movies) {
        movieContainer.empty(); // Clear container before adding new movies
        movies.forEach(movie => {
            movieContainer.append(`
                <div id="${movie.id}" class="col-md-4 d-flex justify-content-center mb-1">
                    <div class="card" style="width: 33vw; min-height: 400px;">
                        <img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" 
                             alt="${movie.original_title}" class="card-img-top">
                        <div class="card-body">
                            <h5 class="card-title">${movie.original_title}</h5>
                            <p class="card-text" style="max-height: 100px; overflow-y: scroll;font-size: 1rem;">
                                ${movie.overview}
                            </p>
                            <p class="read_more" style="font-weight: bold;font-size:1rem;color:blue;
                                font-style: italic; cursor:pointer">
                                read more
                            </p>
                            <p class="text-muted">Rating: ${movie.vote_average}/10</p>
                            <button type="button" class="btn btn-outline-success btn-sm" 
                                    data-id="${movie.id}">Watch</button>
                        </div>
                    </div>
                </div>
            `);
        });
        
        // Attach event to "read more" links
        $(".read_more").off().on('click', function() {
            let cardText = $(this).prev('.card-text');
            if (cardText.css('max-height') === '100px') {
                cardText.css('max-height', 'none');
                $(this).text('read less');
            } else {
                cardText.css('max-height', '100px');
                $(this).text('read more');
            }
        });
        
        // Attach event to "Watch" buttons
        $(".btn.btn-outline-success.btn-sm").off().on('click', function() {
            let movieId = $(this).data('id');
            let button = $(this);
            
            // Mark movie as watched via AJAX
            $.ajax({
                url: `/mark_watched/${movieId}/`,
                type: "POST",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                success: function() {
                    button.attr('disabled', 'true').text("Watched");
                    
                    // Refresh recommendations after marking as watched
                    setTimeout(function() {
                        $.ajax({
                            url: window.location.href,
                            type: "GET",
                            headers: {
                                'X-Requested-With': 'XMLHttpRequest'
                            },
                            success: function(context) {
                                updateMovieCards(context.movie_list);
                            }
                        });
                    }, 1000);
                },
                error: function(xhr, status, error) {
                    console.error(error);
                    alert("Could not mark movie as watched.");
                }
            });
        });
    }
    
    // Handle search input
    $('#floatingInputGroup2').on('input', function() {
        let searchTerm = $(this).val().trim(); // Get the input value
        
        // Only search if there's input or if the field was cleared
        if (searchTerm || searchTerm === '') {
            $.ajax({
                url: window.location.href,  // Current URL
                type: "GET",
                data: { search: searchTerm },  // Send search term
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                },
                dataType: "json",
                success: function(context) {
                    updateMovieCards(context.movie_list); // Update movies
                    
                    // Update validation feedback
                    if (searchTerm === '') {
                        $('#floatingInputGroup2').addClass('is-invalid');
                    } else {
                        $('#floatingInputGroup2').removeClass('is-invalid');
                    }
                },
                error: function(xhr, status, error) {
                    console.error(error);
                }
            });
        }
    });
    
    // Initial movies load (if needed)
    // $.ajax({
    //     url: window.location.href,
    //     type: "GET",
    //     headers: {
    //         'X-Requested-With': 'XMLHttpRequest'
    //     },
    //     success: function(context) {
    //         updateMovieCards(context.movie_list);
    //     }
    // });
});
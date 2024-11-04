$(document).ready(function() {
    var csrftoken = Cookies.get('csrftoken');
    var movieContainer = $('.row.justify-content-center'); // Reference to the movie container

    // Fonction définie en dehors des gestionnaires d'événements
    function updateMovieCards(movies) {
        movieContainer.empty(); // Vider le container avant d'ajouter les nouveaux films
        movies.forEach(movie => {
            movieContainer.append(`
                <div id="${movie.id}" class="col-md-4 d-flex justify-content-center mb-1">
                    <div class="card" style="width: 33vw; min-height: 400px;">
                        <img src="https://image.tmdb.org/t/p/w500${movie.poster_path}" alt="${movie.title}" class="card-img-top">
                        <div class="card-body">
                            <h5 class="card-title">${movie.original_title}</h5>
                            <p class="card-text" style="max-height: 100px; overflow-y: scroll;font-size: 1rem;">${movie.overview}</p>
                            <p class="read_more" style="font-weight: bold;font-size:1rem;color:blue;font-style: italic; cursor:pointer">read more</p>
                            <p class="text-muted">Rating: ${movie.vote_average}/10</p>
                            <button type="button" class="btn btn-outline-success btn-sm">Watch</button>
                        </div>
                    </div>
                </div>
            `);
        });

        // Attach click event to dynamically added buttons
        $(".btn.btn-outline-success.btn-sm").off().on('click', function() {
            $(this).attr('disabled', 'true').text("Watched");
        });
    }

    // GET request to load the initial context (movies)
    $.ajax({
        url: "",  // Assurez-vous que l'URL est correcte ici
        type: "GET",
        dataType: "json",
        success: function(context) {
            updateMovieCards((context.movie_list).slice(0,30));

            // Input change event handler
            $('#floatingInputGroup2').on('change', function() {
                let searchTerm = $('#floatingInputGroup2').val().trim();
                let filteredMovies1 = (context.movie_list).filter(movie => movie.original_title.includes(searchTerm));
                let filteredMovies = filteredMovies1.slice(0, 100);
                console.log(filteredMovies);
                updateMovieCards(filteredMovies);
            });
            $('.class="btn btn-outline-success btn-sm').on('click',function(e){
                const id = $(e.target).attr('data-id');
                $.ajax({
                    url :"",
                    data : id,
                    dataType:'json',
                    success : function(data){
                        console.log(data);
                    }
                })

                
                
                
            })

        

        },
        error: function(xhr, status, error) {
            console.error(error);
        }
    });
    
});

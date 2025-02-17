$(document).ready(function() {
    var csrftoken = Cookies.get('csrftoken');
    var movieContainer = $('.row.justify-content-center'); // Référence au conteneur des films

    // Fonction pour mettre à jour les cartes de films
    function updateMovieCards(movies) {
        movieContainer.empty(); // Vider le conteneur avant d'ajouter les nouveaux films
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

        // Attacher un événement au bouton "Watch"
        $(".btn.btn-outline-success.btn-sm").off().on('click', function() {
            $(this).attr('disabled', 'true').text("Watched");
        });
    }

    // GET request pour récupérer les films filtrés
    $('#floatingInputGroup2').on('input', function() {
        let searchTerm = $(this).val().trim(); // Obtenir la valeur du champ
        $.ajax({
            url: "{% url 'movie_recommendation_view' %}",  // URL de ta vue
            type: "GET",
            data: { search: searchTerm },  // Envoyer le terme de recherche
            dataType: "json",
            success: function(context) {
                updateMovieCards(context.movie_list); // Mettre à jour les films
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });
});

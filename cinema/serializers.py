from rest_framework import serializers

from cinema.models import Genre, CinemaHall, Actor, Movie, MovieSession


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class GenreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name',)


class CinemaHallSerializer(serializers.ModelSerializer):
    capacity = serializers.IntegerField(read_only=True)

    class Meta:
        model = CinemaHall
        fields = ("id", "name", "rows", "seats_in_row", "capacity")


class ActorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name", "full_name")

    @staticmethod
    def get_full_name(obj):
        return obj.__str__()


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("id", "title", "description", "duration", "genres", "actors")


class MovieDetailSerializer(MovieSerializer):
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)


class MovieListSerializer(MovieSerializer):
    genres = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    actors = serializers.StringRelatedField(many=True, read_only=True)


class MovieSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = ("id", "show_time", "movie", "cinema_hall")


class MovieSessionListSerializer(MovieSessionSerializer):
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    cinema_hall_name = serializers.CharField(
        source="cinema_hall.name",
        read_only=True
    )
    cinema_hall_capacity = serializers.IntegerField(
        source="cinema_hall.capacity",
        read_only=True
    )

    class Meta:
        model = MovieSession
        fields = (
            "id",
            "show_time",
            "movie_title",
            "cinema_hall_name",
            "cinema_hall_capacity"
        )


class MovieSessionDetailSerializer(MovieSessionSerializer):
    movie = MovieListSerializer(many=False)
    cinema_hall = CinemaHallSerializer(many=False)

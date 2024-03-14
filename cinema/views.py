# write views here
from rest_framework import viewsets

from cinema.models import Genre, CinemaHall, Actor, Movie, MovieSession
from cinema.serializers import (GenreSerializer,
                                CinemaHallSerializer,
                                ActorSerializer,
                                MovieSerializer,
                                MovieListSerializer,
                                MovieDetailSerializer,
                                MovieSessionSerializer,
                                MovieSessionDetailSerializer,
                                MovieSessionListSerializer)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CinemaHallViewSet(viewsets.ModelViewSet):
    queryset = CinemaHall.objects.all()
    serializer_class = CinemaHallSerializer


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().prefetch_related("genres").prefetch_related("actors")

    def get_serializer_class(self):
        serializer_class = MovieSerializer

        if self.action == "list":
            serializer_class = MovieListSerializer

        if self.action == "retrieve":
            serializer_class = MovieDetailSerializer

        return serializer_class


class MovieSessionViewSet(viewsets.ModelViewSet):
    queryset = MovieSession.objects.all().select_related("movie").select_related("cinema_hall")

    def get_serializer_class(self):
        serializer_class = MovieSessionSerializer

        if self.action == "retrieve":
            serializer_class = MovieSessionDetailSerializer

        if self.action == "list":
            serializer_class = MovieSessionListSerializer

        return serializer_class

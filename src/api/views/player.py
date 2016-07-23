from google.appengine.api import memcache

from rest_framework import filters

from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from core.models import Player, Match
from core.utils import format_matches_to_show_form, form_cache_key, calculate_elo

from .base import TokenRequiredModelViewSet
from ..serializers import PlayerSerializer, PatchPlayerSerializer


class PlayerViewSet(TokenRequiredModelViewSet):

    serializer_class = PlayerSerializer
    queryset = Player.objects.all()
    permissions = []
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter)

    def get_serializer_class(self):
        """Use a different serializer when handling PATCH requests, which
        makes more fields read_only."""
        serializer_class = self.serializer_class

        if self.request.method == 'PATCH':
            serializer_class = PatchPlayerSerializer

        return serializer_class

    @detail_route(methods=['get'])
    def form(self, request, pk=None):
        """Return the results of recent games involving the specified player."""
        user = self.get_object()

        # try and get the queryset of results from memcache
        cache_key = form_cache_key(user)
        queryset = memcache.get(cache_key)
        if queryset is None:
            # this might be pretty inefficent on the datastore...
            queryset = Match.objects.matches_involving_player(user)
            memcache.set(cache_key, queryset)

        # we support a limit param which reduces the number of results
        limit = int(request.query_params.get('limit', 10))
        limited_queryset = queryset[:limit]

        form = format_matches_to_show_form(limited_queryset, user)

        return Response(form)

    @list_route(methods=['get'])
    def elo(self, request, pk=None):
        """Return the points that can be won/lost between two players."""
        player1 = request.query_params.get('player1')
        player2 = request.query_params.get('player2')

        if player1 is None or player2 is None:
            return None

        player1_details = Player.objects.get(slack_id=player1)
        player2_details = Player.objects.get(slack_id=player2)

        result1 = calculate_elo(player1_details.elo, player2_details.elo, 1)
        result2 = calculate_elo(player2_details.elo, player1_details.elo, 1)

        def _generate_results(player_details, elo_win, elo_lose):
            return {
                'slack_id': player_details.slack_id,
                'elo': player_details.elo,
                'elo_win': elo_win,
                'elo_lose': elo_lose,
                'points_win': elo_win - player_details.elo,
                'points_lose': player_details.elo - elo_lose,
            }

        results = [
            _generate_results(player1_details, result1[0], result2[1]),
            _generate_results(player2_details, result2[0], result1[1]),
        ]

        return Response(results)

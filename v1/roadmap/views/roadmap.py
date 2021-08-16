from rest_framework import status
from rest_framework.response import Response

from config.helpers.cache import CachedModelViewSet
from v1.third_party.rest_framework.permissions import IsStaffOrReadOnly
from ..models.roadmap import Roadmap
from ..serializers.roadmap import RoadmapSerializer
from ...teams.models.team import CoreTeam


class RoadmapViewSet(CachedModelViewSet):
    queryset = Roadmap.objects.select_related('team').order_by('estimated_completion_date').all()
    serializer_class = RoadmapSerializer
    permission_classes = [IsStaffOrReadOnly]

    def list(self, request):  # noqa: ignore=A003
        team_name = request.query_params.get('team')
        if team_name:
            team = CoreTeam.objects.filter(title__iexact=team_name)
            if team:
                roadmaps = Roadmap.objects.filter(
                    team__pk=team[0].pk).select_related('team').order_by('estimated_completion_date')
            else:
                return Response(
                    {'detail': f'No Roadmap under team name: {team_name} was found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            roadmaps = self.filter_queryset(roadmaps)
            page = self.paginate_queryset(roadmaps)
            serializer = self.serializer_class(page, context={'request': request}, many=True)
        else:
            page = self.paginate_queryset(self.queryset)
            serializer = self.serializer_class(page, context={'request': request}, many=True)
        return self.get_paginated_response(serializer.data)

from rest_framework.serializers import ModelSerializer

from ..models.feedback import Feedback


class FeedbackSerializer(ModelSerializer):

    class Meta:
        fields = ('pk', 'name', 'email', 'message', 'created_date', 'modified_date',)
        read_only_fields = ('created_date', 'modified_date',)
        extra_kwargs = {
            'email': {'write_only': True}
        }
        model = Feedback

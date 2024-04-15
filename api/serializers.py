from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

class Reviewserializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class Profileserializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class Tagerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class projectSerializer(serializers.ModelSerializer):
    owner = Profileserializer(many=False)
    tags = Tagerializer(many=True)
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = Reviewserializer(reviews, many=True)
        return serializer.data

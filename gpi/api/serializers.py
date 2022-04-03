from rest_framework import serializers




# class ExposureSerializer(serializers.Serializer):
#     time = serializers.DictField(child = serializers.CharField())
#     hour = serializers.IntegerField(required=True, min_value=0, max_value=23)
#     value = serializers.FloatField(required=True)

#     def create(self, validated_data):
#         return Hourly(**validated_data)

#     def update(self, instance, validated_data):
#         instance.hour = validated_data.get('hour', instance.hour)
#         instance.value = validated_data.get('value', instance.value)
#         return instance

# # class TrackSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = None
# #         fields = '__all__'



class PlateSerializer(serializers.Serializer):
    """Your data serializer, define your fields here."""
    identifier = serializers.CharField(max_length=500)
    repository = serializers.CharField(max_length=500)
    #other = serializers.CharField(max_length=200, required=False)
    #exposuer_info = serializers.ListField(child=ExposureSerializer(), min_length=24, max_length=24)
    #exposure_info = serializers.ArrayField()
    #exposure_info = serializers.CharField(max_length=200)

class ArchiveSerializer(serializers.Serializer):
    abbr = serializers.CharField(max_length=500)
    name = serializers.CharField(max_length=500)
    url = serializers.CharField(max_length=500)
    desc = serializers.CharField(max_length=500)
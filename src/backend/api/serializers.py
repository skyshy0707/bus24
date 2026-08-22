import base64

from rest_framework import serializers

from api import fields, models


class ATPSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.ATP
        fields = "__all__"


class ATPHiddenSerialize(fields.ATPIdDefault):

    def __call__(self, serializer_field):
        instance = super().__call__(serializer_field)
        serialized = ATPSerializer(instance)
        return serialized.data


class ATPUpdateSerializer(ATPSerializer):

    user = serializers.HiddenField(default=fields.UserIdDefault())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.fields = ("name", "user")


class BusSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Bus
        fields = "__all__"


class LeadSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Lead
        fields = "__all__"


class LeadCreateSerializer(LeadSerializer):

    atp = serializers.HiddenField(default=ATPSerializer(fields.ATPIdDefault()))

    id = serializers.IntegerField(read_only=True)
    atp_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Lead
        exclude = ("date",)


class AttachUnitsToLeadSerializer(LeadSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.fields = ("unit_set",)


class UnitSerializer(serializers.ModelSerializer):

    bus = BusSerializer(read_only=True)

    class Meta:
        model = models.Unit
        fields = "__all__"


class LeadUpdatePropsSerializer(LeadSerializer):

    unit_set = UnitSerializer(many=True, required=False)
    date = serializers.DateTimeField(read_only=True)
    atp_id = serializers.IntegerField(read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Meta.exclude = ("atp",)


class LeadUnitSetUpdateSerializer(serializers.Serializer):

    units = serializers.ListField(child=serializers.IntegerField(), required=False)
    change_type = serializers.ChoiceField(choices=('add', 'remove'), default='add')


class UnitsAtLeadSerializer(serializers.Serializer):

    unit_set = serializers.SerializerMethodField('unit_set-serializer')

    def unit_set_serializer(self,):
        request = self.content.get('request')
        lead_id = request.lead_id
        unit_set = models.Unit.objects.filter(lead_id=lead_id)
        serializer = UnitSerializer(many=True, queryset=unit_set, required=False)

        return serializer.data


class UnitUpdateSerializer(UnitSerializer):

    id = serializers.IntegerField(read_only=True)
    atp_id = serializers.IntegerField(read_only=True)
    bus_id = serializers.IntegerField()


class UnitCreateSerializer(serializers.ModelSerializer):

    atp = serializers.HiddenField(default=fields.ATPIdDefault())

    id = serializers.IntegerField(read_only=True)
    atp_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Unit
        exclude = ("lead",)


class MessageSerializer(serializers.ModelSerializer):

    lead = LeadSerializer(read_only=True)
    lead_url = serializers.URLField(read_only=True, source='get_lead_url')
    id = serializers.IntegerField(read_only=True)
    atp_id = serializers.IntegerField(read_only=True)
    atp_name = serializers.CharField(read_only=True, source='get_atp_name')

    class Meta:
        model = models.Message
        fields = '__all__'


class MessageCreateSerializer(serializers.ModelSerializer):

    atp = serializers.HiddenField(default=fields.ATPIdDefault())

    class Meta:
        model = models.Message
        fields = '__all__'


class RegistrationSerialzier(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)
    email = serializers.EmailField(source='username')

    class Meta:
        model = models.User
        fields = ('email', 'password', 'password_2')

    
    def validate(self, data):
        if data['password'] != data['password_2']:
            raise serializers.ValidationError("Passwords are not matched")
        return data

    def to_internal_value(self, data):
        for key, value in data.items():
            try:
                data[key] = base64.b64decode(value).decode('utf-8')
            except Exception as e:
                raise serializers.ValidationError({
                    key: "Wrong format base64"
                })
        return super().to_internal_value(data)
    
    def create(self, validated_data):
        validated_data.pop("password_2")
        user = self.Meta.model(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
    
        return user
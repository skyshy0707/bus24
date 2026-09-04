from django.db.models import F, Q, Count
from django.http import Http404
from rest_framework import generics, request, response, status, viewsets
from rest_framework.authentication import ( 
    BasicAuthentication
)

from api import models, pagination, permissions, serializers, utils
from bearer_auth.middleware.bearer_auth.utils import deactivate_tokens
from bearer_auth.middleware.bearer_auth import BearerAuthentication
from bearer_auth.middleware.bearer_auth.utils import create_bearer_token

# Create your views here.



class ATPMixin:

    authentication_classes = [BearerAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    
class ATPMixinE(ATPMixin):

    def get_object(self):
        try:
            return models.ATP.objects.get(user=self.request.user)
        except models.ATP.DoesNotExist as e:
            raise Http404(e)
    

class ATPView(ATPMixinE, generics.RetrieveAPIView):
    serializer_class = serializers.ATPSerializer


class ATPCreate(ATPMixin, generics.CreateAPIView):
    serializer_class = serializers.ATPUpdateSerializer


class ATPEdit(ATPMixinE, generics.UpdateAPIView):
    serializer_class = serializers.ATPUpdateSerializer


class ATPDelete(generics.DestroyAPIView, ATPMixinE):
    pass

class ListMixin:

    authentication_classes = [BearerAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = pagination.Pagination


class ListChoicesMixin(ListMixin, viewsets.GenericViewSet):

    def get(self, request: request.Request):

        items = self.paginate_queryset(self.queryset)
        return self.get_paginated_response(items)


class BusColors(ListChoicesMixin):

    queryset = utils.choices_to_objects(models.COLORS) 
    
    
class BusCathegory(ListChoicesMixin):

    queryset = utils.choices_to_objects(models.CAPACITY_CATHEGORY)


class Buses(generics.ListAPIView):
    authentication_classes = [BearerAuthentication]
    pagination_class = pagination.Pagination
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.BusSerializer
    queryset = models.Bus.objects.all()


class ATPForAcceptingLeadParam(generics.ListAPIView):

    authentication_classes = [BearerAuthentication]
    pagination_class = pagination.Pagination
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.ATPSerializer

    def get_queryset(self):
        capacity_class = self.kwargs.get("cc")
        capacity = models.define_min_capacity(capacity_class)

        print("capaciry:", capacity, "cc:", capacity_class)
        qs = models.ATP.objects.filter(Q(unit__bus__capacity__gte=capacity) & Q(unit__lead=None)).distinct()
        print("atp qs: ", qs)
        return qs
    

class UnitsForAcceptingLead(generics.ListAPIView):

    authentication_classes = [BearerAuthentication]
    pagination_class = pagination.Pagination
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsOwner
    ]
    serializer_class = serializers.UnitSerializer

    def get_queryset(self):
        capacity_class = self.kwargs.get("cc")
        capacity = models.define_min_capacity(capacity_class)
        atp_id = permissions.get_profile_id(self.request)
        return models.Unit.objects.filter(Q(bus__capacity__gte=capacity) & Q(lead=None) & Q(atp__id=atp_id))
    

class UncoveredLeads(generics.ListAPIView):

    pagination_class = pagination.Pagination
    serializer_class = serializers.LeadSerializer

    def get_queryset(self):
        return models.Lead.objects.annotate(
            total_units=Count('unit')
        ).filter(units_per_route__gt=F('total_units'))


class ProfileLeadsInfo(generics.ListAPIView):

    authentication_classes = [BearerAuthentication]
    pagination_class = pagination.Pagination
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = serializers.LeadSerializer


class MyCreatedLeads(ProfileLeadsInfo):

    def get_queryset(self):
        atp_id = permissions.get_profile_id(self.request)
        return models.Lead.objects.filter(atp__id=atp_id)
    

class MyAcceptedLeads(ProfileLeadsInfo):

    def get_queryset(self):
        atp_id = permissions.get_profile_id(self.request)
        return models.Lead.objects.filter(unit__atp_id=atp_id).distinct()


class MyBusUnits(ListMixin, generics.ListAPIView):

    serializer_class = serializers.UnitSerializer

    def get_queryset(self):
        atp_id = permissions.get_profile_id(self.request)
        return models.Unit.objects.filter(atp__id=atp_id)
    

class LeadUnitSet(ListMixin, generics.ListAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsOwner | permissions.IsLeadWasMessaged
    ]
    serializer_class = serializers.UnitSerializer

    def get_object(self):
        lead_id = self.kwargs.get("id")
        try:
            return models.Lead.objects.get(id=lead_id)
        except models.Lead.DoesNotExist as e:
            raise Http404(e)

    def get_queryset(self):
        return self.get_object().unit_set.all()

    
class BusUnitMixin:

    authentication_classes = [BearerAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
    ]

class BusUnitOwnMixin(BusUnitMixin):
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsOwner
    ]
    lookup_field = "id"
    queryset = models.Unit.objects.all()


class BusUnitView(BusUnitOwnMixin, generics.RetrieveAPIView):
    serializer_class = serializers.UnitSerializer

class BusUnitCreate(BusUnitMixin, generics.CreateAPIView):

    serializer_class = serializers.UnitCreateSerializer


class BusUnitEdit(BusUnitOwnMixin, generics.UpdateAPIView):

    serializer_class = serializers.UnitUpdateSerializer
        
 
class BusUnitDelete(BusUnitOwnMixin, generics.DestroyAPIView):
    pass
    

class LeadMixin:

    authentication_classes = [BearerAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.LeadSerializer
    

class LeadCrudMixin(LeadMixin):
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsOwner | permissions.IsLeadWasMessaged
    ]
    lookup_field = "id"
    queryset = models.Lead.objects.all()


class LeadView(LeadCrudMixin, generics.RetrieveAPIView):
    pass

class LeadPropsEdit(LeadCrudMixin, generics.UpdateAPIView):

    permission_classes = [
        permissions.IsAuthenticated, 
        permissions.IsOwner
    ]
    serializer_class = serializers.LeadUpdatePropsSerializer


class LeadCreate(LeadMixin, generics.CreateAPIView):

    serializer_class = serializers.LeadCreateSerializer


class LeadDelete(LeadCrudMixin, generics.DestroyAPIView):

    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsOwner
    ]

class UnitsAtLead(ListMixin, generics.ListAPIView):

    serializer_class = serializers.UnitsAtLeadSerializer


class ModifyLeadUnitSet(LeadCrudMixin, generics.UpdateAPIView):

    serializer_class = serializers.LeadUnitSetUpdateSerializer

    def patch(self, request: request.Request, *args, **kwargs):
        atp_id = permissions.get_profile_id(self.request)
        serialized = self.serializer_class(data=self.request.data)

        if not serialized.is_valid():
            return response.Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serialized.errors
            )
        
        qs_params = utils.to_data_obj(serialized.validated_data)
        
        units = qs_params.units
        change_type = qs_params.change_type
        unit_queryset = models.Unit.objects.filter(id__in=units, atp__id=atp_id)
        lead = self.get_object()

        if change_type == "add":
            lead.unit_set.add(*unit_queryset[:lead.units_per_route])
        else:
            lead.unit_set.remove(*unit_queryset)

        return response.Response(
            serializers.LeadUpdatePropsSerializer(lead).data
        )
    

class MessageMixin:

    authentication_classes = [BearerAuthentication]
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = serializers.MessageSerializer


class MessageWMixin(MessageMixin):

    lookup_field = 'id'

    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsOwner
    ]


class MessageCreate(MessageWMixin, generics.CreateAPIView):

    serializer_class = serializers.MessageCreateSerializer


class MessageUpdate(MessageWMixin, generics.UpdateAPIView):

    queryset = models.Message.objects.all()


class MessageDelete(MessageWMixin, generics.DestroyAPIView):
    pass


class MessageView(MessageWMixin, generics.RetrieveAPIView):
    queryset = models.Message.objects.all()


class SendMessage(generics.CreateAPIView):

    lookup_field = "lead_id"

    authentication_classes = [BearerAuthentication]
    permission_classes = [
        permissions.IsAuthenticated,
        permissions.IsOwner
    ]
    serializer_class = serializers.MessageSerializer

    def get_object(self):
        try:
            return models.Lead.objects.get(id=self.lookup_field)
        except models.Lead.DoesNotExist as e:
            raise Http404(e)
    
    def perform_create(self, serializer):
        data = serializer.data
        lead = self.get_object()
        capacity_class = lead.capacity_class
        capacity = models.define_min_capacity(capacity_class)
        allowed_atps = models.ATP.objects.filter(Q(unit__bus__capacity__gte=capacity) & Q(unit__lead=None)).distinct()
        to = data.get("to")
        to = allowed_atps.values("id").intersection(set(to))
        serializer.data.to = to
        return super().perform_create(serializer)


class Chats(ListMixin, generics.ListAPIView):

    serializer_class = serializers.ATPSerializer

    def get_queryset(self):
        atp_id = permissions.get_profile_id(self.request)
        return models.ATP.objects.filter(Q(message__to__in=[atp_id]) & Q(message__atp=atp_id)).distinct()


class ShoutBox(ListMixin, generics.ListAPIView):

    lookup_field = 'id'

    serializer_class = serializers.MessageSerializer

    def get_queryset(self):
        atp_id = permissions.get_profile_id(self.request)
        chat_id = self.kwargs.get(self.lookup_field)

        return models.Message.objects.filter(
            Q(atp=chat_id) & Q(to__in=[atp_id])
        ).union(
            models.Message.objects.filter(Q(atp=atp_id) & Q(to__in=[chat_id]))
        )
    
    
class RefreshToken(generics.CreateAPIView):
    authentication_classes = [BearerAuthentication]

    def post(self, request, *args, **kwargs):
        deactivate_tokens(request)
        
        return response.Response(
            create_bearer_token(request), 
            status=status.HTTP_201_CREATED
        )

    
class Signup(generics.CreateAPIView):

    serializer_class = serializers.RegistrationSerialzier


class Signin(generics.views.APIView):

    authentication_classes = [
        BasicAuthentication
    ]

    def post(self, request, *args, **kwargs):
        deactivate_tokens(request)
        
        return response.Response(
            create_bearer_token(request), 
            status=status.HTTP_201_CREATED
        )


class Logout(generics.RetrieveAPIView):

    authentication_classes = [BearerAuthentication]

    def get(self, request, *args, **kwargs):
        deactivate_tokens(request)
        return response.Response(
            { "message": "Logout success" }, 
            status=status.HTTP_204_NO_CONTENT
        )
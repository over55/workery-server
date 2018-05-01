# -*- coding: utf-8 -*-
from django_filters.rest_framework import DjangoFilterBackend
from starterkit.drf.permissions import IsAuthenticatedAndIsActivePermission
from django.conf.urls import url, include
from django.shortcuts import get_list_or_404, get_object_or_404
from rest_framework import filters
from rest_framework import generics
from rest_framework import authentication, viewsets, permissions, status
from rest_framework.response import Response
from tenant_api.pagination import StandardResultsSetPagination
from tenant_api.permissions.order import (
   CanListCreateOrderPermission,
   CanRetrieveUpdateDestroyOrderPermission
)
from tenant_api.serializers.activity_sheet_item import (
    ActivitySheetItemListCreateSerializer,
)
from tenant_foundation.models import ActivitySheetItem


class ActivitySheetItemListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ActivitySheetItemListCreateSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = (
        permissions.IsAuthenticated,
        IsAuthenticatedAndIsActivePermission,
        CanListCreateOrderPermission
    )

    def get_queryset(self):
        """
        List
        """
        queryset = ActivitySheetItem.objects.all().order_by('-created')
        return queryset

    def post(self, request, format=None):
        """
        Create
        """
        serializer = ActivitySheetItemListCreateSerializer(data=request.data, context={
            'created_by': request.user,
            'franchise': request.tenant
        })
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

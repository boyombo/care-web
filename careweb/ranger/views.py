from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
import django_excel as excel

from payment.models import Payment
from ranger.models import Ranger, WalletFunding
from ranger.serializers import CreateFundingSerializer, WalletFundingSerializer


class CreateFundingView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = CreateFundingSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            p_date = data.get("payment_date")
            payment = Payment.objects.create(amount=data.get('amount'), payment_date=p_date,
                                             reference="{0} - {1}".format(data.get('name'), data.get('bank')), status=0,
                                             narration="", paid_by=data.get('name'), cust_reference="")
            ranger = Ranger.objects.get(id=data.get('ranger_id'))
            wf = WalletFunding.objects.create(name=data.get('name'), bank=data.get('bank'), amount=data.get('amount'),
                                              payment_date=p_date, ranger=ranger, payment=payment,
                                              status=0)
            serialized = WalletFundingSerializer(wf)
            return Response({"success": True, "funding": serialized.data}, status=status.HTTP_200_OK)
        else:
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_200_OK)


@login_required
def export_rangers(request):
    column_names = [
        "S/N", "First Name", "Last Name", "Phone Number",
        "LGA", "Balance", "Date Added"
    ]
    output = [column_names]
    rows = []
    rangers = Ranger.objects.all()
    index = 1
    for ranger in rangers:
        date = ranger.created.strftime("%B %d, %Y") if ranger.created else ""
        rows.append([
            index,
            ranger.first_name,
            ranger.last_name,
            ranger.phone,
            ranger.lga.name,
            ranger.balance,
            date
        ])
    output.extend(rows)
    sheet = excel.pe.Sheet(output)
    return excel.make_response(sheet, "xls", file_name="Rangers")

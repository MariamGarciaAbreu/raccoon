from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import TransactionSerializer, TransactionCategorySerializer
from .models import Transaction, TransactionCategory
from rest_framework import status

@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello, world!'})

@api_view(['POST'])
def add_transaction(request):
    transaction = TransactionSerializer(data=request.data)
    if transaction.is_valid():
        transaction.save()
        return Response(transaction.data, status=status.HTTP_201_CREATED)
    else:
        return Response(transaction.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def view_transactions(request):
    
    if request.query_params:
        transactions = Transaction.objects.filter(**request.query_params.dict())
    else:
        transactions = Transaction.objects.all()

    if transactions:
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    else:
        return Response([])

@api_view(['GET'])
def view_transaction(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_category(request):
    categories = TransactionCategory.objects.all()
    
    if categories:
        serializer = TransactionCategorySerializer(categories, many=True)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_transaction(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TransactionSerializer(transaction, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_transaction(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    transaction.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
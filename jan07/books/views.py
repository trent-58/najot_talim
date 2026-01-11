from rest_framework.views import APIView
from rest_framework import status, response
from books import models, serializers


class BookListView(APIView):
    def get(self, request):
        books = models.Book.objects.all()
        serializer = serializers.BookSerializer(books, many=True)
        return response.Response(serializer.data)


class BookCreateView(APIView):
    def post(self, request):
        serializer = serializers.BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookUpdateView(APIView):
    def put(self, request, pk):
        book = models.Book.objects.filter(pk=pk).first()
        if not book:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        book = models.Book.objects.filter(pk=pk).first()
        if not book:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookDeleteView(APIView):
    def delete(self, request, pk):
        book = models.Book.objects.filter(pk=pk).first()
        if not book:
            return response.Response(status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return response.Response(status=status.HTTP_204_NO_CONTENT)


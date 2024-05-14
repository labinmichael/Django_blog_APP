from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination


class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes =[JWTAuthentication]

    def get(self,request):
        try:
            blogs =Blog.objects.filter(user=request.user)
            serializer =BlogSerializer(blogs, many=True)
            return Response({"data":serializer.data,
                    "message":"blogs fetch successfully"
                        },status=status.HTTP_200_OK)
        
        except Exception as e:
                        
            return Response({"data":{},
                            "message":"something went wrong"
                                },status=status.HTTP_400_BAD_REQUEST)               

            
           
    def post(self,request):
        try:
            data        = request.data
            data['user']=request.user.id  
            serializer = BlogSerializer(data=data)
            if not serializer.is_valid():
                                return Response({"data":serializer.errors
                                 ,"message":"something went wrong"
                                 },status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({"data":serializer.data,
                             "message":"blog create success"
                                 },status=status.HTTP_201_CREATED)
        except Exception as e:
                        
            return Response({"data":{},
                            "message":"something went wrong"
                                },status=status.HTTP_400_BAD_REQUEST)   

    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get('uid')).first()  # Select the first object from the queryset
            
            if not blog:
                return Response({"data": {}, "message": "Invalid blog UID"}, status=status.HTTP_400_BAD_REQUEST)
        
            if not request.user == blog.user: 
                return Response({"data": {}, "message": "You are not authorized to do this"}, status=status.HTTP_400_BAD_REQUEST)        

            serializer = BlogSerializer(blog, data=data, partial=True)   
            if not serializer.is_valid():
                return Response({"data": serializer.errors, "message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response({"data": serializer.data, "message": "Blog updated successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"data": {}, "message": f"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
        


    def delete(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uid=data.get('uid')).first()  # Select the first object from the queryset
            
            if not blog:
                return Response({"data": {}, "message": "Invalid blog UID"}, status=status.HTTP_400_BAD_REQUEST)
        
            if not request.user == blog.user: 
                return Response({"data": {}, "message": "You are not authorized to do this"}, status=status.HTTP_400_BAD_REQUEST)        
                
            blog.delete()  # Delete the blog directly
            return Response({"data": {}, "message": "Blog deleted successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)  # Print the exception for debugging purposes
            return Response({"data": {}, "message": f"Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)


  
class BlogSearchView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            search_query = request.GET.get('search')
            if not search_query:
                return Response({
                    "data": {},
                    "message": "Search query parameter is missing"
                }, status=status.HTTP_400_BAD_REQUEST)
                
            blogs = Blog.objects.filter(Q(title__icontains=search_query) | Q(blog_txt__icontains=search_query), user=request.user)
            serializer = BlogSerializer(blogs, many=True)
            return Response({
                "data": serializer.data,
                "message": "Blogs fetched successfully based on search query"
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "data": {},
                "message": "Something went wrong"
            }, status=status.HTTP_400_BAD_REQUEST)



class BlogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class VisitorBlogView(APIView):
    
    def get(self, request):
        try:
            blogs = Blog.objects.all().order_by('-created_at')
            paginator = BlogPagination()
            result_page = paginator.paginate_queryset(blogs, request)
            serializer = BlogSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"data": {}, "message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
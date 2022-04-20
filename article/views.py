from typing import List, Type

from django.shortcuts import render
from django.http import JsonResponse, Http404
from article.models import Article, Category, Tag, Avatar
# from article.serializers import ArticleListSerializer, ArticleDetailSerializer
from article.serializers import ArticleSerializer, CategorySerializer, CategoryDetailSerializer, TagSerializer, \
    ArticleDetailSerializer, AvatarSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from article.permissions import IsAdminUserOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
# Create your views here.
from rest_framework.filters import SearchFilter

# def article_list(request):
#     articles = Article.objects.all()
#     serializer = ArticleListSerializer(articles, many=True)
#     return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})
'''@api_view(['GET','POST'])
def article_list(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

'''
class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleListSerializer
    # 为什么这里只要加一个permission_classes就可以来限制权限了
    permission_classes = [IsAdminUserOrReadOnly]
    # permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
'''

'''class ArticleDetail(APIView):

    # 获取单个文章对象
    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except:
            raise Http404

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        # 返回json数据
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article, data=request.data)
        # 验证提交数据是否合法
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        # 删除成功后返回204
        return Response(status=status.HTTP_204_NO_CONTENT)'''

'''class ArticleDetail(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin, generics.GenericAPIView
                    ):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)'''

'''
class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAdminUserOrReadOnly]
'''


# 此view可集成列表、详情逻辑
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    # 替代get_queryset函数
    # 此为精准匹配
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['author__username', 'title']
    # 此为模糊搜索，未实现成功
    filter_backends = [SearchFilter]
    search_fields = ['author__username', 'title']

    # 在创建文章前，提供了视图集无法自行推断的用户外键字段
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return SomeSerializer
    #     else:
    #         return AnotherSerializer

    # def get_queryset(self):
    #     queryset = self.queryset
    #     username = self.request.query_params.get('username', None)
    #
    #     if username is not None:
    #         queryset = queryset.filter(author__username=username)
    #
    #     return queryset
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleSerializer
        else:
            return ArticleDetailSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    '''分类视图集'''
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        else:
            return CategoryDetailSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminUserOrReadOnly]

class AvatarViewSet(viewsets.ModelViewSet):
    queryset = Avatar.objects.all()
    serializer_class = AvatarSerializer
    permission_classes = [IsAdminUserOrReadOnly]
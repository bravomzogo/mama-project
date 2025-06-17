from django.contrib import admin
from .models import Product, Like, Comment

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at', 'get_like_count')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'image_preview')
    fields = ('name', 'description', 'price', 'image', 'image_preview', 'category', 'created_at')
    ordering = ('-created_at',)
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 100px;" />'
        return 'No image'
    image_preview.allow_tags = True
    image_preview.short_description = 'Image Preview'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('user', 'product')
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, True

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'content_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'product__name', 'content')
    readonly_fields = ('created_at',)
    autocomplete_fields = ('user', 'product')
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, True
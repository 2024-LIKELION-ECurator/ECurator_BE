from django.contrib import admin
from .models import Diary

@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'updated_at')
    list_filter = ('author', 'created_at')
    search_fields = ('title', 'content', 'author__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # 관리자가 작성자와 관련된 데이터를 쉽게 관리하도록 필터링 (옵션으로 수정 가능)
        return queryset

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            # 생성 시 현재 요청 사용자를 작성자로 설정
            obj.author = request.user
        super().save_model(request, obj, form, change)

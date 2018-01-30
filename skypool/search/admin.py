from django.contrib import admin


from .models import Brand, Tag, Article, ArticleImage, ArticleTag, Activity, ActivityParam, ActivityArticle


admin.site.register(Brand)
admin.site.register(Tag)
admin.site.register(Article)
admin.site.register(ArticleImage)
admin.site.register(ArticleTag)
admin.site.register(Activity)
admin.site.register(ActivityParam)
admin.site.register(ActivityArticle)


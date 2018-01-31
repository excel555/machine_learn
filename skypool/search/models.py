from django.db import models


class Brand(models.Model):
    logo = models.ImageField(upload_to='brand_logo')
    name = models.CharField(max_length=100)
    info = models.CharField(max_length=1000)

    baike_url = models.CharField(max_length=1000)
    tianyancha_url = models.CharField(max_length=1000)

    weibo_url = models.CharField(max_length=1000)
    weixin_url= models.CharField(max_length=1000)
    tieba_url = models.CharField(max_length=1000)

    tmall_url = models.CharField(max_length=1000)
    jd_url = models.CharField(max_length=1000)
    job_url = models.CharField(max_length=1000)

    total_popularity_score = models.FloatField(default=0.0)
    total_figure_score = models.FloatField(default=0.0)
    total_market_score = models.FloatField(default=0.0)
    total_innovation_score = models.FloatField(default=0.0)
    total_capital_score = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    def tags(self):
        return Tag.objects.filter(brand=self)

    def activities(self):
        return Activity.objects.filter(brand=self)


class Tag(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Article(models.Model):
    source = models.CharField(max_length=100)
    source_url = models.CharField(max_length=1000)
    create_time = models.DateTimeField(auto_now=True)

    title = models.CharField(max_length=200)
    content = models.CharField(max_length=20000)

    # 曝光
    impression = models.FloatField(default=0.0)
    # 互动
    engagement = models.FloatField(default=0.0)
    # 情感
    sentiment = models.FloatField(default=0.0)

    def __str__(self):
        return '%s: %s' % (self.source, self.title)

    def images(self):
        return [_.image for _ in ArticleImage.objects.filter(article=self)]

    def tags(self):
        return [_.tag for _ in ArticleTag.objects.filter(article=self)]

    def activities(self):
        return [_.activity for _ in ActivityArticle.objects.filter(article=self)]


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='article_image')    

    def __str__(self):
        return '%s: %s' % (self.article.title, self.image.id)


class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return '%s: %s' % (self.article.title, self.tag.name)


class Activity(models.Model):
    create_time = models.DateTimeField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    intent = models.CharField(max_length=100)

    influence = models.FloatField()
    sentiment = models.FloatField()

    popularity_score = models.FloatField(default=0.0)
    figure_score = models.FloatField(default=0.0)
    market_score = models.FloatField(default=0.0)
    innovation_score = models.FloatField(default=0.0)
    capital_score = models.FloatField(default=0.0)

    def __str__(self):
        return '%s: %s' % (self.brand.name, self.intent)

    def params(self):
        return ActivityParam.objects.filter(activity=self)

    def articles(self):
        return [_.article for _ in ActivityArticle.objects.filter(activity=self)]


class ActivityParam(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    external_url = models.CharField(max_length=1000)

    def __str__(self):
        return '%s: %s' % (self.activity, self.name)    


class ActivityArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def __str__(self):
        return '%s: %s' % (self.activity, self.article.title)


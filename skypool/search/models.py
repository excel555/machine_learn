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

    # 品牌曝光/露出
    impression = models.FloatField(default=0.0)
    # 用户互动
    engagement = models.FloatField(default=0.0)
    # 情感
    sentiment = models.FloatField(default=0.0)

    def __str__(self):
        return self.source_url


class ArticleImage(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='article_image')    


class ArticleTag(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)


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


class ActivityParam(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    external_url = models.CharField(max_length=1000)


class ActivityArticle(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)



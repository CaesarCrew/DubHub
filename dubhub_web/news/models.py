from django.db import models

class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='news', blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'news'
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['-id']  # Order by ID descending

class NewsMedia(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='media', blank=False, null=False)
    file = models.FileField(upload_to='news/media/', blank=False, null=False)
    caption = models.CharField(max_length=255, blank=True, null=True)
    news_type = models.IntegerField(default=0)

    def __str__(self):
        return self.caption if self.caption else 'Media for {}'.format(self.news.title)

    class Meta:
        db_table = 'news_media'
        verbose_name = 'News Media'
        verbose_name_plural = 'News Media'
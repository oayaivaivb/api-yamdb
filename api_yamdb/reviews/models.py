from django.db import models

<<<<<<< HEAD
# Create your models here.
=======

class Review(models.Model):
    title = models.IntegerField()  # потом ForeignKey на Title
    author = models.IntegerField()  # потом ForeignKey на User
    text = models.TextField()
    score = models.IntegerField()
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.IntegerField()  # потом ForeignKey на User
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:15]
>>>>>>> f9b892d (отзывы и комменты с заглушками)

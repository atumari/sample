from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    point = models.IntegerField(default=0)
    num_questions = models.IntegerField(default=0)
    register_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Question(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                                related_name='question_author')
    correct = models.CharField(max_length=10)
    point = models.IntegerField(default=0)
    register_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.correct + '(Author: ' + self.author.name +\
                    '  Point: ' + str(self.point) + ')'




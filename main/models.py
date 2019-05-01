from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Lab(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    start_date = models.DateField()
    due_date = models.DateField()
    users = models.ManyToManyField(User)
    completed = models.BooleanField(default=False)

    class Meta: 
        verbose_name_plural = 'Labs'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        print('in save')
        todos = Todo.objects.filter(lab=self, completed=False)
        print(todos, self.id)
        print(len(todos) == 0 and self.id is not None)
        if len(todos) == 0 and self.id: 
            self.completed = True
        super(Lab, self).save(*args, **kwargs)

class Todo(models.Model):
    title = models.CharField(max_length=50)
    completed = models.BooleanField(default=False)
    lab = models.ForeignKey(Lab, default=1, verbose_name=("Lab"), on_delete=models.SET_DEFAULT)
    
    class Meta: 
        verbose_name_plural = 'Todos'

    def __str__(self):
        return self.title
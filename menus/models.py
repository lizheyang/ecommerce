from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=100, default='')
    folder_name = models.CharField(max_length=50, default='')
    description = models.CharField(max_length=200)
    materials = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class MenuStep(models.Model):
    menu = models.ForeignKey(Menu)
    no = models.IntegerField()
    detail = models.TextField()
    img = models.ImageField(upload_to='menus/', default='zero.jpg')

    def __str__(self):
        return self.menu.name + ' Step ' + str(self.no)
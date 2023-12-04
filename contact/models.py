from django.db import models

class Contact(models.Model):
    """Model definition for Contact."""
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=100)
    subject = models.CharField(max_length=400)
    message = models.TextField()
    date_recieved		    = models.DateTimeField(verbose_name='date recieved', auto_now_add=True)
    date_last_viewed		= models.DateTimeField(verbose_name='last viewed', auto_now=True)




    # TODO: Define fields here

    class Meta:
        """Meta definition for Contact."""
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

    def __str__(self):
        """Unicode representation of Contact."""
        return f"{self.name} {self.subject}"

class Subscribe(models.Model):
    email                   = models.EmailField(max_length=200, verbose_name='email', unique=True)
    is_subscribed           = models.BooleanField(default=True ,verbose_name='subscribed' )
    # name                    = models.CharField(max_length=200,verbose_name='name',  blank=True, null=True)    
    date_recieved		    = models.DateTimeField(verbose_name='date recieved', auto_now_add=True)
    date_last_viewed		= models.DateTimeField(verbose_name='last viewed', auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Subscribe'
        verbose_name_plural = 'Subscribes'
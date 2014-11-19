from django.db import models
import django.contrib.auth.models

class C4CUser(models.Model):
    user = models.OneToOneField(django.contrib.auth.models.User,primary_key=True) #make a link with internal django users
    address = models.CharField(max_length=300)
    time_account = models.IntegerField(default=0)
    birthday = models.DateField()
    network = models.ManyToManyField("self",symmetrical=False)
    branches = models.ManyToManyField("C4CBranch")

class C4CJob(models.Model):
    created_by = models.ForeignKey(C4CUser,related_name='jobs_created')
    asked_by = models.ForeignKey(C4CUser,related_name='jobs_asked')
    done_by = models.ForeignKey(C4CUser,related_name='jobs_accepted')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    duration = models.IntegerField() #in minutes
    location = models.CharField(max_length=300) 
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class C4CDonation(models.Model):
    sender = models.ForeignKey(C4CUser,related_name='donations_made')
    receiver = models.ForeignKey(C4CUser,related_name='donations_received')
    date = models.DateTimeField()
    message = models.CharField(max_length=1000)
    amount = models.IntegerField() #in minutes

class C4CBranch(models.Model):
    name = models.CharField(max_length=100,primary_key=True)
    address = models.CharField(max_length=300)
    officers = models.ManyToManyField("C4CUser")
    main_user = models.OneToOneField(C4CUser,related_name='is_main_user_of_branch')

class C4CEvent(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    job = models.ForeignKey(C4CJob,default=None, null=True, blank=True)
    user = models.ForeignKey(C4CUser)
    description = models.CharField(max_length=1000)
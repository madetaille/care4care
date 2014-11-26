import django.contrib.auth.models
from django.db import models


class C4CUser(models.Model):

    """ Add additionnal interesting fields to the default Django's users """
    user = models.OneToOneField(django.contrib.auth.models.User, primary_key=True)  # make a link with internal django users
    address = models.CharField(max_length=300)
    time_account = models.IntegerField(default=0)
    birthday = models.DateField()
    network = models.ManyToManyField("self", symmetrical=False, blank=True)
    branches = models.ManyToManyField("C4CBranch", blank=True)

    def __str__(self):
        """ Allows to clearly see the username in the administration """
        return str(self.user)


class C4CJob(models.Model):

    """ Represents a job """
    created_by = models.ForeignKey(C4CUser, related_name='jobs_created')
    asked_by = models.ForeignKey(C4CUser, related_name='jobs_asked', default=None, null=True, blank=True)
    done_by = models.ForeignKey(C4CUser, related_name='jobs_accepted', default=None, null=True, blank=True)
    offer = models.BooleanField(default=False)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    duration = models.IntegerField(null=True)  # in minutes
    location = models.CharField(max_length=300)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(default=None, null=True, blank=True)
    complete = models.BooleanField(default=False)

    def is_offer(self):
        """ Returns true if the job is an offer """
        return self.created_by == self.done_by

    def is_demand(self):
        """ Returns true if the demand is an offer """
        return self.created_by == self.asked_by

    def __str__(self):
        """ Allows to clearly see the jobs in the administration """
        return "{} - {}".format(("Offer" if self.is_offer() else "Demand"), self.title)


class C4CDonation(models.Model):

    """ Represents a donation """

    sender = models.ForeignKey(C4CUser, related_name='donations_made')
    receiver = models.ForeignKey(C4CUser, related_name='donations_received')
    date = models.DateTimeField()
    message = models.CharField(max_length=1000)
    amount = models.IntegerField()  # in minutes

    def __str__(self):
        """ Allows to clearly see the donations in the administration """
        return "{} > {}: {}".format(str(self.sender), str(self.receiver), self.amount)


class C4CBranch(models.Model):

    """ Represents a branch """

    name = models.CharField(max_length=100, primary_key=True)
    address = models.CharField(max_length=300)
    officers = models.ManyToManyField("C4CUser", blank=True)
    main_user = models.OneToOneField(C4CUser, related_name='is_main_user_of_branch')

    def __str__(self):
        """ Allows to clearly see the branches in the administration """
        return self.name


class C4CEvent(models.Model):

    """ Represents an event """
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    job = models.ForeignKey(C4CJob, default=None, null=True, blank=True)
    user = models.ForeignKey(C4CUser)
    description = models.CharField(max_length=1000)

    def short(self):
        return self.name
    short.allow_tags = True

    def __str__(self):
        """ Allows to clearly see the events in the administration """
        return "{} - {}".format(str(self.date), self.name)

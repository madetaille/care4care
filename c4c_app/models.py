import django.contrib.auth.models
from django.db import models
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from model_utils import FieldTracker


class C4CUser(models.Model):

    """ Add additionnal interesting fields to the default Django's users """

    class Meta:
        verbose_name = 'C4C User'
        verbose_name_plural = 'C4C Users'

    user = models.OneToOneField(django.contrib.auth.models.User, primary_key=True)  # make a link with internal django users
    address = models.CharField(max_length=300)
    time_account = models.IntegerField(default=0)
    birthday = models.DateField()
    network = models.ManyToManyField("self", symmetrical=False, blank=True)
    branches = models.ManyToManyField("C4CBranch", blank=True)

    def __str__(self):
        """ Allows to clearly see the username in the administration """
        return str(self.user)

    def recompute_time_account(self):
        """ Recomputes the time account of a user """
        count = 0
        for job in self.jobs_asked.filter(complete=True):
            count -= job.duration
        for job in self.jobs_accepted.filter(complete=True):
            count += job.duration
        for donation in self.donations_made.all():
            count -= donation.amount
        for donation in self.donations_received.all():
            count += donation.amount
        self.time_account = count
        self.save()


class C4CJob(models.Model):

    """ Represents a job """

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

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

    # Allow to track changes
    tracker = FieldTracker(fields=['asked_by', 'done_by'])

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

    class Meta:
        verbose_name = 'Donation'
        verbose_name_plural = 'Donations'

    sender = models.ForeignKey(C4CUser, related_name='donations_made')
    receiver = models.ForeignKey(C4CUser, related_name='donations_received')
    date = models.DateTimeField()
    message = models.CharField(max_length=1000)
    amount = models.IntegerField()  # in minutes

    # Allow to track changes
    tracker = FieldTracker(fields=['sender', 'receiver'])

    def __str__(self):
        """ Allows to clearly see the donations in the administration """
        return "{} > {}: {}".format(str(self.sender), str(self.receiver), self.amount)


class C4CBranch(models.Model):

    """ Represents a branch """

    class Meta:
        verbose_name = 'Branch'
        verbose_name_plural = 'Branches'

    name = models.CharField(max_length=100, primary_key=True)
    address = models.CharField(max_length=300)
    officers = models.ManyToManyField("C4CUser", blank=True)
    main_user = models.OneToOneField(C4CUser, related_name='is_main_user_of_branch')

    def __str__(self):
        """ Allows to clearly see the branches in the administration """
        return self.name


class C4CEvent(models.Model):

    """ Represents an event """

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'

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


# Signal handlers for time account update
def _get_set_without_none(listt):
    """ Get a set that does not include None from the list ``listt`` """
    return set([i for i in listt if i is not None])


def _update_user_time_account_by_id(id_set):
    """ Update time account of users whose ids are in the set ``id_set`` """
    for user_pk in id_set:
        user = C4CUser.objects.get(pk=user_pk)
        user.recompute_time_account()


@receiver(pre_save, sender=C4CJob)
def handle_job_pre_save(sender, instance, **kwargs):
    """ Registers user that may be impacted by the save of the job """
    instance.user_to_update = _get_set_without_none([instance.asked_by_id, instance.done_by_id, instance.tracker.previous('asked_by'), instance.tracker.previous('asked_by')])


@receiver(post_save, sender=C4CJob)
def handle_job_post_save(sender, instance, **kwargs):
    """ Recomputes the time account of the users impacted by the save of the job """
    _update_user_time_account_by_id(instance.user_to_update)


@receiver(pre_delete, sender=C4CJob)
def handle_job_delete(sender, instance, **kwargs):
    """ Recomputes the time account of the users impacted by the save of the job """
    user_to_update = _get_set_without_none([instance.asked_by_id, instance.done_by_id, instance.tracker.previous('asked_by'), instance.tracker.previous('asked_by')])
    _update_user_time_account_by_id(user_to_update)


@receiver(pre_save, sender=C4CDonation)
def handle_donation_pre_save(sender, instance, **kwargs):
    """ Registers user that may be impacted by the save of the donation """
    instance.user_to_update = _get_set_without_none([instance.sender_id, instance.receiver_id, instance.tracker.previous('sender'), instance.tracker.previous('receiver')])


@receiver(post_save, sender=C4CDonation)
def handle_donation_post_save(sender, instance, **kwargs):
    """ Recomputes the time account of the users impacted by the save of the donation """
    _update_user_time_account_by_id(instance.user_to_update)


@receiver(pre_delete, sender=C4CDonation)
def handle_donation_delete(sender, instance, **kwargs):
    user_to_update = _get_set_without_none([instance.sender_id, instance.receiver_id, instance.tracker.previous('sender'), instance.tracker.previous('receiver')])
    _update_user_time_account_by_id(user_to_update)

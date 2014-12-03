from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from django.contrib.auth.models import User, Group

from c4c_app.models import C4CBranch, C4CDonation, C4CEvent, C4CJob, C4CUser

#########################################
#                                       #
# Models accessible only to super-admin #
#                                       #
#########################################


class C4CAdminUser(admin.StackedInline):

    """ Allow to modify the C4CUser in the administration of the default User model """
    model = C4CUser
    can_delete = False


class UserAdmin(OriginalUserAdmin):

    """ Modify the default UserAdmin to allow to modify C4CUser too"""
    inlines = (C4CAdminUser, )


class C4CAdminBranch(admin.ModelAdmin):
    fields = ('name', 'address', 'main_user')
    readonly_fields = ('group', 'officers_group')
    actions = ['delete_selected']

    def save_model(self, request, obj, form, change):
        """ Automatically creates the two groups needed by the new branch """
        if not change:
            obj.group = Group.objects.create(name=("users - " + obj.name))
            obj.officers_group = Group.objects.create(name=("officers - " + obj.name))
            obj.group.user_set.add(obj.main_user)
            obj.officers_group.user_set.add(obj.main_user)
        admin.ModelAdmin.save_model(self, request, obj, form, change)

    def delete_model(self, request, obj):
        """ Deletes the branch """
        obj.group.delete()
        obj.officers_group.delete()
        admin.ModelAdmin.delete_model(self, request, obj)

    def delete_selected(self, request, obj):
        """ Deletes the branch (bulk)"""
        for o in obj.all():
            o.group.delete()
            o.officers_group.delete()
            o.delete()

########################################
#                                      #
# Models accessible to non-super-admin #
#                                      #
########################################


def _get_user_queryset_from_officer(user):
    """ Return a queryset asking for all the users that the officer can moderate """
    groups = [a.group for a in list(C4CBranch.objects.filter(officers_group__in=list(user.groups.all())))]
    return User.objects.filter(groups__in=groups)


class C4CAdminJob(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Restrict users that are displayed in the form for non-superadmin """
        if not request.user.is_superuser:  # officer
            if db_field.name in ("created_by", "asked_by", "done_by"):
                kwargs["queryset"] = _get_user_queryset_from_officer(request.user)
        return super(C4CAdminJob, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(C4CAdminDonation, self).get_queryset(request)
        if not request.user.is_superuser:  # officer
            users = list(_get_user_queryset_from_officer(request.user))
            return qs.filter(created_by__in=users, asked_by__in=users, done_by__in=users)
        return qs


class C4CAdminDonation(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Restrict users that are displayed in the form for non-superadmin """
        if not request.user.is_superuser:  # officer
            if db_field.name in ("sender", "receiver"):
                kwargs["queryset"] = _get_user_queryset_from_officer(request.user)
        return super(C4CAdminDonation, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        qs = super(C4CAdminDonation, self).get_queryset(request)
        if not request.user.is_superuser:  # officer
            users = list(_get_user_queryset_from_officer(request.user))
            return qs.filter(sender__in=users, receiver__in=users)
        return qs


class C4CAdminEvent(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """ Restrict users that are displayed in the form for non-superadmin """
        if not request.user.is_superuser:  # officer
            if db_field.name in ("user"):
                kwargs["queryset"] = _get_user_queryset_from_officer(request.user)
        return super(C4CAdminEvent, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.unregister(User)
# admin.site.unregister(Group)
admin.site.register(User, UserAdmin)

admin.site.register(C4CJob, C4CAdminJob)
admin.site.register(C4CDonation, C4CAdminDonation)
admin.site.register(C4CBranch, C4CAdminBranch)
admin.site.register(C4CEvent, C4CAdminEvent)

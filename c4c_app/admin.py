from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from django.contrib.auth.models import User, Group

from c4c_app.models import C4CBranch, C4CDonation, C4CEvent, C4CJob, C4CUser


class C4CAdminUser(admin.StackedInline):

    """ Allow to modify the C4CUser in the administration of the default User model """
    model = C4CUser
    can_delete = False


class UserAdmin(OriginalUserAdmin):

    """ Modify the default UserAdmin to allow to modify C4CUser too"""
    inlines = (C4CAdminUser, )


class C4CAdminJob(admin.ModelAdmin):
    pass


class C4CAdminDonation(admin.ModelAdmin):
    pass


class C4CAdminBranch(admin.ModelAdmin):
    fields = ('name', 'address', 'main_user')
    readonly_fields = ('group', 'officers_group')
    actions = ['delete_selected']

    def save_model(self, request, obj, form, change):
        """ Automatically creates the two groups needed by the new branch """
        if not change:
            obj.group = Group.objects.create(name=("users - " + obj.name))
            obj.officers_group = Group.objects.create(name=("officers - " + obj.name))
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


class C4CAdminEvent(admin.ModelAdmin):
    pass


admin.site.unregister(User)
# admin.site.unregister(Group)
admin.site.register(User, UserAdmin)

admin.site.register(C4CJob, C4CAdminJob)
admin.site.register(C4CDonation, C4CAdminDonation)
admin.site.register(C4CBranch, C4CAdminBranch)
admin.site.register(C4CEvent, C4CAdminEvent)

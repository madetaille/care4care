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
    pass


class C4CAdminEvent(admin.ModelAdmin):
    pass


admin.site.unregister(User)
# admin.site.unregister(Group)
admin.site.register(User, UserAdmin)

admin.site.register(C4CJob, C4CAdminJob)
admin.site.register(C4CDonation, C4CAdminDonation)
admin.site.register(C4CBranch, C4CAdminBranch)
admin.site.register(C4CEvent, C4CAdminEvent)

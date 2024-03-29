from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
            }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Company)
admin.site.register(models.CbJobsData)
admin.site.register(models.CbQnsData)
admin.site.register(models.CbBrowsingData)
admin.site.register(models.Location)
admin.site.register(models.Job)
admin.site.register(models.CompanyChatbot)
admin.site.register(models.JobMap)
admin.site.register(models.Benefit)
admin.site.register(models.QuestionTopic)
admin.site.register(models.Question)
admin.site.register(models.RoleType)

from django.contrib import admin

from organizations.models import organizations, grups, dicts
from breaks.models.replacements import GroupInfo


########################################
# IN_LINE
########################################
class EmployeeInline(admin.TabularInline):
    model = organizations.Employee
    fields = ('user', 'position', 'date_joined')


class MemberInline(admin.TabularInline):
    model = grups.Member
    fields = ('user', 'date_joined')


class ProfileBreaksInline(admin.StackedInline):
    model = GroupInfo
    fields = ('group', 'min_active', 'break_start', 'break_end', 'break_max_duration')


########################################
# MODELS
########################################
@admin.register(organizations.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director')
    inlines = (EmployeeInline, )


@admin.register(grups.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager',)
    inlines = (MemberInline, ProfileBreaksInline,)


@admin.register(dicts.Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active',)


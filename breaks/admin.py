from django.contrib import admin
from django.contrib.admin import TabularInline

from breaks.models import breaks, dicts, organizations, grups, replacements


########################################
# IN_LINE
########################################
class ReplacementEmployeeInline(TabularInline):
    model = replacements.ReplacementEmployee
    fields = ('employee', 'status')




########################################
# MODELS
########################################
@admin.register(organizations.Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'director')


@admin.register(grups.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'manager', 'min_active')


@admin.register(replacements.Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'breaks_start', 'breaks_end', 'breaks_max_duration')

    inlines = (
        ReplacementEmployeeInline,
    )


@admin.register(breaks.Break)
class BreakAdmin(admin.ModelAdmin):
    list_display = ('id', 'replacement', 'break_start', 'break_end',)


@admin.register(dicts.ReplacementStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active',)


@admin.register(dicts.BreakStatus)
class BreakStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active',)

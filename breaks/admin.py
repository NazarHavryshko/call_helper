from django.contrib import admin
from django.contrib.admin import TabularInline

from breaks.models import breaks, dicts, replacements


########################################
# IN_LINE
########################################
# class ReplacementEmployeeInline(TabularInline):
#     model = replacements.ReplacementEmployee
#     fields = ('employee', 'status')


########################################
# MODELS
########################################
@admin.register(replacements.Replacement)
class ReplacementAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'breaks_start', 'breaks_end', 'breaks_max_duration')


@admin.register(breaks.Break)
class BreakAdmin(admin.ModelAdmin):
    list_display = ('id', 'replacement', 'break_start', 'break_end',)


@admin.register(dicts.ReplacementStatus)
class ReplacementStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active',)


@admin.register(dicts.BreakStatus)
class BreakStatusAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'sort', 'is_active',)

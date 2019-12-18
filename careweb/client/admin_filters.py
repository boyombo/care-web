from django.contrib import admin


class MyClientFilter(admin.SimpleListFilter):
    title = "my client"

    parameter_name = "mine"

    def lookups(self, request, model_admin):
        return (("0", "No"), ("1", "Yes"))

    def queryset(self, request, queryset):
        if self.value() == "0":
            return queryset.exclude(ranger__user=request.user)
        if self.value() == "1":
            return queryset.filter(ranger__user=request.user)

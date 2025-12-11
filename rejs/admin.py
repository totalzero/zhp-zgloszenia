from django import forms
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Rejs, Zgloszenie, Wplata, Wachta, Ogloszenie


class OgloszenieInline(admin.StackedInline):
	model = Ogloszenie
	extra = 0
	fields = ('tytul', 'text')

class WachtaForm(forms.ModelForm):
	czlonkowie = forms.ModelMultipleChoiceField(
		Zgloszenie.objects.none(),
		required=False,
		widget=admin.widgets.FilteredSelectMultiple("Członkowie", is_stacked=False)
	)
	class Meta:
		fields = "__all__"

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		if self.instance and self.instance.pk:
			self.fields['czlonkowie'].queryset = Zgloszenie.objects.filter(rejs=self.instance.rejs)
			self.fields['czlonkowie'].initial = self.instance.czlonkowie.all()
		else:
			rejs_initial = self.initial.get('rejs') or (self.data.get('rejs')if self.data else None) 
			if rejs_initial:
				try:
					self.fields['czlonkowie'].queryset = Zgloszenie.objects.filter(rejs_id=rejs_initial)
				except Exception:
					self.fields['czlonkowie'].queryset = Zgloszenie.Objects.none()
			else:
				self.fields['czlonkowie'].queryset = Zgloszenie.objects.none()
	def save(self, commit=True):
		instance = super().save(commit=commit)
		selected = self.cleaned_data.get('czlonkowie', [])
		current = set(self.instance.czlonkowie.all())
		to_remove = current - set(selected)
		for zg in to_remove:
			zg.wachta = None
			zg.save(update_fields=['wachta'])

		for zg in selected:
			if zg.rejs_id != instance.rejs_id:
				raise forms.ValidationError(f"Zgłoszenie {zg} nie nalezy do rejsu {instance.rejs}")
			zg.wachta = instance
			zg.save(update_fields=['wachta'])
		return instance

#@admin.register(Wachta)
class WachtaAdmin(admin.ModelAdmin):
	form=WachtaForm
	list_display = ('nazwa', 'rejs')
	list_filter = ('rejs', )
	#filter_horizontal = ("czlonkowie", )

class WachtaInline(admin.TabularInline):
	model = Wachta
	form = WachtaForm
	extra = 0
	show_change_link = True

class WplataInline(admin.TabularInline):
	model = Wplata
	extra = 0
	readonly_fields = ['data']
	ordering = ['data']

class ZgloszenieInline(admin.TabularInline):
	model = Zgloszenie
	extra = 0
	readonly_fields = ['imie', 'nazwisko', 'email', 'telefon']
	show_change_link = True


@admin.register(Rejs)
class RejsyAdmin(admin.ModelAdmin):
	list_display = ['nazwa', 'od', 'do', 'start', 'koniec']
	inlines = [ZgloszenieInline, WachtaInline, OgloszenieInline]

@admin.register(Zgloszenie)
class ZgloszenieAdmin(admin.ModelAdmin):
	list_display = ("id", "imie", "nazwisko", "rejs")
	list_filter = ('rejs', )
	search_fields = ('imie', 'nazwisko')
	readonly_fields = ('rejs_cena', 'do_zaplaty', 'suma_wplat')
	inlines = [WplataInline]
	fieldsets = (
		("Dane zgłoszenia: ", {
			"fields": (
				"imie",
				"nazwisko",
				"email",
				"telefon",
				"status",
				"wzrok",
				"rejs",
				"wachta",
			)
		}),
		("rozliczenie:", {
			"fields": (
				"rejs_cena",
				"suma_wplat",
				"do_zaplaty"
			)
		}),
	)
"""
@admin.register(Wplata)
class WplataAdmin(admin.ModelAdmin):
	list_display = ["id", "finanse", "kwota", "data"]
	list_filter = ['finanse']
	ordering = ["-data"]

"""

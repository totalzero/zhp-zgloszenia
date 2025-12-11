from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import reverse
from .models import Ogloszenie, Zgloszenie, Wplata
from .mailers import send_simple_mail
from django.template.loader import render_to_string

@receiver(pre_save, sender=Zgloszenie)
def zgloszenie_pre_save(sender, instance, **kwargs):
	if not instance.pk:
		instance._old_status = None
		instance._old_wachta_id = None
	else:
		try:
			old = Zgloszenie.objects.get(pk=instance.pk)
			instance._old_status = old.status
			instance._old_wachta_id = old.wachta_id
		except Zgloszenie.DoesNotExist:
			instance._old_status = None
			instance._old_wachta_id = None


@receiver(post_save, sender=Zgloszenie)
def zgloszenie_post_save(sender, instance, created, **kwargs):
	if created:
		subject = f"Potwierdzenie zgłoszenia na rejs: {instance.rejs.nazwa}"
		context = {"zgl": instance,
			 "rejs": instance.rejs,
			 "link": instance.get_absolute_url() if hasattr(instance, 'get_absolute_url') else None,}
		send_simple_mail(subject, instance.email, "emails/zgloszenie_utworzone", context)
		return
	old_status = getattr(instance, "_old_status", None)
	if old_status is not None and old_status != instance.status:
		context = {"zgl": instance,
			 	"old_status": old_status,
			 	"new_status": instance.status,
			 	"link": f"{'http://localhost:8000'}" + reverse("zgloszenie_details", kwargs={"token": instance.token}),
			 	}

		if instance.status in ["QUALIFIED", "zakfalifikowany"]:
			subject = f"Potwierdzamy zakfalifikowanie na rejs  {instance.rejs.nazwa}"
			send_simple_mail(subject, instance.email, "emails/zgloszenie_potwierdzone", context)
		elif instance.status in ["odrzocone", "odrzócone"]:
			subject = f"odrzócone zgłoszenie na rejs  {instance.rejs.nazwa}"
			send_simple_mail(subject, instance.email, "emails/zgloszenie_o", context)

	old_wachta_id = getattr(instance, "_old_wachta_id", None)
	if old_wachta_id is None and instance.wachta_id is not None:
		subject = f"dodano do wachty {instance.wachta.nazwa}"
		context = {
			"zgl": instance,
			"wachta": instance.wachta,
			"link": f"{'http://localhost:8000'}" + reverse("zgloszenie_details", kwargs={"token": instance.token}),
		}
		send_simple_mail(subject, instance.email, "emails/wachta_added", context)

@receiver(post_save, sender=Wplata)
def wplata_post_save(sender, instance, created, **kwargs):
	if not created:
		return
	zgl = instance.zgloszenie
	context = {
		"zgl": zgl,
		"wplata": instance,
		"link": f"{'http://localhost:8000'}" + reverse("zgloszenie_details", kwargs={"token": zgl.token}),
	}
	if instance.rodzaj in ["wplata", "Wpłata"]:
		subject = f"Zarejestrowaliśmy nową wpłatę {zgl.imie} {zgl.nazwisko}"
		send_simple_mail(subject, zgl.email, 'emails/wplata', context)
	if instance.rodzaj in ["zwrot", "zwrot"]:
		subject = f"zwrot wpłaconych środków {zgl.imie} {zgl.nazwisko}"
	send_simple_mail(subject, zgl.email, 'emails/wplata_zwrot', context)

@receiver(post_save, sender=Ogloszenie)
def ogloszenie_post_save(sender, instance, created, **kwargs):
	if not created:
		return
	rejs = instance.rejs
	zgloszenia = rejs.zgloszenia.all()
	for z in zgloszenia:
		subject = f"Nowe ogłoszenie dla rejsu:: {rejs.nazwa}"
		context = {
			"ogloszenie": instance,
			"zgl": z,
			"rejs": rejs,
			"link": reverse("zgloszenie_details", kwargs={"token": z.token}),
		}
		send_simple_mail(subject, z.email, "emails/ogloszenie", context)
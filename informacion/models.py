from django.db import models

# Create your models here.
class Region(models.Model):
	class Meta:
		unique_together = (("codigo_estado", "codigo_municipio","codigo_parroquia"),)
		verbose_name_plural = "Regiones"
		ordering = ["codigo_estado", "codigo_municipio","codigo_parroquia"]
	codigo_estado = models.IntegerField(max_length=2, blank=False)
	codigo_municipio = models.IntegerField(max_length=2, blank=True)
	codigo_parroquia = models.IntegerField(max_length=2, blank=True)
	nombre = models.CharField(blank=False, max_length=100)
	link = models.CharField( max_length=250)

	def __unicode__(self):
		return self.nombre

class Centro(models.Model):
	class Meta:
		unique_together = (("codigo_estado", "codigo_municipio","codigo_parroquia","codigo_centro"),)
		verbose_name_plural = "Centros"
	codigo_estado = models.IntegerField(max_length=2, blank=False)
	codigo_municipio = models.IntegerField(max_length=2, blank=True)
	codigo_parroquia = models.IntegerField(max_length=2, blank=True)
	codigo_centro= models.IntegerField(max_length=3,blank=False)
	nombre = models.CharField(blank=False, max_length=100);
	link = models.CharField( max_length=250)

	def __unicode__(self):
		return self.nombre
	

class Mesa(models.Model):
	class Meta:
		unique_together = (("codigo_estado", "codigo_municipio","codigo_parroquia","codigo_centro","codigo_mesa"),)
		verbose_name_plural = "Mesas"
	codigo_estado = models.IntegerField(max_length=2, blank=False)
	codigo_municipio = models.IntegerField(max_length=2, blank=True)
	codigo_parroquia = models.IntegerField(max_length=2, blank=True)
	codigo_centro= models.IntegerField(max_length=3,blank=False)
	codigo_mesa = models.IntegerField(max_length=3,blank=False)
	eleccion = models.IntegerField(max_length=1,default=0)
	nombre = models.CharField(blank=False, max_length=100);
	ch = models.IntegerField(default=0)
	op = models.IntegerField(default=0)
	ot = models.IntegerField(default=0)
	electores = models.IntegerField(default=0)
	votantes = models.IntegerField(default=0)
	nulos = models.IntegerField(default=0)
	link = models.CharField( max_length=250)
	auditada = models.BooleanField(default=False)

	def __unicode__(self):
		return self.nombre
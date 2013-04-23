from django.contrib import admin
from informacion.models import Mesa,Region,Centro

class RegionAdmin(admin.ModelAdmin):
	list_display=['nombre','codigo_estado','codigo_municipio','codigo_parroquia','link']
	list_filter = ['codigo_estado','codigo_municipio']
	search_fields = ['codigo_estado','codigo_municipio']
	
class CentroAdmin(admin.ModelAdmin):
	list_display=['nombre','codigo_estado','codigo_municipio','codigo_parroquia','link']
	list_filter = ['codigo_estado','codigo_municipio']
	search_fields = ['codigo_estado','codigo_municipio']
	
class MesaAdmin(admin.ModelAdmin):
	list_display=['nombre','codigo_estado','codigo_municipio','codigo_parroquia','codigo_centro','link']
	list_filter = ['codigo_estado','codigo_municipio']
		

admin.site.register(Mesa,MesaAdmin)
admin.site.register(Centro,CentroAdmin)
admin.site.register(Region,RegionAdmin)
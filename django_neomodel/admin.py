from django.contrib import admin

def register(model, model_admin):
	admin.site.register([model], model_admin)
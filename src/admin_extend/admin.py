from django.contrib.admin import AdminSite


class OxidianaAdmin(AdminSite):
    index_title = "Welcome"
    site_title = "Oxidiana"
    site_header = "Oxidiana"

my_admin = OxidianaAdmin(name="admin")


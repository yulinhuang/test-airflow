# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin
from flask import request

# Creating flask appbuilder Menu Items
appbuilder_mitem_mlflow = {
    "name": "MLFlow",
    "href": "http://localhost:5000",
    "category": "External tools",
}
appbuilder_mitem_notebook = {
    "name": "Jupyter notebooks",
    "href": "http://localhost:8888",
    "category": "External tools",
}
appbuilder_mitem_minio = {
    "name": "MinIO",
    "href": "http://localhost:9000",
    "category": "External tools",
}
appbuilder_mitem_jupyterhub = {
    "name": "Jupyter Hub",
    "href": "http://{server}:8000".format(server='localhost'),
    "category": "External tools",
}
# appbuilder_mitem_toplevel = {
#     "name": "Apache",
#     "href": "https://www.apache.org/",
# }


# Defining the plugin class
class AirflowTestPlugin(AirflowPlugin):
    name = "external_tool_link_plugin"
    # appbuilder_views = [v_appbuilder_package, v_appbuilder_nomenu_package]
    appbuilder_menu_items = [
        appbuilder_mitem_mlflow, 
        appbuilder_mitem_notebook,
        appbuilder_mitem_minio,
        appbuilder_mitem_jupyterhub,
        #  appbuilder_mitem_toplevel,
    ]
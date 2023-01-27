# This is the class you derive to create a plugin
from airflow.plugins_manager import AirflowPlugin

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
# appbuilder_mitem_toplevel = {
#     "name": "Apache",
#     "href": "https://www.apache.org/",
# }


# Defining the plugin class
class AirflowTestPlugin(AirflowPlugin):
    name = "test_plugin"
    # appbuilder_views = [v_appbuilder_package, v_appbuilder_nomenu_package]
    appbuilder_menu_items = [
        appbuilder_mitem_mlflow, 
        appbuilder_mitem_notebook,              
        #  appbuilder_mitem_toplevel,
    ]
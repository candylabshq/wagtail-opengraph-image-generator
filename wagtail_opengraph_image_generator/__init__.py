default_app_config = (
    "wagtail_opengraph_image_generator.apps.WagtailOGImageGeneratorConfig"
)

VERSION = (2, 0, 0, "final")


def get_version():
    version = "{}.{}".format(VERSION[0], VERSION[1])
    if VERSION[2]:
        version = "{}.{}".format(version, VERSION[2])
    if VERSION[3] != "final":
        version = "{}.{}".format(version, VERSION[3])
    return version

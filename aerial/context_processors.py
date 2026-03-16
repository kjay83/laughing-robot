from ..employe_project import __aerial_version__

def version_renderer(request):
    return {'AERIAL_VERSION': __aerial_version__}
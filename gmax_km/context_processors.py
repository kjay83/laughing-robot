from . import __gmax_km_version__

def version_renderer(request):
    return {'GMAX_KM_VERSION': __gmax_km_version__}
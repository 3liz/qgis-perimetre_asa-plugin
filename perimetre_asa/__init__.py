__copyright__ = "Copyright 2021, 3Liz"
__license__ = "GPL version 3"
__email__ = "info@3liz.org"


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Raepa class from file Raepa.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    from .asaperimetre import AsaPerimetre
    return AsaPerimetre()

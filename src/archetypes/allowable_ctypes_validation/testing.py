from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class Archetypesallowable_Ctypes_ValidationLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import archetypes.allowable_ctypes_validation
        xmlconfig.file(
            'configure.zcml',
            archetypes.allowable_ctypes_validation,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')


ARCHETYPES_ALLOWABLE_CTYPES_VALIDATION_FIXTURE = Archetypesallowable_Ctypes_ValidationLayer()
ARCHETYPES_ALLOWABLE_CTYPES_VALIDATION_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ARCHETYPES_ALLOWABLE_CTYPES_VALIDATION_FIXTURE,),
    name="Archetypesallowable_Ctypes_ValidationLayer:Integration"
)

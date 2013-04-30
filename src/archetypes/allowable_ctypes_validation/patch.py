import logging
logger = logging.getLogger(__name__)

try:
    from Products.Archetypes.Field import Field
    from Products.Archetypes import PloneMessageFactory as _
    HAS_AT = True
except:
    HAS_AT = False
    msg = "No Archetypes found! Are you sure you need me?"
    logger.warn(msg)

# conditional backport of allowable_content_types validation
# see https://dev.plone.org/ticket/7556
# and https://github.com/collective/collective.pageheader/issues/1

VALIDATE_ALLOWABLE_CTYPES = True

if HAS_AT and not getattr(Field, 'validate_content_types', None):
    VALIDATE_ALLOWABLE_CTYPES = False

    from Acquisition import aq_get
    from types import FileType, StringType, UnicodeType

    from zope.contenttype import guess_content_type
    from zope.i18n import translate
    from zope.i18nmessageid import Message

    from Products.CMFCore.utils import getToolByName

    STRING_TYPES = [StringType, UnicodeType]

    # following methods have been copied from AT 1.8.7

    def validate(self, value, instance, errors=None, **kwargs):
        """
        Validate passed-in value using all field validators.
        Return None if all validations pass; otherwise, return failed
        result returned by validator
        """
        if errors is None:
            errors = {}
        name = self.getName()
        if errors and name in errors:
            return True

        if self.required:
            res = self.validate_required(instance, value, errors)
            if res is not None:
                return res

        if self.enforceVocabulary:
            res = self.validate_vocabulary(instance, value, errors)
            if res is not None:
                return res

        if getattr(self, 'allowable_content_types', None):
            res = self.validate_content_types(instance, value, errors)
            if res is not None:
                return res

        res = instance.validate_field(name, value, errors)
        if res is not None:
            return res

        if self.validators:
            res = self.validate_validators(value, instance, errors, **kwargs)
            if res is not True:
                return res

        # all ok
        return None

    def validate_content_types(self, instance, value, errors):
        """make sure the value's content-type is allowed"""
        if value in ("DELETE_IMAGE", "DELETE_FILE", None, ''):
            return None
        # plone.app.blob.field.BlobWrapper cannot be imported
        # at startup due to circular imports
        from plone.app.blob.field import BlobWrapper
        body = ''
        if isinstance(value, FileType):
            tell = value.tell()
            value.seek(0)
            body = value.read()
            value.seek(tell)
        elif isinstance(value, StringType):
            body = value
        elif isinstance(value, BlobWrapper):
            body = value.data

        if isinstance(value, (FileType, BlobWrapper)) and body in (None, ''):
            return None

        mtr = getToolByName(instance, 'mimetypes_registry', None)
        if mtr is not None:
            orig_filename = getattr(value, 'filename',
                                    getattr(value, 'name', ''))
            kw = dict(mimetype=None,
                      filename=orig_filename)
            try:
                d, f, mimetype = mtr(body[:8096], **kw)
            except UnicodeDecodeError:
                d, f, mimetype = mtr(len(body) < 8096 and body or '', **kw)
        else:
            mimetype, enc = guess_content_type(
                value.filename, value.read(), None)

        mimetype = str(mimetype).split(';')[0].strip()
        if mimetype not in self.allowable_content_types:
            request = aq_get(instance, 'REQUEST')
            label = self.widget.Label(instance)
            name = self.getName()
            if isinstance(label, Message):
                label = translate(label, context=request)
            error = _(u'error_allowable_content_types',
                      default=u'Mimetype ${mimetype} is not allowed '
                      'on ${name}, please correct.',
                      mapping={
                          'mimetype': mimetype,
                          'name': label
                      })
            error = translate(error, context=request)
            errors[name] = error
            return error

        return

    # PATCHING!

    # replace validate method
    Field.old_validate = Field.validate
    Field.validate = validate
    # add validate_content_types
    Field.validate_content_types = validate_content_types

    msg = "PATCHED Products.Archetypes.Field for adding \
    allowable_content_types validation!"
    logger.warn(msg)

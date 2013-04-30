.. contents::

Introduction
============

Previous to Products.Archetypes 1.8.7 there was not validation onto `allowable_content_types` field's attribute.

This attribute is very important cause it allows to constrain the type of content to be put in field.

Uploading a PDF file to an image field breaks the object (no edit, no view at all).

Version 1.8.7 fixes this bug https://dev.plone.org/ticket/7556.

I met this problem here https://github.com/collective/collective.pageheader/issues/1 so I decided to solve it for all the previous version of AT.


Please, report issues or ideas here https://github.com/simahawk/archetypes.allowable_ctypes_validation/issues.

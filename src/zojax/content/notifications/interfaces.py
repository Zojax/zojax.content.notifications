##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
from zope import interface, schema
from zope.i18nmessageid import MessageFactory
from z3c.schema.email import RFC822MailAddress

_ = MessageFactory('zojax.content.notifications')


class IContentNotification(interface.Interface):
    """ content notification """

    title = schema.TextLine(
        title = u'Notification title',
        required = True)

    description = schema.TextLine(
        title = u'Notification description',
        required = True)

    type = interface.Attribute('Type')

    def create(principal=None):
        """ create subscription object """

    def subscribe(principal=None):
        """ subscribe to notification """

    def unsubscribe(principal=None):
        """ unsubscribe to notification  """

    def isSubscribed(principal=None):
        """ check if current principal subscribed """

    def getSubscription(principal=None):
        """ get current principal subscription """

    def isSubscribedInParents(context=None, principal=None):
        """ check if current principal subscribed for parents objects """

    def getSubscribers(context):
        """ return subrcibed principals """


class INotificationMailTemplate(interface.Interface):
    """ notification mail template """


class INotificationsPreferences(interface.Interface):
    """ email notifications management """


class INotificationsContexts(interface.Interface):
    
    def getContexts(**params):
        """ return contexts """

class IContentNotifications(interface.Interface):
    """ Content Notifications configlet """

    notification_from_name = schema.TextLine(
        title = _(u"Notification 'From' name"),
        default = u'Portal administrator',
        required = True)

    notification_from_address = RFC822MailAddress(
        title = _(u"Notification 'From' address"),
        default = u'noreply@norep.ly',
        required = True)

    notification_replyto_name = schema.TextLine(
        title = _(u"Notification 'Reply-to' name"),
        default = u'Portal administrator',
        required = True)

    notification_replyto_address = RFC822MailAddress(
        title = _(u"Notification 'Reply-to' address"),
        default = u'noreply@norep.ly',
        required = True)
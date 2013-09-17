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
from zope import interface, component
from zope.component import getAdapters
from zope.traversing.browser import absoluteURL
from zope.app.security.interfaces import IUnauthenticatedPrincipal
from zojax.content.actions.action import Action
from zojax.content.type.interfaces import IContent
from zojax.content.actions.interfaces import IAction, INotificationCategory

from interfaces import _, IContentNotification


class INotificationsAction(IAction, INotificationCategory):
    """ action """


class NotificationsAction(Action):
    interface.implements(INotificationsAction)
    component.adapts(IContent, interface.Interface)

    weight = 999998
    title = _(u'Email notifications')

    @property
    def url(self):
        return '%s/notifications'%(absoluteURL(self.context, self.request))

    def isAvailable(self):
        if IUnauthenticatedPrincipal.providedBy(self.request.principal):
            return False

        for name, adapter in getAdapters((self.context,), IContentNotification):
            return True

        return False

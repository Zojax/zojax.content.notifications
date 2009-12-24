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
from zope import interface
from zope.component import getAdapters, getAdapter, queryAdapter
from zojax.statusmessage.interfaces import IStatusMessage

from interfaces import _, IContentNotification


class Notifications(object):

    def listNotifications(self):
        notifications = []
        for name, notification in getAdapters(
            (self.context,), IContentNotification):
            notifications.append((notification.title, name, notification))

        notifications.sort()
        return [notification for title, name, notification in notifications]

    def update(self):
        request = self.request

        if 'form.button.subscribe' in request:
            ids = request.get('ids', ())

            for name, notification in getAdapters(
                (self.context,), IContentNotification):

                if name in ids:
                    notification.subscribe()
                else:
                    notification.unsubscribe()

            IStatusMessage(request).add(
                _('Email notification subscriptions have been updated.'))

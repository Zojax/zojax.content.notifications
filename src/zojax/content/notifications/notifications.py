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
from zojax.content.notifications.notification import Notification
from zope import interface
from zope.component import adapts, getAdapters, getAdapter, \
                           getUtility, queryAdapter
from zope.proxy import removeAllProxies
from zope.app.component.interfaces import ISite
from zope.app.component.hooks import getSite
from zope.app.intid.interfaces import IIntIds

from zojax.statusmessage.interfaces import IStatusMessage
from interfaces import _, IContentNotification, INotificationsContexts
from zojax.authentication.utils import getPrincipal
from zojax.principal.profile.interfaces import IPersonalProfile
from zope.traversing.browser import absoluteURL


class Notifications(object):

    def listNotifications(self):
        notifications = []
        for name, notification in getAdapters(
            (self.context,), IContentNotification):
            notifications.append((notification.title, name, notification))

        notifications.sort()
        return [notification for title, name, notification in notifications]

    def listSubscribers(self, notification):
        profiles = [IPersonalProfile(getPrincipal(subscriber)) for subscriber in notification.getSubscribers(self.context)]
        return [(profile.title, absoluteURL(profile.space, self.request)) for profile in profiles]

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


class NotificationsContexts(object):
    
    adapts(None)
    interface.implements(INotificationsContexts)
    
    
    def __init__(self, context):
        self.context = context
        
    def getContexts(self, *objects, **params): 
        context = self.context
        ids = getUtility(IIntIds)
        context = removeAllProxies(context)
    
        contexts = []
    
        while True:
            id = ids.queryId(context)
            if id is not None:
                contexts.append(id)
    
            context = context.__parent__
            if context is None or ISite.providedBy(context):
                break
    
        contexts.append(ids.queryId(getSite()))
        return contexts
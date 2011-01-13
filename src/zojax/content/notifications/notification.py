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
from zojax.content.notifications.interfaces import INotificationsContexts
"""

$Id$
"""
from zope import interface
from zope.proxy import removeAllProxies
from zope.component import getUtility
from zope.app.intid.interfaces import IIntIds
from zope.app.component.hooks import getSite
from zope.app.component.interfaces import ISite
from zojax.mail.interfaces import IMailAddress
from zojax.subscription.utils import getPrincipal
from zojax.subscription.interfaces import ISubscriptions
from zojax.subscription.subscription import Subscription


class Notification(object):

    type = ''

    def __init__(self, context):
        self.context = context

    def create(self, principal=None):
        return Subscription(principal, type=self.type)

    def subscribe(self, principal=None):
        if principal is None:
            principal = getPrincipal().id
        if not self.isSubscribed(principal):
            getUtility(ISubscriptions).add(self.context, self.create(principal))

    def unsubscribe(self, principal=None):
        if principal is None:
            principal = getPrincipal().id
        getUtility(ISubscriptions).removeSubscription(
            self.context, principal, self.type)

    def isSubscribed(self, principal=None):
        return self.getSubscription(principal) is not None

    def isSubscribedInParents(self, context=None, principal=None):
        if principal is None:
            principal = getPrincipal().id

        ids = getUtility(IIntIds)

        if context is None:
            context = self.context

        contexts = INotificationsContexts(context).getContexts()

        if getUtility(ISubscriptions).search(
            object = {'any_of': contexts}, principal={'any_of': (principal,)},
            visibility = None, type = {'any_of': (self.type,)}):
            return True

        return False

    def getSubscribers(self, context):
        ids = getUtility(IIntIds)
        context = removeAllProxies(context)

        contexts = INotificationsContexts(context).getContexts()

        principals = set()
        for subs in getUtility(ISubscriptions).search(
            object = {'any_of': contexts}, type = {'any_of': (self.type,)}):

            principals.add(subs.principal)

        return principals

    def getSubscription(self, principal=None):
        if principal is None:
            principal = getPrincipal().id

        try:
            return getUtility(ISubscriptions).search(
                object = self.context, principal={'any_of': (principal,)},
                visibility = None, type = {'any_of': (self.type,)})[0]
        except IndexError:
            return None

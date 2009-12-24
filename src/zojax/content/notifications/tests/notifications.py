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
from zope.component import getUtility, getAdapter
from zojax.subscription.interfaces import SubscriptionException
from zojax.subscription.interfaces import ISubscriptionDescription
from zojax.content.notifications.utils import sendNotification
from zojax.content.notifications.notification import Notification

from interfaces import ICommentsNotification


class CommentsNotification(Notification):
    component.adapts(interface.Interface)
    interface.implementsOnly(ICommentsNotification)

    type = u'comments'
    title = u'Recent comments'
    description = u'Recently added comments.'


class CommentsNotificationDescription(object):
    interface.implements(ISubscriptionDescription)

    type = u'comments'
    title = u'Recent comments'
    description = u'Recently added comments.'

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
from email.Utils import formataddr
from zope.proxy import removeAllProxies
from zope.component import getUtility, queryMultiAdapter
from zope.security.management import queryInteraction
from zope.app.intid.interfaces import IIntIds
from zope.app.component.hooks import getSite
from zope.app.component.interfaces import ISite
from zojax.mail.interfaces import IMailAddress
from zojax.subscription.utils import getPrincipals
from zojax.subscription.interfaces import ISubscriptions

from interfaces import INotificationMailTemplate, INotificationsContexts


def getRequest():
    interaction = queryInteraction()

    if interaction is not None:
        for participation in interaction.participations:
            if participation is not None:
                return participation


def getSubscribers(types, *objects, **params):
    ids = getUtility(IIntIds)
    context = removeAllProxies(objects[0])

    contexts = INotificationsContexts(context).getContexts(*objects, **params)

    if isinstance(types, basestring):
        types = (types,)

    principals = set()
    for subs in getUtility(ISubscriptions).search(
        object = {'any_of': contexts},
        type = {'any_of': types}, **params):

        principals.add(subs.principal)

    return principals


def sendNotification(types, *objects, **params):
    template = queryMultiAdapter(
        (tuple(objects) + (getRequest(),)), INotificationMailTemplate)
    if template is None:
        return

    principals = getSubscribers(types, *objects, **params)

    if principals:
        emails = set()
        for principal in getPrincipals(principals):
            mail = IMailAddress(principal, None)
            if mail is not None:
                emails.add(formataddr((principal.title, mail.address)))

        if emails:
            template.update()

            if not template.hasHeader('Reply-to'):
                template.addHeader('Reply-to', 'noreply@noreply', False)

            template.send(emails)

    return principals

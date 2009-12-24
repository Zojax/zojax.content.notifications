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
from zope.component import getUtility, getAdapter, queryMultiAdapter
from zope.traversing.browser import absoluteURL
from zojax.content.type.interfaces import IContentViewView
from zojax.statusmessage.interfaces import IStatusMessage
from zojax.subscription.interfaces import ISubscriptions, ISubscriptionDescription

from interfaces import _, IContentNotification


class PreferenceView(object):

    def listSubscriptions(self):
        types = {}
        subscriptions = {}

        request = self.request

        for subs in getUtility(ISubscriptions).principalSubscriptions(
            self.context.__principal__.id):

            if subs.type not in types:
                types[subs.type] = getUtility(ISubscriptionDescription, subs.type)

            typeObject = types.get(subs.type)

            data = subscriptions.setdefault(typeObject, [])

            content = subs.object

            view = queryMultiAdapter((content, request), IContentViewView)
            try:
                if view is not None:
                    url = '%s/%s'%(absoluteURL(content, request), view.name)
                else:
                    url = '%s/'%absoluteURL(content, request)
            except:
                url = u''

            info = {'id': subs.id,
                    'url': url,
                    'title': getattr(content, 'title', content.__name__),
                    'description': getattr(content, 'description', u'')}

            data.append(info)

        subscriptions = [(tp.title, {'tp':tp, 'data':data})
                         for tp, data in subscriptions.items()]
        subscriptions.sort()

        return [info for t, info in subscriptions]

    def update(self):
        request = self.request

        if 'button.unsubscribe' in request:
            principal = self.context.__principal__.id
            subscriptions = getUtility(ISubscriptions)

            for id in request.get('ids', ()):
                subscriptions.unsubscribePrincipal(principal, int(id))

            IStatusMessage(request).add(_(u'Subscriptions have been updated.'))

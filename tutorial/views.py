from pyramid.view import (
    view_config,
    view_defaults
    )


@view_defaults(route_name='hello')
class TutorialViews(object):
    def __init__(self, request):
        self.request = request
        self.view_name = 'TutorialViews'

    # Retrieving /howdy/first/last the first time
    @view_config(renderer='hello.pt')
    def hello(self):
        return {'page_title': 'Hello View'}

    # Posting to /howdy/first/last via the "Edit" submit button
    @view_config(request_method='POST', renderer='edit.pt')
    def rate(self):
        one = int(self.request.params['user'])
        two = int(self.request.params['movie'])
        return {'page_title': 'Edit View', 'new_name': one+two}

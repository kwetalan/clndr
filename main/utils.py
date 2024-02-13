from datetime import datetime

class DataMixin():
    def get_data(self, **kwargs):
        kwargs['y'] = datetime.now().year
        kwargs['m'] = datetime.now().month
        kwargs['d'] = datetime.now().day
        kwargs['is_auth'] = self.request.user.is_authenticated
        kwargs['user'] = self.request.user
        return kwargs
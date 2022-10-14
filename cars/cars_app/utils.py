from cars_app.models import Category


menu = ({"title": "Home", "url_name": "home"},
        {"title": "About", "url_name": "about"},
        {"title": "Add article", "url_name": "addarticle"},
        {"title": "Feedback", "url_name": "feedback"})


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        categories = Category.objects.all()
        context['menu'] = menu
        context['categories'] = categories
        return context
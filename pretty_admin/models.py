from django.db import models
from django.urls import reverse


class BaseModel(models.Model):

    class Meta:
        abstract = True

    @staticmethod
    def external_link(url, text, target='_blank'):
        return u"<a target='{target}' class='external_link' href='{url}'><img src='/static/img/external-link.svg' class='svg external_link'></img> {text} </a>" \
            .format(url=url, text=text, target=target)

    @staticmethod
    def internal_link(url, text, target='_blank'):
        return u"<a target='{target}' class='internal_link' href='{url}'><img src='/static/img/internal-link.svg' class='svg internal_link'></img> {text} </a>" \
            .format(url=url, text=text, target=target)

    @property
    def admin_edit_url(self):
        return reverse("admin:%s_%s_change" %
                       (self._meta.app_label, self._meta.model_name), args=(self.pk,))

    def admin_edit_link(self, url_text="Edit"):
        return self.internal_link(self.admin_edit_url, url_text)

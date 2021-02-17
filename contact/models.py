from django.forms import widgets


from django.db import models

from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel
)
from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractFormField
)


class FormField(AbstractFormField):
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields',
    )


class ContactPage(AbstractEmailForm):

    template = "contact/contact_page.html"
    # This is the default path.
    # If ignored, Wagtail adds _landing.html to your template name
    landing_page_template = "contact/contact_page_landing.html"

    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label='Form Fields'),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel("subject"),
        ], heading="Email Settings"),
    ]

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        # form = super(AbstractEmailForm, self).get_form(*args, **kwargs)  # use this syntax for Python 2.x
        # iterate through the fields in the generated form
        for name, field in form.fields.items():
            # here we want to adjust the widgets on each field
            # if the field is a TextArea - adjust the rows
            if isinstance(field.widget, widgets.Textarea):
                field.widget.attrs.update({'rows': '5'})
            # for all fields, get any existing CSS classes and add 'form-control'
            # ensure the 'class' attribute is a string of classes with spaces
            css_classes = field.widget.attrs.get('class', '').split()
            css_classes.append('form-control')
            field.widget.attrs.update({'class': ' '.join(css_classes)})
        return form


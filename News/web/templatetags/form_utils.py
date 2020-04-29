import types

from django import template

register = template.Library()


def as_widget(self, widget=None, attrs=None, only_initial=False):
    """
    Render the field by rendering the passed widget, adding any HTML
    attributes passed as attrs. If a widget isn't specified, use the
    field's default widget.
    """
    widget = widget or self.field.widget
    if self.field.localize:
        widget.is_localized = True
    attrs = attrs or {}
    attrs.update(self._attrs)
    attrs = self.build_widget_attrs(attrs, widget)
    if self.auto_id and 'id' not in widget.attrs:
        attrs.setdefault('id', self.html_initial_id if only_initial else self.auto_id)
    return widget.render(
        name=self.html_initial_name if only_initial else self.html_name,
        value=self.value(),
        attrs=attrs,
        renderer=self.form.renderer,
    )


@register.filter
def add_attr(field, value):
    values = value.split(':')
    property_ = values[0]
    value_ = values[1]
    as_widget_method = types.MethodType(as_widget, field)
    setattr(field, 'as_widget', as_widget_method)
    setattr(field, '_attrs', {property_: value_})
    return field

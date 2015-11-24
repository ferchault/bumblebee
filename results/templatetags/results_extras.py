from django import template
register = template.Library()


@register.filter(name='add_attributes')
def add_attributes(field, css):
    attrs = {}
    definition = css.split(',')

    for d in definition:
        if ':' not in d:
            attrs['class'] = d
        else:
            t, v = d.split(':')
            attrs[t] = v

    return field.as_widget(attrs=attrs)


@register.filter(name='form_explain')
def add_attributes(form):
    return form.Meta.model.explain()


@register.filter
def fieldtype(obj):
    return obj.__class__.__name__


@register.simple_tag
def value_to_string(field, object):
	if field.__class__.__name__ == 'ForeignKey':
		return getattr(object, field.name)
	return field.value_to_string(object)

@register.simple_tag
def column_content(field, object):
	column = getattr(object, field)
	try:
		return column()
	except:
		return column

@register.simple_tag
def column_header(field, object):
	column = getattr(object, field)
	try:
		return object.alias[field]
	except:
		pass
	try:
		return column.verbose_name
	except:
		return field

@register.filter(name='is_boolean_field')
def is_boolean_field(field):
	return field.field.__class__.__name__ == 'BooleanField'

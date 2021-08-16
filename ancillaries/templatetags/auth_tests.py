from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def manager_test(context):
    """ Template tag to check if user is a manager or admin """
    u_type = context['profile'].user_type.type.lower()
    if u_type == 'manager' or u_type == 'admin':
        return True
    else:
        return False


@register.simple_tag(takes_context=True)
def stock_test(context):
    """ Template tag to check if user is a manager,
    admin or stock controller """
    u_type = context['profile'].user_type.type.lower()
    if u_type in ('stock controller', 'admin', 'manager'):
        return True
    else:
        return False


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


@register.simple_tag(takes_context=True)
def job_test(context):
    """
    Template tag to check if user is an admin,
    manager, created the job, was assigned to the job,
    or the job is unassigned
    """
    job = context['job']
    user = context['profile']
    user_type = user.user_type.type.lower()
    if user_type in ('admin', 'manager'):
        return True
    elif job.created_by == user.user:
        return True
    elif user.user in job.assigned_to.all():
        return True
    elif job.assigned_to.count() == 0:
        return True
    else:
        return False

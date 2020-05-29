from django import template


register = template.Library()


@register.filter()
def percentage(amount, total):
    try:
        print(total)
        return '{:1.f$'.format(amount / int(total) * 100)
    except ZeroDivisionError:
        return None
    except ValueError:
        return total

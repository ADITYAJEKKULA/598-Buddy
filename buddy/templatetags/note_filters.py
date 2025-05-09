from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def truncate_lines(text, num_lines):
    """
    Truncates text to the first num_lines and appends an ellipsis if truncated.
    Returns a tuple: (truncated_text, was_truncated).
    """
    if not isinstance(text, str):
        # Handle non-string input gracefully
        return (text, False)

    lines = text.splitlines()
    was_truncated = len(lines) > num_lines

    if was_truncated:
        truncated_text = "\n".join(lines[:num_lines]) + "..."
    else:
        truncated_text = text

    # We don't need mark_safe here as we are just adding text and '...'
    # If we were adding HTML tags like <br>, mark_safe would be necessary.
    return (truncated_text, was_truncated)
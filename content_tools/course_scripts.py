"""Load a lesson's interactive experiment when the reader approaches it."""
from html import escape


def lab_loader(item, topic, versioned_asset):
    base = f'/static/tutorials/{topic}/'
    libraries = ' '.join(versioned_asset(base + dep) for dep in item.get('scripts', []))
    script = versioned_asset(base + item['id'].lower() + '.js')
    loader = versioned_asset('/static/js/course-plot-loader.js')
    return (f'<script src="{loader}" defer data-lab="{escape(item["id"], quote=True)}-lab" '
            f'data-libraries="{escape(libraries, quote=True)}" data-script="{script}"></script>')

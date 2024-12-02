from jinja2 import Environment, FileSystemLoader, select_autoescape, nodes
from jinja2_simple_tags import StandaloneTag
import os, shutil

# custom tag disables the link to the page you're currently on
class LinkExtension(StandaloneTag):
    safe_output = True
    tags = {'link'}

    def render(self, path='/index.htm', loc='/index.htm', title='home'):
        print(path, loc)
        if path.split('/')[1] == loc:
            return '<a style="pointer-events: none;" class="navbar-item"><span class="title is-5">' \
                + title + '</span></a>'
        else:
            return '<a class="navbar-item" href="' + path + '">' + title + '</a>'

# builds the path to move files
def target_for(path):
    if 'pages' in path:
        return path.replace('pages', 'build')
    else:
        return 'build/' + path

# creates directory if not available
def mkdir_for(path):
    target_dir = os.path.dirname(path)
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

# selects only relevant html / htm files
def filter_path(path: str):
    return (os.path.splitext(path)[1] in ['.html', '.htm']) and (
        os.path.splitext(path)[0] not in ['base', 'article']
    )

# renders html files and copies to build directory
def copy_files(env, context):
    for template in env.list_templates(filter_func=filter_path):
        context['loc'] = template.split('/')[1]
        target_path = target_for(template)
        rendered = env.get_template(template).render(**context)
        mkdir_for(target_path)

        with open(target_path, 'w') as f:
            f.write(rendered)

# copies static files to build directory
def copy_static(env):
    for static in env.list_templates(
        filter_func=lambda path: os.path.splitext(path)[1] not in ['.html', '.htm']
    ):
        target_path = target_for(static)
        mkdir_for(target_path)

        shutil.copy('./resources/' + static, './' + target_path)


def main():
    env = Environment(
        loader=FileSystemLoader('resources/'),
        autoescape=select_autoescape(['html', 'htm', 'xml']),
        extensions=[LinkExtension]
    )
    context = {'temp': 'This is testing passing context.'}
    copy_files(env, context)
    copy_static(env)


if __name__ == '__main__':
    main()

import os
import logging

log = logging.getLogger()


class TemplateGenerator:
    BASE_HTML = '''{% load static %}
    <!DOCTYPE HTML>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Document</title>
        <link rel="stylesheet" href="">
    </head>
    <body>
        <div class="nav">
            <a href="{% url 'home' %}">Home</a> |
            <a href="{% url 'about' %}">About</a> |
            <hr>
        </div>
    
        {% block content %}
        {% endblock content %}
        <script src="" type=""></script>
    </body>
    </html>
    '''

    INDEX_HTML = '''<!doctype html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Document</title>
        <link rel="stylesheet" href="assets/css/style.css">
        <link rel="stylesheet" href="assets/css/bootstrap.min.css">
    </head>
    <body>
        <p>Hello, Template!</p>
    
        <script type="text/javascript" src="assets/js/script.js"></script>
        <script type="text/javascript" src="assets/js/bootstrap.min.js"></script>
        
    </body>
    </html>
    '''

    DJANGO_PAGE_HTML = '''<!DOCTYPE HTML>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport"
              content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>Document</title>
        <link rel="stylesheet" href="">
    </head>
    <body>
        {% extends 'base.html' %}
    
        {% block content %}
        {% endblock content %}
        <script src="" type=""></script>
    </body>
    </html>
    '''

    SCRIPT_JS = '''\"use strict\";
    
    function main () {
        console.log("Hello, World!");
    }
    
    document.onload = main();
    '''

    STYLE_CSS = '''/* Styles go here. */
    
    p {
        color: red;
    }
    '''

    DJANGO_TEMPLATE = {
        'templates_folder': 'templates',
        'template_files': [
            {'templates/base.html': BASE_HTML},
            {'templates/home.html': DJANGO_PAGE_HTML},
            {'templates/about.html': DJANGO_PAGE_HTML}
        ],
        'static_folder': 'static',
        'static_js_folder': 'static/js',
        'static_js_files': [{'static/js/script.js': SCRIPT_JS}],
        'static_css_folder': 'static/css',
        'static_css_files': [{'static/css/style.css': STYLE_CSS}]
}

    NATIVE_TEMPLATE = {
        'assets_folder': 'assets',
        'js_folder': 'assets/js',
        'css_folder': 'assets/css',
        'images_folder': 'assets/images',
        'index_files': [{'index.html': INDEX_HTML}],
        'js_files': [{'assets/js/script.js': SCRIPT_JS}],
        'css_files': [{'assets/css/style.js': STYLE_CSS}]
    }

    def __init__(
        self,
        template_path: str = '',
        template_type: str = 'native',
    ) -> None:

        self.template_path, self.template_type = template_path, template_type
        self.templates = {
            'native': self.NATIVE_TEMPLATE,
            'django': self.DJANGO_TEMPLATE
        }

    def __str__(self):
        return vars(self)

    def create_template(self):
        log.info(f'Creating {self.template_type} template.')

        for file_object, file_path in self.templates[self.template_type].items():
            if 'folder' in file_object:
                folder_path = os.path.join(self.template_path, file_path)

                try:
                    log.info(f'Creating folder {folder_path}.')
                    os.makedirs(folder_path)

                except FileExistsError as e:
                    log.error(f'Folder {folder_path} already exists.')
                    continue

            else:
                for file in file_path:
                    for file_name, content in file.items():
                        new_file_path = os.path.join(self.template_path, file_name)

                        try:
                            log.info(f'Writing file {new_file_path}')

                            with open(new_file_path, 'w') as f:
                                f.write(content)

                        except FileExistsError:
                            log.error(f'File {new_file_path} already exists')

                        except IOError as e:
                            log.error(f'Error writing file:\n{e}', exc_info=True)

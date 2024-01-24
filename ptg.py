#!/usr/bin/env python
import configargparse
import logging
import json
import sys

from generator.generator import TemplateGenerator
from api.downloader import ResourceDownloader


parser = configargparse.get_argument_parser(
    description='Configuration options for project template generator',
    formatter_class=configargparse.ArgumentDefaultsRawHelpFormatter
)

parser.add_argument('-p', '--path', type=str, default='template',
                    help='Path of the new project.')

parser.add_argument('-t', '--type', type=str, default='native',
                    help='The type of project (native | django | flask)')

parser.add_argument('-l', '--log-level', type=str, default='info')

parser.add_argument('-d', '--download-resources', action='store_true',
                    default=False, help='Download additional resources, i.e., bootstrap.')

cfg = parser.parse_known_args()[0]

logging.basicConfig(
    format='%(process)d - %(asctime)s - %(levelname)s: %(message)s',
    datefmt='%H:%M:%S',
    level=logging.getLevelName(cfg.log_level.upper()),
    handlers=[logging.StreamHandler(sys.stdout)]
)

log = logging.getLogger()
log.debug(json.dumps(vars(cfg), indent=4))

if __name__ == '__main__':
    TemplateGenerator(template_type=cfg.type, template_path=cfg.path).create_template()
    ResourceDownloader(target_file_path=cfg.path, project_type=cfg.type).get_bootstrap()

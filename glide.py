#!/usr/bin/env python

"""Glide

Usage:
  glide.py show-projects
  glide.py create-project <project_name>
  glide.py select-project <project_name>
  glide.py show-themes
  glide.py show-layouts <theme_name>
  glide.py show-pages
  glide.py create-page <page_name> <theme_name> <layout_name>
  glide.py build
  glide.py test
  glide.py launch
  glide.py (-h | --help)
  glide.py --version

Options:
  -h --help     Shows this screen.
  --version     Shows version.

"""

import os
import sys
import shutil
import logging
from docopt import docopt
import pathlib
import simplejson as json
import yaml
from jinja2 import Template
from bs4 import BeautifulSoup

from projectmanager import ProjectManager


# 
# Globals
# 
config = None
logger = None
# projectName = ''
# pageName = ''
# themeName = ''
# layoutName = ''


# 
# Start
# 
if __name__ != '__main__':
  sys.exit(0)


# 
# Load configuration file
# 
try:
  with open('config/config.json', 'r') as configFile:
    config = json.load(configFile)
except FileNotFoundError:
  logger.error('Cannot find the config file.')
  sys.exit(1)


# 
# Setup logger
# 
if config['debuggingMode']:
  loggingLevel = logging.DEBUG
  # logFormat = '[%(asctime)s] %(levelname)s : %(message)s'
else:
  loggingLevel = logging.INFO
logFormat = '%(message)s'
logging.basicConfig(level=loggingLevel, format=logFormat)
logger = logging.getLogger()


# 
# Setup configurations
# 
rootPath = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
templateRootPath = rootPath / config['templateSettings']['path']
dataRootPath = rootPath / config['userdataSettings']['path']
outputRootPath = rootPath / config['outputSettings']['path']


# 
# Handle commands
# 
print()
args = docopt(__doc__, version='Glide v0.1')

if args['show-projects']:
  ProjectManager.showProjects(dataRootPath)

elif args['create-project']:
  ProjectManager.createProject(dataRootPath, outputRootPath, args['<project_name>'])

elif args['select-project']:
  ProjectManager.selectProject(dataRootPath, outputRootPath, args['<project_name>'])

elif args['show-themes']:
  ProjectManager.showThemes()

elif args['show-layouts']:
  ProjectManager.showLayouts(args['<theme_name>'])

elif args['show-pages']:
  ProjectManager.showPages(dataRootPath)

elif args['create-page']:
  ProjectManager.createPage(dataRootPath, args['<page_name>'], args['<theme_name>'], args['<layout_name>'])

elif args['build']:
  ProjectManager.build()

elif args['test']:
  ProjectManager.test()

elif args['launch']:
  ProjectManager.launch()

else:
  logger.error('Command unidentified')
  sys.exit(1)
print()


# # 
# # Load templates
# # 
# htmlTemp = ''
# data = None
# with open(str(templateRootPath / themeName / layoutName / '{}.html'.format(layoutName)), 'r') as htmlTempF:
#   htmlTemp = htmlTempF.read()
# with open(str(dataPath / '{}.yml'.format(pageName)), 'r') as dataF:
#   data = yaml.load(dataF.read())


# # 
# # TODO: General format verification
# # 


# # 
# # TODO: Segmentation
# # 


# # 
# # TODO: Grammar check for each segment
# # 


# # 
# # Fill out the HTML template
# # 
# template = Template(htmlTemp)
# res = template.render(data)
# # logger.debug(res)


# # 
# # Output the rendered page
# # 
# if not projectPath.exists():
#   projectPath.mkdir()
# with open(str(projectPath / '{}.html'.format(pageName)), 'w') as outputF:
#   outputF.write(res)
#   outputF.close()
#   logger.info('Generated %s.html', pageName)


# # 
# # Copy required resources
# #
# themeCssSrcPath = str(templateRootPath / themeName / '{}.css'.format(themeName))
# themeCssDstPath = str(projectPath / '{}.css'.format(themeName))
# shutil.copyfile(themeCssSrcPath, themeCssDstPath)
# glideJsSrcPath = str(glideRootPath / 'resources' / 'js' / 'glide.js')
# glideJsDstPath = str(projectPath / 'glide.js')
# shutil.copyfile(glideJsSrcPath, glideJsDstPath)


# # # # # # # # # # # # # # # # # # 
# #  Not using Glidefile for now; # 
# # # # # # # # # # # # # # # # # # 


# # 
# # Make the sequence in this project's Glidefile or append the new page
# # 
# # if not glideFile.exists():
# #   # It's the first page of the project. Make a new Glidefile.
# #   with open(str(glideFile), 'w') as outputF:
# #     outputF.write(pageName + '\n')
# #     outputF.close()
# # else:
# #   # Glidefile exists. Append the new page.
# #   with open(str(glideFile), 'a') as outputF:
# #     outputF.write(pageName + '\n')
# #     outputF.close()


# # 
# # Connect sequential pages using Glidefile (click to next)
# # 
# # pages = None
# # with open(str(glideFile), 'r') as inputF: # existence guaranteed
# #   pages = inputF.read().split('\n')
# # for index, page in enumerate(pages):
# #   if index == len(pages) - 1:
# #     break
# #   htmlContent = ''
# #   htmlParser = None
# #   # Update the output files
# #   with open(str(projectPath / '{}.html'.format(page)), 'r') as inputF:
# #     htmlContent = inputF.read()
# #     htmlParser = BeautifulSoup(htmlContent, 'html5lib')
# #     tags = htmlParser.select('.click-to-next')
# #     for tag in tags:
# #       tag['data-next-page'] = pages[index + 1]
# #   with open(str(projectPath / '{}.html'.format(page)), 'w') as outputF:
# #     outputF.write(htmlParser.prettify(formatter='html'))
# #     outputF.close()
# #     logger.info('Updated Glidefile')

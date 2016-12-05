# For later use:
# Project bolierplate - cookiecutter-django:
# https://github.com/pydanny/cookiecutter-django

# For later use:
# Interactive commandline tool - Click
# http://click.pocoo.org/5/

import os
import sys
import pathlib
import shutil
import logging
import simplejson as json
import yaml
from jinja2 import Template
from bs4 import BeautifulSoup


# 
# Globals
# 
config = None
logger = None
projectName = ''
pageName = ''
themeName = ''
layoutName = ''


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
  logger.info('Cannot find the config file.')
  sys.exit(1)


# 
# Setup logger
# 
if config['debuggingMode']:
  loggingLevel = logging.DEBUG
else:
  loggingLevel = logging.INFO
logFormat = '[%(asctime)s] %(levelname)s : %(message)s'
logging.basicConfig(level=loggingLevel, format=logFormat)
logger = logging.getLogger()


# 
# Command-line arguments
# 
if len(sys.argv) != 5:
  logger.info('Specify your command-line arguments.')
  logger.info('For example, run python glide.py [projectName] [pageName] [themeName] [layoutName]')
  sys.exit(0)
else:
  projectName = sys.argv[1]
  pageName = sys.argv[2]
  themeName = sys.argv[3]
  layoutName = sys.argv[4]


# 
# Setup configurations
# 
glideRootPath = pathlib.Path(os.path.dirname(os.path.abspath(__file__)))
templateRootPath = pathlib.Path(glideRootPath / config['templateSettings']['path'])
dataPath = glideRootPath / config['userdataSettings']['path']
outputPath = glideRootPath / config['outputSettings']['path']
projectPath = outputPath / projectName
glideFile = projectPath / '{}.glide'.format(projectName)
logger.info('Looking for tempaltes in %s', templateRootPath)
logger.info('Looking for user data in %s', dataPath)


# 
# Load templates
# 
htmlTemp = ''
data = None
with open(str(templateRootPath / themeName / layoutName / '{}.html'.format(layoutName)), 'r') as htmlTempF:
  htmlTemp = htmlTempF.read()
with open(str(dataPath / '{}.yml'.format(pageName)), 'r') as dataF:
  data = yaml.load(dataF.read())


# 
# TODO: General format verification
# 


# 
# TODO: Segmentation
# 


# 
# TODO: Grammar check for each segment
# 


# 
# Fill out the HTML template
# 
template = Template(htmlTemp)
res = template.render(data)
# logger.debug(res)


# 
# Output the rendered page
# 
if not projectPath.exists():
  projectPath.mkdir()
with open(str(projectPath / '{}.html'.format(pageName)), 'w') as outputF:
  outputF.write(res)
  outputF.close()
  logger.info('Generated %s.html', pageName)


# 
# Copy required resources
#
themeCssSrcPath = str(templateRootPath / themeName / '{}.css'.format(themeName))
themeCssDstPath = str(projectPath / '{}.css'.format(themeName))
shutil.copyfile(themeCssSrcPath, themeCssDstPath)
glideJsSrcPath = str(glideRootPath / 'resources' / 'js' / 'glide.js')
glideJsDstPath = str(projectPath / 'glide.js')
shutil.copyfile(glideJsSrcPath, glideJsDstPath)


# 
# Make the sequence in this project's Glidefile or append the new page
# 
if not glideFile.exists():
  # It's the first page of the project. Make a new Glidefile.
  with open(str(glideFile), 'w') as outputF:
    outputF.write(pageName + '\n')
    outputF.close()
else:
  # Glidefile exists. Append the new page.
  with open(str(glideFile), 'a') as outputF:
    outputF.write(pageName + '\n')
    outputF.close()

# 
# Connect sequential pages (click to next)
# 
pages = None
with open(str(glideFile), 'r') as inputF: # existence guaranteed
  pages = inputF.read().split('\n')
for index, page in enumerate(pages):
  if index == len(pages) - 1:
    break
  htmlContent = ''
  htmlParser = None
  # Update the output files
  with open(str(projectPath / '{}.html'.format(page)), 'r') as inputF:
    htmlContent = inputF.read()
    htmlParser = BeautifulSoup(htmlContent, 'html5lib')
    tags = htmlParser.select('.click-to-next')
    for tag in tags:
      tag['data-next-page'] = pages[index + 1]
  with open(str(projectPath / '{}.html'.format(page)), 'w') as outputF:
    outputF.write(htmlParser.prettify(formatter='html'))
    outputF.close()
    logger.info('Updated Glidefile')


# 
# 
# 

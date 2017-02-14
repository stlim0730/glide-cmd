from os import listdir, mkdir
from os.path import isfile, join, exists
import simplejson as json
import sys


class ProjectManager():


  CONFIG_FILE = 'config/config.json'
  PROJECT_FILE = 'config/project.json'


  # def __init__(self):
  # # Don't need to instantiate for now: static access only.
  #   return


  @staticmethod
  def _exists(path, name):
    return exists(join(path, name))


  @staticmethod
  def _mkdir(path, name):
    mkdir(join(path, name))


  @staticmethod
  def getConfFile(path):
    try:
      with open(path, 'r') as f:
        return json.load(f)
    except FileNotFoundError:
      print('Cannot find the file: %s.' % path)
      sys.exit(1)


  @staticmethod
  def setConfFile(path, key, val):
    confFile = ProjectManager.getConfFile(path)
    confFile[key] = val
    with open(path, 'w') as f:
      return json.dump(confFile, f, indent='  ')


  @staticmethod
  def getCurrentProject():
    projectSettings = ProjectManager.getConfFile(ProjectManager.PROJECT_FILE)
    return projectSettings['current']


  @staticmethod
  def setCurrentProject(projectName):
    ProjectManager.setConfFile(ProjectManager.PROJECT_FILE, 'current', projectName)
    return ProjectManager.getCurrentProject()


  @staticmethod
  def showProjects(projectRoot):
    currentProject = ProjectManager.getCurrentProject()
    pRootDir = str(projectRoot)
    dirs = [d for d in listdir(pRootDir) if not isfile(join(pRootDir, d))]
    for d in dirs:
      if d == currentProject:
        print('* %s' % d)
      else:
        print('  %s' % d)
    print()
    if len(dirs) == 0:
      print('No project exists.')
      print('Use create-project command to create a new project.')
    elif len(dirs) == 1:
      print('%d project exists.' % len(dirs))
      print('Use select-project command to select a project to work on.')
    else:
      print('%d projects exist.' % len(dirs))
      print('Use select-project command to select a project to work on.')


  @staticmethod
  def createProject(dataRoot, outputRoot, projectName):
    dRootDir = str(dataRoot)
    oRootDir = str(outputRoot)
    dExists = ProjectManager._exists(dRootDir, projectName)
    if dExists:
      # The project path exists. Failed to create a project.
      print('Couldn\'t create a new project as a project with the same name exists.')
      print('Use show-projects command to see existing projects.')
    else:
      # They don't exist. Safely create a new project.
      ProjectManager._mkdir(dRootDir, projectName)
      # TODO: clear the output path?
      oExists = ProjectManager._exists(oRootDir, projectName)
      if not oExists:
        ProjectManager._mkdir(oRootDir, projectName)
      print('Your project \'%s\' has been created.' % projectName)
      ProjectManager.selectProject(dataRoot, outputRoot, projectName)


  @staticmethod
  def selectProject(dataRoot, outputRoot, projectName):
    # Make sure the required paths exist
    dRootDir = str(dataRoot)
    oRootDir = str(outputRoot)
    dExists = ProjectManager._exists(dRootDir, projectName)
    oExists = ProjectManager._exists(oRootDir, projectName)
    if dExists:# and oExists:
      # Safely select the project.
      currentProject = ProjectManager.setCurrentProject(projectName)
      print('Now you\'re working on project \'%s\'.' % currentProject)
    else:
      # Something's wrong.
      print('Couldn\'t select the project you specified.')
      print('Use show-projects command to see existing projects.')


  @staticmethod
  def showPages(dataRoot):
    # Make sure the required paths exists
    dRootDir = str(dataRoot)
    currentProject = ProjectManager.getCurrentProject()
    dExists = ProjectManager._exists(dRootDir, currentProject)
    if dExists:
      # Show existing data files
      files = [f for f in listdir(join(dRootDir, currentProject)) if f.endswith('.glide')]
      for f in files:
        print('  %s' % f)
      print()
      if len(files) == 0:
        print('Project \'%s\' doens\'t have a page.' % currentProject)
      elif len(files) == 1:
        print('Project \'%s\' has %d page.' % (currentProject, len(files)))
      else:
        print('Project \'%s\' has %d pages.' % (currentProject, len(files)))
      print('Use create-page command to create a new page.')
    else:
      print('Couldn\'t find pages in the current project.')
      print('Use show-projects command to see existing projects.')
      print('Use select-project command to select a project to work on.')


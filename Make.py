import subprocess
import sys
import os

PROJECT_FILE = 'project.yml'
MIN_XCODE_GEN_VERSION = '2.10.1'

class ProjectGenerator:
	def __init__(self, projectName):
		self.projectName = projectName
		self.resultStr = ''

	def configure_name(self):
		self.resultStr += f'name: {self.projectName}\n'
		return self

	def configure_options(self):
		self.resultStr += 'options:\n'
		self.resultStr += f'  minimumXcodeGenVersion: {MIN_XCODE_GEN_VERSION}\n'
		return self

	def configure_packages(self):
		self.resultStr += 'packages:\n'
		self.resultStr += '  SnapKit:\n'
		self.resultStr += '    url: https://github.com/SnapKit/SnapKit.git\n'
		self.resultStr += '    branch: 5.0.1\n'
		return self

	def configure_targets(self):
		self.resultStr += 'targets:\n'
		self.resultStr += f'  {self.projectName}:\n'
		self.resultStr += '    platform: iOS\n'
		self.resultStr += '    type: application\n'
		self.resultStr += '    sources:\n'
		self.resultStr += f'      - {self.projectName}\n'
		self.resultStr += '    dependencies:\n'
		self.resultStr += '      - package: SnapKit\n'
		return self

	def run(self):
		with open(PROJECT_FILE, 'w') as f:
			f.write(self.resultStr)
		os.rename('DefaultProjectName', self.projectName)
		subprocess.run(["xcodegen"])

if __name__ == "__main__":

	if os.path.exists('{}'.format(PROJECT_FILE)):
		os.remove('{}'.format(PROJECT_FILE))

	args = sys.argv
	if len(args) > 0 and args[0].lower() == 'make.py':
		args = args[1:]

	project_name = 'DefaultProjectName'
	for arg in args:
		arg_name, arg_val = arg.split('=')
		if arg_name == 'name':
			project_name = arg_val

	generator = ProjectGenerator(project_name)
	generator.configure_name()
	generator.configure_options()
	generator.configure_packages()
	generator.configure_targets()
	generator.run()



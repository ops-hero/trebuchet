import os
from fabric.api import local

from .utils import local_template, prepare_folder

def get_custom_file(type_, name, template, target_path=None, target_extension=None,
                target_is_executable=None, target_filename=None, options=None):
    """ factory for CustomFiles """
    if type_ == 'nginx':
        return NGINXCustomFile(name, template, options=options)
    elif type_ == "binary":
        return BinaryCustomFile(name, template, options=options)
    elif type_ == "debian":
        return DEBIANCustomFile(name, template, options=options)
    elif type_ == "product":
        return ProductCustomFile(name, template, options=options)
    elif type_ == "upstart":
        return UpstartCustomFile(name, template, options=options)
    elif type_ == "newrelic_config":
        return NewrelicConfigCustomFile(name, template, options=options)
    elif type_ == "custom":
        return CustomFile(name, template, target_path, target_extension, target_is_executable, target_filename, options)
    else:
        raise NotImplementedError


class CustomFile(object):
    is_executable = False
    relative_path = ""
    extension = ""

    def __init__(self, name, template=None, target_path=None, target_extension=None,
                target_is_executable=None, target_filename=None, options=None):
        self.name = name
        self.template = template

        if target_is_executable:
            self.is_executable = target_is_executable

        if target_path:
            self.relative_path = target_path

        if target_extension:
            self.extension = target_extension

        if target_filename:
            self.filename = target_filename

        self.options = options if options else {}

    def build(self, base_path, options=None, extra_template_dir=None):
        print "{%s}: building file %s" % (self.__class__.__name__, self.name)

        # fuse the path, even if relative_filepath starts with "/"
        full_path = os.path.join(base_path, *self.relative_filepath.split("/"))
        print full_path
        prepare_folder(os.path.dirname(full_path))

        params = {'full_name': self.name}
        if self.options:
            params.update(self.options)
        if options:
            params.update(options)

        my_cwd = os.path.abspath(os.path.dirname(__file__))
        template_dir = [os.path.join(my_cwd, "..", "templates")]
        if extra_template_dir:
            template_dir.append(extra_template_dir)

        local_template(self.template,
            full_path,
            context=params,
            use_jinja=True,
            backup=False,
            template_dir=template_dir)

        if self.is_executable:
            local("chmod +x %s" % full_path)

        self.post_build(full_path)

    def post_build(self, full_path):
        pass

    @property
    def relative_filepath(self):
        if hasattr(self, "filename"):
            return os.path.join(self.relative_path, self.filename)
        return os.path.join(self.relative_path,
                            "%s%s" % (self.name, self.extension))


class NGINXCustomFile(CustomFile):
    relative_path = os.path.join("etc", "nginx", "sites-available")
    extension = ".conf"


class BinaryCustomFile(CustomFile):
    relative_path = os.path.join("opt", "trebuchet", "bin")
    is_executable = True


class DEBIANCustomFile(CustomFile):
    relative_path = os.path.join("DEBIAN")

    def post_build(self, full_path):
        local('echo "" >> %s' % full_path)
        local('chmod 0775 %s' % full_path)


class ProductCustomFile(CustomFile):
    relative_path = os.path.join("etc", "trebuchet")
    extension = ".conf"

class UpstartCustomFile(CustomFile):
    relative_path = os.path.join("etc", "init")
    extension = ".conf"

# class HelicomServerConfigCustomFile(CustomFile):
#     relative_path = os.path.join("etc", "trebuchet", "helicom_server")
#     extension = ".cfg"

# class HelicomBrokerConfigCustomFile(CustomFile):
#     relative_path = os.path.join("etc", "trebuchet", "helicom_broker")
#     extension = ".cfg"

class NewrelicConfigCustomFile(CustomFile):
    relative_path = os.path.join("etc", "trebuchet", "newrelic")
    extension = ".ini"

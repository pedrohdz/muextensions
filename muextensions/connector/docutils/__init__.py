class Connector():
    @property
    def target_dir(self):
        # pylint: disable=no-member
        return self._target_dir

    @property
    def base_uri(self):
        # pylint: disable=no-member
        return self._base_uri

    @property
    def default_image_format(self):
        # pylint: disable=no-member
        return self._default_image_format

    @property
    def create_dirs(self):
        # pylint: disable=no-member
        return self._create_dirs

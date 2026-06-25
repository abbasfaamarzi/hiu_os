import logging
from hiu_os.__operations__.__file__.__base__.__keywords__ import OsKeywords
from hiu_os.__operations__.__file__.__base__.__serializers__ import Vars

logger = logging.getLogger(__name__)


class Formats:
    """
    Utility class for handling file names, formats, and naming conventions.
    """

    @staticmethod
    def has_os_generator_request(file_name: str):
        """
        Extract the OS generator request suffix from a file name if present.

        Args:
            file_name (str): The file name to inspect.

        Returns:
            str or None: The request type ('create', 'update', 'delete', 'read')
                         if found, otherwise None.
        """
        logger.debug(f"Checking for OS generator request in: {file_name}")
        os_generator_request = None
        if "_" in file_name:
            file_name_split = file_name.split("_")
            os_generator_request = file_name_split[-1]
            if os_generator_request in OsKeywords.OSGeneratorRequests:
                logger.info(f"Found OS generator request: {os_generator_request}")
                return os_generator_request
        logger.debug("No OS generator request found.")
        return None

    @staticmethod
    def get_format(name):
        """
        Validate if the given name is a known format.

        Args:
            name (str): The format name to check.

        Returns:
            str or None: The format name if it is in the known list, else None.
        """
        logger.debug(f"Checking format: {name}")
        if name in OsKeywords.FORMATS:
            logger.info(f"Format recognized: {name}")
            return name
        logger.warning(f"Unknown format: {name}")
        return None

    @staticmethod
    def get_format_name(name):
        """
        Split a file name into base name and extension.

        For names with a dot, the last part is treated as extension.
        For names with an underscore but no dot, splits on the first underscore.
        If neither, returns (name, "dir").

        Args:
            name (str): The file or directory name.

        Returns:
            tuple: (base_name, extension_or_dir)
        """
        logger.debug(f"Splitting format name: {name}")
        if '.' in name:
            parts = name.split(".")
            if len(parts) == 2:
                result = parts[0], parts[1]
            else:
                result = ".".join(parts[:-1]), parts[-1]
            logger.debug(f"Dot split result: {result}")
            return result
        if "_" in name:
            parts = name.split("_", 1)
            result = parts[0], parts[1]
            logger.debug(f"Underscore split result: {result}")
            return result
        logger.debug("No separator found, defaulting to directory.")
        return name, "dir"

    @staticmethod
    def format_cuter(file_name: str):
        """
        Remove the extension from a file name (strip everything after the first dot).

        Args:
            file_name (str): The file name.

        Returns:
            str: The file name without extension.
        """
        if '.' in file_name:
            result = file_name.split(".")[0]
            logger.debug(f"format_cuter: {file_name} -> {result}")
            return result
        return file_name

    @staticmethod
    def is_hard_file(file_name: str):
        """
        Check if a file name ends with the literal "file".

        Args:
            file_name (str): The file name.

        Returns:
            bool: True if it ends with "file", else False.
        """
        result = file_name.endswith("file")
        logger.debug(f"is_hard_file({file_name}) -> {result}")
        return result

    @staticmethod
    def to_snake_case(original_name) -> str:
        """
        Convert a CamelCase or PascalCase name to snake_case.

        Args:
            original_name (str): The input string.

        Returns:
            str: The snake_case version.
        """
        import re
        snake = re.sub(r'(?<!^)(?=[A-Z])', '_', original_name).lower()
        logger.debug(f"to_snake_case: {original_name} -> {snake}")
        return snake

    @staticmethod
    def column_name_field_name(name):
        """
        Split a name on the first underscore into two parts.

        If no underscore, returns (name, name).

        Args:
            name (str): The input string.

        Returns:
            tuple: (first_part, second_part)
        """
        if "_" in name:
            parts = name.split("_", 1)
            result = parts[0], parts[1]
        else:
            result = name, name
        logger.debug(f"column_name_field_name({name}) -> {result}")
        return result

    @staticmethod
    def column_syntax(name):
        """
        Extract column and field names assuming the last two characters are separators.

        e.g., 'id_' -> column_name='id', field_name='_'.
        WARNING: This implementation seems buggy; it simply takes name[:-2] and name[-1].

        Args:
            name (str): The input string.

        Returns:
            tuple: (column_name, field_name)
        """
        column_name = name[:-2]
        field_name = name[-1]
        logger.debug(f"column_syntax({name}) -> ({column_name}, {field_name})")
        return column_name, field_name


class DictAttr(dict):
    """
    A dictionary that allows attribute-style access for its keys.
    Also prevents overriding existing built-in attributes.
    """

    def __setattr__(self, field, value):
        if field not in dir(self):
            self[field] = value
        else:
            super().__setattr__(field, value)

    def __getattr__(self, field):
        if field in self:
            return self[field]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute '{field}'")


class VarsApi(Vars):
    """
    API-specific variable handler, extending Vars to provide filtered API attributes.
    """

    @property
    def path_api(self):
        """Return the API variables (alias for api_vars)."""
        return self.api_vars

    @property
    def ledgers(self):
        """Return the API variables (alias for api_vars)."""
        return self.api_vars

    @property
    def ledgers_name(self):
        """Return a set of API variable names."""
        return set(self.api_vars_name)

    @property
    def call_api(self):
        """
        Return a DictAttr of callable API methods, excluding properties and internal names.
        """
        filtered = {
            k: v for k, v in self.api_all_dict
            if not isinstance(getattr(self.api, k, None), property)
            and k not in self.inheritance_names
            and not k.startswith("__")
            and not k.startswith("_")
        }
        logger.debug(f"call_api: built DictAttr with {len(filtered)} items")
        return DictAttr(filtered)
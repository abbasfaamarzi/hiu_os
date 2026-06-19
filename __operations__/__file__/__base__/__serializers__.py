import logging
from hiu_os.__operations__.__file__.__base__.__keywords__ import OsKeywords

logger = logging.getLogger(__name__)


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


class SerializersClear:
    """
    Helper methods for cleaning or transforming serialized data.
    """

    @staticmethod
    def pop_path(data: dict) -> dict:
        """
        Remove the 'path' key from the input dictionary if present.

        Args:
            data (dict): The dictionary to process.

        Returns:
            dict: The dictionary with 'path' removed (if it existed).
        """
        try:
            data.pop('path')
            logger.debug("pop_path: removed 'path' key")
        except (KeyError, TypeError) as e:
            logger.debug(f"pop_path: no 'path' key or invalid input: {e}")
        return data


class Vars:
    """
    Base class for extracting and filtering class attributes,
    particularly for API-related variable handling.
    """
    inheritance_names = []
    inheritance_names.extend(OsKeywords.INHERTAINCENAMES)

    @property
    def api(self):
        """Return the class itself (used to inspect class attributes)."""
        return self.__class__

    @property
    def api_name(self):
        """Return the name of the class."""
        return self.api.__name__

    @property
    def api_all_dict(self):
        """Return all class attributes as items."""
        return self.api.__dict__.items()

    @property
    def api_vars(self):
        """
        Return a DictAttr containing class variables (non-callable, non-property,
        not in inheritance_names, and not private/dunder).
        """
        filtered = {
            k: v for k, v in self.api_all_dict
            if not callable(v)
            and not isinstance(getattr(self.api, k, None), property)
            and k not in self.inheritance_names
            and not k.startswith("__")
            and not k.startswith("_")
        }
        logger.debug(f"api_vars: built DictAttr with {len(filtered)} items")
        return DictAttr(filtered)

    @property
    def api_vars_name(self):
        """Return a list of variable names from api_vars."""
        return list(self.api_vars.keys())

    @property
    def api_vars_value(self):
        """Return a list of variable values from api_vars."""
        return list(self.api_vars.values())

    @property
    def api_type(self):
        """Return the class name of the current instance."""
        return type(self).__name__
import logging

logger = logging.getLogger(__name__)


class OsKeywords:
    """
    Central repository of OS-related constants and keyword lists.
    """
    # Bytes representations for path separators
    sep_b = b'\\'
    seps_b = b'\\/'
    colon_b = b':'

    # String representations
    sep = '\\'
    seps = '\\/'
    colon = ':'

    # Known file extensions (used for validation)
    KNOWN_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "pdf", "docx", "xlsx", "txt", "json"]

    # Static directories or files that are part of the OS structure
    STATICS_OS_DIR_OR_FILE_LIST = {
        'main_dir',
        'assets',
        'default',
        'fonts',
        'none_profile',
        'gallery'
    }

    # Allowed generator request types
    OSGeneratorRequests = ["create", "update", "delete", "read"]

    # Supported file formats for the system
    FORMATS = ["file", "json", "pkl"]

    # Reserved keywords used in cursor/path operations
    CURSERKEYWORDS = [
        "_path",
        "path_builder",
        "parent",
        "child_name",
        "path_split",
        "head_name",
        "file_name",
        "format_name",
        "tree",
        "resource",
        "save_log",
        "files",
        "set_curser",
        "request",
        "do_request"
    ]

    # Names that are inherited and should be skipped in some contexts
    INHERTAINCENAMES = ["on_genesis", "tree", "save_tree", "on_genesis"]  # duplicate 'on_genesis'


class AppKeywords:
    """
    Application-level configuration constants.
    """
    version_name = "hiu_os"
    name = "TimiOs"
    main_calender_country = "United States"
    domin = "http://127.0.0.1:8000/"
    theme_data_config = {
        "style": "Light",
        "color": "Yellowgreen",
        "language": "Arabic",
    }


class FallbackChoices:
    """
    Fallback constants, primarily for acronym lists.
    """
    FORMATS = ['API', 'XML', 'JSON', 'HTTP', 'HTTPS', 'URL', 'URI', 'SQL', 'CSS', 'HTML']


class SnakePascalName:
    """
    Utility class for converting between naming conventions (snake, Pascal, camel, kebab).
    """
    COMMON_ACRONYMS = FallbackChoices.FORMATS

    @classmethod
    def to_snake_case(cls, original_name: str) -> str:
        """
        Convert any input string to snake_case.

        Args:
            original_name (str): Input string.

        Returns:
            str: snake_case version.
        """
        if not original_name:
            return ""
        if original_name.isupper():
            return original_name.lower()
        result = []
        prev_char = ''
        for i, char in enumerate(original_name):
            current_char_upper = char.isupper()
            prev_char_lower = prev_char.islower() if prev_char else False
            if current_char_upper and prev_char_lower:
                result.append('_')
                result.append(char.lower())
            elif (current_char_upper and prev_char and prev_char.isupper() and i < len(original_name) - 1 and
                  original_name[i + 1].islower()):
                result.append('_')
                result.append(char.lower())
            else:
                result.append(char.lower())
            prev_char = char
        snake = ''.join(result)
        logger.debug(f"to_snake_case({original_name}) -> {snake}")
        return snake

    @classmethod
    def to_pascal_case(cls, original_name: str, preserve_acronyms: bool = True) -> str:
        """
        Convert snake_case to PascalCase (CapitalizedWords).

        Args:
            original_name (str): Input string (typically snake_case).
            preserve_acronyms (bool): If True, keep known acronyms uppercase.

        Returns:
            str: PascalCase version.
        """
        if not original_name:
            return ""
        parts = original_name.split('_')
        capitalized_parts = []
        for part in parts:
            if preserve_acronyms and part in cls.COMMON_ACRONYMS:
                capitalized_parts.append(part.upper())
            else:
                capitalized_parts.append(part.capitalize())
        result = ''.join(capitalized_parts)
        logger.debug(f"to_pascal_case({original_name}, preserve={preserve_acronyms}) -> {result}")
        return result

    @classmethod
    def to_camel_case(cls, original_name: str, preserve_acronyms: bool = True) -> str:
        """
        Convert snake_case to camelCase (first word lowercased).

        Args:
            original_name (str): Input string.
            preserve_acronyms (bool): If True, keep known acronyms uppercase.

        Returns:
            str: camelCase version.
        """
        if not original_name:
            return ""
        parts = original_name.split('_')
        camel_parts = [parts[0]]
        for part in parts[1:]:
            if preserve_acronyms and part in cls.COMMON_ACRONYMS:
                camel_parts.append(part.upper())
            else:
                camel_parts.append(part.capitalize())
        result = ''.join(camel_parts)
        logger.debug(f"to_camel_case({original_name}, preserve={preserve_acronyms}) -> {result}")
        return result

    @classmethod
    def to_kebab_case(cls, original_name: str) -> str:
        """
        Convert any input string to kebab-case.

        Args:
            original_name (str): Input string.

        Returns:
            str: kebab-case version.
        """
        snake = cls.to_snake_case(original_name)
        kebab = snake.replace('_', '-')
        logger.debug(f"to_kebab_case({original_name}) -> {kebab}")
        return kebab

    @classmethod
    def detect_case(cls, text: str) -> str:
        """
        Detect the naming convention of the given text.

        Args:
            text (str): Input string.

        Returns:
            str: One of 'snake_case', 'kebab-case', 'PascalCase', 'camelCase', or 'unknown'.
        """
        if '_' in text:
            return 'snake_case'
        elif '-' in text:
            return 'kebab-case'
        elif text and text[0].isupper():
            return 'PascalCase'
        elif text and text[0].islower() and any(c.isupper() for c in text[1:]):
            return 'camelCase'
        else:
            return 'unknown'
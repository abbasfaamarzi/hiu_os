<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HiuOs</title>
</head>
<body>
    <div style="text-align: center; padding: 2rem;">
        <img src="hiu_logo.png" alt="لوگوی HiuOs" style="max-width: 100%; height: auto;">
        <h1 style="margin-top: 20px;">Welcome to HiuOs</h1>
    </div>
</body>
</html>

# Comprehensive Guide to the `__operations__` Package

This package forms the core file and directory management layer for the **TimiOs** (or `hiu_os`) application. It provides a **fluent, cursor‑based interface** that lets you navigate the filesystem, perform CRUD operations on text, JSON, and Pickle files, and manage directories – all with integrated logging.

---

## Installation & Setup

The package is part of the project and requires no separate installation. To use it, import the main classes from `_system_.py`:

```python
from _system_ import OperationsSystem, Curser
```

Alternatively, you can use the minimal entry point `hiu.py`:

```python
from hiu import HiuOs

os = HiuOs()
desktop = os.desktop
```

---

## Architecture Overview

The package is structured into several submodules:

- **`__base__`** – Core utilities:
  - `Formats`: file name parsing, extension extraction, naming conversions.
  - `DictAttr`: dictionary with attribute‑style access (e.g., `obj.key`).
  - `OsKeywords` & `AppKeywords`: system constants and application settings.
  - `SnakePascalName`: conversion between naming conventions (snake_case, PascalCase, etc.).
  - `LifeCycleLog`: lifecycle logging (start, working, stop).

- **`__structure__`** – Abstract base class `HttpOperatorRequest` defining the standard CRUD methods (`create`, `read`, `update`, `clear`, `delete`).

- **Concrete implementations**:
  - `File`: operations on plain text files (`.txt`, `.csv`, etc.).
  - `JsonFile`: operations on JSON files.
  - `PickleFile`: operations on Python Pickle (binary serialization) files.
  - `Dir`: operations on directories.

- **`__path__`** – Path utilities (`Path` for splitting/joining, finding main directory, etc.) and the `AppCurser` for chained navigation.

- **`_system_.py`** – Main classes:
  - `Curser`: the fluent filesystem navigator.
  - `ShortCuts`: predefined paths (e.g., `assets`, `settings.json`).
  - `OperationsSystem`: high‑level accessor for application resources.

---

## Core Classes and Usage

### 1. `OperationsSystem` – Entry Point

Create an instance to access all major paths:

```python
system = OperationsSystem()
```

Key properties:

- `system.desktop` – cursor for the application root.
- `system.assets`, `system.default`, `system.fonts`, `system.ledgers`, `system.settings`, `system.configs`, `system.logs`, `system.paths` – shortcuts to commonly used locations.
- `system.tree` – a `DictAttr` containing the full tree of available cursors.
- `system.save_tree()` – saves the current tree to `paths.json`.

### 2. `Curser` – The Fluent Navigator

The `Curser` class is the heart of the package. It allows you to traverse the filesystem using attribute chaining and perform operations directly.

#### Creating a Cursor

```python
cursor = Curser()                  # starts at the application's main directory
cursor = Curser("/custom/path")    # starts at a given absolute path
```

#### Navigation

Use attribute access (or `__call__`) to move into sub‑paths:

```python
cursor.assets.default.settings_json   # navigates to assets/default/settings.json
cursor("assets")("default")("settings_json")   # equivalent
```

If the attribute name matches a known extension (e.g., `json`, `txt`, `pkl`), the cursor treats it as a file and automatically appends the extension. Otherwise, it is considered a directory.

#### CRUD Operations

Every cursor exposes the following methods (all accept optional `data` and return the result of the operation):

- `create(data)` – creates the file/directory (overwrites if exists).
- `read` (property) – returns the content (for JSON/Pickle: dict/list; for text: string; for directories: dict mapping names to full paths).
- `update(data)` – updates content (for files, same as `create`; for directories, renames – requires `new_name`).
- `clear()` – empties file content or removes all contents of a directory (the directory itself remains).
- `delete()` – permanently removes the file or entire directory tree.

**Examples:**

```python
# Read a JSON settings file
settings = system.settings.read
print(settings.theme)   # because read returns a DictAttr

# Update settings
system.settings.update({"theme": "dark", "language": "English"})

# Create a new text file under assets
system.assets.new_file_txt.create("Hello, world!")

# List contents of the default directory
items = system.default.read   # returns a dict

# Delete the file
system.assets.new_file_txt.delete()

# Clear a directory (remove all contents)
system.assets.temp_dir.clear()
```

#### The `tree` Property

Each cursor provides a `tree` property returning a `DictAttr` with metadata:

```python
info = system.default.tree
print(info.path)             # relative path from the application root
print(info.file_name)        # base name without extension
print(info.format_name)      # extension or 'dir'
print(info.tree)             # dictionary of parent paths
if info.format_name == "dir":
    print(info.every_things) # directory contents (excluding hidden items)
```

#### Operation Aliases

For convenience, several attribute names are mapped to the underlying CRUD methods (see `http_map_pattern` in `Curser`). For example, `rename` maps to `update`, `list` maps to `read`. So you can write `cursor.folder.rename("new_name")` (though the `update` method expects a `new_name` parameter for directories).

#### Automatic Creation

The class variable `AUTO_CREATE = True` (default) causes any missing directory/file to be automatically created (with `create({})`) when you navigate to it. Set it to `False` to disable this behavior.

---

### 3. Direct Use of File/Directory Handlers

Although you normally work through `Curser`, you can also call the static methods of `File`, `JsonFile`, `PickleFile`, or `Dir` directly:

```python
from __operations__.__file__.__json__ import JsonFile
data = JsonFile.read("path/to/file.json")
```

---

### 4. Path Utilities (`Path`)

The `Path` class provides helpful static methods:

- `Path.split(path)` – splits a path into components using the OS separator.
- `Path.join(*parts)` – intelligently joins path parts (handles Windows drive letters).
- `Path.main_dir()` – locates the application root by searching for `AppKeywords.version_name` in the current file's path.
- `Path.path_builder(*args)` – builds an absolute path under the main directory.

---

### 5. `DictAttr` and `Formats`

- `DictAttr` – a dictionary that also allows attribute access (e.g., `obj.key`). The result of `read` for JSON and directories is of this type.
- `Formats` – provides utilities like:
  - `get_format_name(name)`: splits a name into base and extension.
  - `to_snake_case(name)`: converts to snake_case.
  - `has_os_generator_request(file_name)`: checks for `create`, `update`, `delete`, or `read` at the end of a file name.

---

### 6. Lifecycle Logging (`LifeCycleLog`)

This class maintains global state for logging start/working/stop events. When a `Curser` is created with `save_log=True`, every operation logs details to `log.json` via the cursor’s `_log_cursor`. Example:

```python
cursor = Curser(save_log=True)
cursor.settings_json.update({"new": "value"})   # logs the update
```

---

## Complete Example

```python
from _system_ import OperationsSystem

os = OperationsSystem()

# 1. Read settings
settings = os.settings.read
print(f"Theme: {settings.get('style')}")

# 2. Change and save settings
os.settings.update({"style": "Dark", "color": "Blue"})

# 3. Create a new JSON file in ledgers
os.ledgers.my_data_json.create({"users": ["Alice", "Bob"]})

# 4. Read it back
data = os.ledgers.my_data_json.read
print(data.users)   # ['Alice', 'Bob']

# 5. Delete it
os.ledgers.my_data_json.delete()

# 6. Print the entire tree and save it
tree = os.tree
os.save_tree()
```

---

## Customization and Advanced Topics

### Adding New File Formats

To support a new format (e.g., YAML), create a class that implements the `HttpOperatorRequest` interface (with `create`, `read`, `update`, `clear`, `delete`). Then register it in the `Curser.files` dictionary with the appropriate extension key.

### Modifying Constants

- Extensions recognised by the system are in `OsKeywords.KNOWN_EXTENSIONS`.
- The list of format names used for operation dispatching is in `OsKeywords.FORMATS`.
- Application‑wide settings (name, version, theme defaults) are in `AppKeywords`.
- Naming conversion acronyms can be extended in `SnakePascalName.COMMON_ACRONYMS`.

### Logging Configuration

Each module uses Python’s standard `logging` with a module‑level logger. You can configure log levels and handlers as usual.

### Platform Compatibility

The package uses `os.path.join` and `os.sep` internally, but be aware that `AppCurser.getattrs` currently uses a hardcoded backslash – consider replacing it with `os.path.join` for cross‑platform safety.

---

## Known Limitations and Caveats

- **Duplicate `DictAttr` definitions** – the class appears in both `__formats__.py` and `__serializers__.py`; centralising it would avoid confusion.
- **`Formats.column_syntax`** – the implementation (`name[:-2]` and `name[-1]`) is likely buggy; it seems intended to split on the last underscore.
- **Hardcoded backslash** in `AppCurser.getattrs` – use `os.path.join` for portability.
- **`Curser.__getattr__`** – when an attribute matches an operation alias (e.g., `list` → `read`), it may conflict with reserved names. This is intentional but could be surprising.
- **`AUTO_CREATE`** is global – you might want per‑cursor control.
- **Lifecycle logging** – expects the cursor to provide an `update(path, data)` method; this couples logging to the cursor’s storage mechanism.

---

## Summary

The `__operations__` package provides a robust, intuitive, and extensible filesystem management layer for your Python applications. Its fluent cursor interface drastically reduces boilerplate code, while the built‑in logging and automatic path resolution make it ideal for projects that rely heavily on configuration files, data storage, and asset management.

With the knowledge from this guide, you can now confidently navigate, read, write, and organise your files using a clean, Pythonic API. Happy coding!
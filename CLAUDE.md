# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**GeoIP2-python** is MaxMind's official Python client library for:
- **GeoIP2/GeoLite2 Web Services**: Country, City, and Insights endpoints
- **GeoIP2/GeoLite2 Databases**: Local MMDB file reading for various database types (City, Country, ASN, Anonymous IP, Anonymous Plus, ISP, etc.)

The library provides both web service clients (sync and async) and database readers that return strongly-typed model objects containing geographic, ISP, anonymizer, and other IP-related data.

**Key Technologies:**
- Python 3.10+ (type hints throughout, uses modern Python features)
- MaxMind DB Reader for binary database files
- Requests library for sync web service client
- aiohttp for async web service client
- pytest for testing
- ruff for linting and formatting
- mypy for static type checking
- uv for dependency management and building

## Code Architecture

### Package Structure

```
src/geoip2/
├── models.py           # Response models (City, Insights, AnonymousIP, etc.)
├── records.py          # Data records (City, Location, Traits, etc.)
├── errors.py           # Custom exceptions for error handling
├── database.py         # Local MMDB file reader
├── webservice.py       # HTTP clients (sync Client and async AsyncClient)
├── _internal.py        # Internal base classes and utilities
└── types.py            # Type definitions
```

### Key Design Patterns

#### 1. **Model Classes vs Record Classes**

**Models** (in `models.py`) are top-level responses returned by database lookups or web service calls:
- `Country` - base model with country/continent data
- `City` extends `Country` - adds city, location, postal, subdivisions
- `Insights` extends `City` - adds additional web service fields (web service only)
- `Enterprise` extends `City` - adds enterprise-specific fields
- `AnonymousIP` - anonymous IP lookup results
- `AnonymousPlus` extends `AnonymousIP` - adds additional anonymizer fields
- `ASN`, `ConnectionType`, `Domain`, `ISP` - specialized lookup models

**Records** (in `records.py`) are contained within models and represent specific data components:
- `PlaceRecord` - abstract base with `names` dict and locale handling
- `City`, `Continent`, `Country`, `RepresentedCountry`, `Subdivision` - geographic records
- `Location`, `Postal`, `Traits`, `MaxMind` - additional data records

#### 2. **Constructor Pattern**

Models and records use keyword-only arguments (except for required positional parameters):

```python
def __init__(
    self,
    locales: Sequence[str] | None,  # positional for records
    *,
    continent: dict[str, Any] | None = None,
    country: dict[str, Any] | None = None,
    # ... other keyword-only parameters
    **_: Any,  # ignore unknown keys
) -> None:
```

Key points:
- Use `*` to enforce keyword-only arguments
- Accept `**_: Any` to ignore unknown keys from the API
- Use `| None = None` for optional parameters
- Boolean fields default to `False` if not present

#### 3. **Serialization with to_dict()**

All model and record classes inherit from `Model` (in `_internal.py`) which provides `to_dict()`:

```python
def to_dict(self) -> dict[str, Any]:
    # Returns a dict suitable for JSON serialization
    # - Skips None values and False booleans
    # - Recursively calls to_dict() on nested objects
    # - Handles lists/tuples of objects
    # - Converts network and ip_address to strings
```

The `to_dict()` method replaced the old `raw` attribute in version 5.0.0.

#### 4. **Locale Handling**

Records with names use `PlaceRecord` base class:
- `names` dict contains locale code → name mappings
- `name` property returns the first available name based on locale preference
- Default locale is `["en"]` if not specified
- Locales are passed down from models to records

#### 5. **Property-based Network Calculation**

For performance reasons, `network` and `ip_address` are properties rather than attributes:

```python
@property
def network(self) -> ipaddress.IPv4Network | ipaddress.IPv6Network | None:
    # Lazy calculation and caching of network from ip_address and prefix_len
```

#### 6. **Web Service Only vs Database Models**

Some models are only used by web services and do **not** need MaxMind DB support:

**Web Service Only Models**:
- `Insights` - extends City but used only for web service
- Simpler implementation without database parsing logic

**Database-Supported Models**:
- Models used by both web services and database files
- Must handle MaxMind DB format data structures
- Examples: `City`, `Country`, `AnonymousIP`, `AnonymousPlus`, `ASN`, `ISP`

## Testing Conventions

### Running Tests

```bash
# Install dependencies using uv
uv sync --all-groups

# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/models_test.py

# Run specific test class or method
uv run pytest tests/models_test.py::TestModels::test_insights_full

# Run tests with coverage
uv run pytest --cov=geoip2 --cov-report=html
```

### Linting and Type Checking

```bash
# Run all linting checks (mypy, ruff check, ruff format check)
uv run tox -e lint

# Run mypy type checking
uv run mypy src tests

# Run ruff linting
uv run ruff check

# Auto-fix ruff issues
uv run ruff check --fix

# Check formatting
uv run ruff format --check --diff .

# Apply formatting
uv run ruff format .
```

### Running Tests Across Python Versions

```bash
# Run tests on all supported Python versions
uv run tox

# Run on specific Python version
uv run tox -e 3.11

# Run lint environment
uv run tox -e lint
```

### Test Structure

Tests are organized by component:
- `tests/database_test.py` - Database reader tests
- `tests/models_test.py` - Response model tests
- `tests/webservice_test.py` - Web service client tests

### Test Patterns

When adding new fields to models:
1. Update the test method to include the new field in the `raw` dict
2. Add assertions to verify the field is properly populated
3. Test both presence and absence of the field (null handling)
4. Verify `to_dict()` serialization includes the field correctly

Example:
```python
def test_anonymous_plus_full(self) -> None:
    model = geoip2.models.AnonymousPlus(
        "1.2.3.4",
        anonymizer_confidence=99,
        network_last_seen=datetime.date(2025, 4, 14),
        provider_name="FooBar VPN",
        is_anonymous=True,
        is_anonymous_vpn=True,
        # ... other fields
    )

    assert model.anonymizer_confidence == 99
    assert model.network_last_seen == datetime.date(2025, 4, 14)
    assert model.provider_name == "FooBar VPN"
```

## Working with This Codebase

### Adding New Fields to Existing Models

1. **Add the parameter to `__init__`** with proper type hints:
   ```python
   def __init__(
       self,
       # ... existing params
       *,
       field_name: int | None = None,  # new field
       # ... other params
   ) -> None:
   ```

2. **Assign the field in the constructor**:
   ```python
   self.field_name = field_name
   ```

3. **Add class-level type annotation** with docstring:
   ```python
   field_name: int | None
   """Description of the field, its source, and availability."""
   ```

4. **Update `to_dict()` if special handling needed** (usually automatic via `_internal.Model`)

5. **Update tests** to include the new field in test data and assertions

6. **Update HISTORY.rst** with the change (see CHANGELOG Format below)

### Adding New Models

When creating a new model class:

1. **Determine if web service only or database-supported**
2. **Follow the pattern** from existing similar models
3. **Extend the appropriate base class** (e.g., `Country`, `City`, `SimpleModel`)
4. **Use type hints** for all attributes
5. **Use keyword-only arguments** with `*` separator
6. **Accept `**_: Any`** to ignore unknown API keys
7. **Provide comprehensive docstrings** for all attributes
8. **Add corresponding tests** with full coverage

### Date Handling

When a field returns a date string from the API (e.g., "2025-04-14"):

1. **Parse it to `datetime.date`** in the constructor:
   ```python
   import datetime

   self.network_last_seen = (
       datetime.date.fromisoformat(network_last_seen)
       if network_last_seen
       else None
   )
   ```

2. **Annotate as `datetime.date | None`**:
   ```python
   network_last_seen: datetime.date | None
   ```

3. **In `to_dict()`**, dates are automatically converted to ISO format strings by the base class

### Deprecation Guidelines

When deprecating fields:

1. **Add deprecation to docstring** with version and alternative:
   ```python
   metro_code: int | None
   """The metro code of the location.

   .. deprecated:: 5.0.0
      The code values are no longer being maintained.
   """
   ```

2. **Keep deprecated fields functional** - don't break existing code

3. **Update HISTORY.rst** with deprecation notices

4. **Document alternatives** in the deprecation message

### HISTORY.rst Format

Always update `HISTORY.rst` for user-facing changes.

**Important**: Do not add a date to changelog entries until release time. Version numbers are added but without dates.

Format:
```rst
5.2.0
++++++++++++++++++

* IMPORTANT: Python 3.10 or greater is required. If you are using an older
  version, please use an earlier release.
* A new ``field_name`` property has been added to ``geoip2.models.ModelName``.
  This field provides information about...
* The ``old_field`` property in ``geoip2.models.ModelName`` has been deprecated.
  Please use ``new_field`` instead.
```

## Common Pitfalls and Solutions

### Problem: Incorrect Type Hints
Using wrong type hints can cause mypy errors or allow invalid data.

**Solution**: Follow these patterns:
- Optional values: `Type | None` (e.g., `int | None`, `str | None`)
- Non-null booleans: `bool` (default to `False` in constructor if not present)
- Sequences: `Sequence[str]` for parameters, `list[T]` for internal lists
- IP addresses: `IPAddress` type alias (from `geoip2.types`)
- IP objects: `IPv4Address | IPv6Address` from `ipaddress` module

### Problem: Missing to_dict() Serialization
New fields not appearing in serialized output.

**Solution**: The `to_dict()` method in `_internal.Model` automatically handles most cases:
- Non-None values are included
- False booleans are excluded
- Empty dicts/lists are excluded
- Nested objects with `to_dict()` are recursively serialized

If you need custom serialization, override `to_dict()` carefully.

### Problem: Test Failures After Adding Fields
Tests fail because fixtures don't include new fields.

**Solution**: Update all related tests:
1. Add field to constructor calls in tests
2. Add assertions for the new field
3. Test null case if field is optional
4. Verify `to_dict()` serialization

### Problem: Constructor Argument Order
Breaking changes when adding required parameters.

**Solution**:
- Use keyword-only arguments (after `*`) for all optional parameters
- Only add new parameters as optional with defaults
- Never add required positional parameters to existing constructors

## Code Style Requirements

- **ruff** enforces all style rules (configured in `pyproject.toml`)
- **Type hints required** for all functions and class attributes
- **Docstrings required** for all public classes, methods, and attributes (Google style)
- **Line length**: 88 characters (Black-compatible)
- No unused imports or variables
- Use modern Python features (3.10+ type union syntax: `X | Y` instead of `Union[X, Y]`)

## Development Workflow

### Setup

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependencies including dev and lint groups
uv sync --all-groups
```

### Before Committing

```bash
# Format code
uv run ruff format .

# Check linting
uv run ruff check --fix

# Type check
uv run mypy src tests

# Run tests
uv run pytest

# Or run everything via tox
uv run tox
```

### Version Requirements

- **Python 3.10+** required (as of version 5.2.0)
- Uses modern Python features (match statements, structural pattern matching, `X | Y` union syntax)
- Target compatibility: Python 3.10-3.14

## Additional Resources

- [API Documentation](https://geoip2.readthedocs.org/)
- [GeoIP2 Web Services Docs](https://dev.maxmind.com/geoip/docs/web-services)
- [MaxMind DB Format](https://maxmind.github.io/MaxMind-DB/)
- GitHub Issues: https://github.com/maxmind/GeoIP2-python/issues

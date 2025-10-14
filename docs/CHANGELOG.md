# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- GitHub Actions CI/CD pipeline
- PyPI packaging configuration
- Community files (LICENSE, CONTRIBUTING.md)

### Changed
- Centralized all configuration in pyproject.toml
- Removed pytest.ini (migrated to pyproject.toml)

## [1.1.0] - 2025-10-12

### Fixed
- **CRITICAL**: Fixed template processing system that was generating non-functional projects
- **CRITICAL**: Fixed placeholder processing for both `$VARIABLE` and `{{VARIABLE}}` formats
- **CRITICAL**: Fixed requirements.txt generation with real dependencies instead of placeholders
- **CRITICAL**: Fixed Python code generation to be fully functional without placeholders
- **CRITICAL**: Fixed infinite loop issue in non-interactive testing mode
- Fixed missing `EJEMPLO_USO_MAIN` placeholder causing warnings
- Fixed Python syntax errors in generated code (true → True)
- Fixed duplicate code lines in generated templates

### Added
- Hybrid template processing system supporting both placeholder formats
- Comprehensive default values for 50+ placeholders
- Enhanced placeholder detection and replacement system
- Detailed logging for template processing
- Non-interactive testing support via configuration files
- Automatic cleanup of unprocessed placeholders

### Changed
- Improved template processing performance
- Enhanced error handling and logging
- Better default value management
- Optimized disk space usage (freed ~3GB)
- Streamlined project generation workflow

### Technical Details
- Implemented `_process_template` method with dual format support
- Added `_replace_with_defaults` method with comprehensive fallback values
- Enhanced `collect_project_info` with 50+ additional variables
- Improved `_find_unprocessed_placeholders` detection system
- Fixed all template processing warnings and errors

## [1.0.0] - 2024-12-19

### Added
- Initial release of Pre-Cursor
- Project generator optimized for AI agents
- Support for multiple project types:
  - Python Library
  - Python CLI Tool
  - Python Web App (Flask/Django/FastAPI)
  - Python Data Science
  - Python ML/AI
  - C++ Project
  - Node.js Project
  - TD_MCP Project
  - Custom projects
- Template system with placeholder substitution
- Configuration file support (JSON/YAML)
- Interactive and non-interactive modes
- Git repository initialization
- Comprehensive documentation
- Test suite with 80%+ coverage
- Examples and quickstart guide

### Features
- **Template Processing**: Uses Python's string.Template for placeholder replacement
- **Project Validation**: Robust validation of project parameters
- **Configuration Loading**: Support for JSON and YAML configuration files
- **Git Integration**: Automatic Git repository initialization
- **Documentation Generation**: Automatic README, CONTEXT, and tutorial generation
- **TD_MCP Integration**: Specialized support for TouchDesigner MCP projects
- **Error Handling**: Comprehensive error handling and user feedback

### Technical Details
- Python 3.8+ compatibility
- Modular architecture with separate validation and configuration modules
- Comprehensive test coverage
- Clean, maintainable codebase following established methodology
- Professional project structure ready for distribution

## [0.1.0] - 2024-12-19

### Added
- Initial development version
- Basic project generation functionality
- Core template system
- Basic validation framework

---

## Version History

- **1.0.0**: First stable release with full feature set
- **0.1.0**: Initial development version

## Release Notes

### v1.0.0 Release Notes
This is the first stable release of Pre-Cursor, a project generator optimized for AI agents. The tool provides a comprehensive solution for creating new projects with established methodologies and best practices.

**Key Highlights:**
- 🚀 **One Command, Complete Project**: Generate full project structures with a single command
- 🤖 **AI Agent Optimized**: Designed specifically for use with AI coding assistants
- 📚 **Comprehensive Documentation**: Every generated project includes complete documentation
- 🔧 **Multiple Project Types**: Support for Python, C++, Node.js, and specialized projects
- ⚡ **Fast and Reliable**: Robust validation and error handling ensure consistent results

**Breaking Changes:**
- None (first stable release)

**Migration Guide:**
- No migration needed (first stable release)

**Known Issues:**
- None reported

**Future Roadmap:**
- Additional project types
- Enhanced template customization
- Plugin system for extensibility
- Web interface for project generation

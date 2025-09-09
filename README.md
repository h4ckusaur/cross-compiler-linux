# 🐧 Cross-Compile Linux

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://www.docker.com/)

A powerful Python tool for cross-compiling C programs across different Linux distributions using Docker containers. Perfect for ensuring your C code works consistently across various Linux environments without needing multiple physical machines.

## ✨ Features

- 🐳 **Docker-based compilation** - Isolated, reproducible builds
- 🎯 **Multi-distro support** - Ubuntu, Debian, CentOS, and more
- 🔍 **Smart image detection** - Automatically finds compatible Docker images
- 📁 **Makefile support** - Detects and builds from existing Makefiles
- 🧹 **Auto-cleanup** - Removes Docker images after compilation to save space
- ⚡ **Simple CLI** - Easy-to-use command-line interface

## 🚀 Quick Start

### Prerequisites

- Python 3.6+
- Docker installed and running
- Internet connection (for pulling Docker images)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/h4ckusaur/cross-compile-linux.git
cd cross-compile-linux
```

2. Install dependencies:
```bash
pip install requests
```

### Basic Usage

```bash
python cross-compile.py <directory> <distro> <version>
```

**Example:**
```bash
python cross-compile.py . ubuntu 22.04
```

## 📖 Detailed Usage

### Command Syntax

```bash
python cross-compile.py [OPTIONS] <directory> <distro> <version>
```

**Parameters:**
- `<directory>` - Path to your C source code directory
- `<distro>` - Target Linux distribution (e.g., ubuntu, debian, centos)
- `<version>` - Distribution version (e.g., 20.04, 11, 8)

### Examples

#### Compile a simple C program for Ubuntu 22.04
```bash
python cross-compile.py . ubuntu 22.04
```

#### Compile for Debian 11
```bash
python cross-compile.py /path/to/project debian 11
```

#### Compile for CentOS 8
```bash
python cross-compile.py . centos 8
```

## 🏗️ How It Works

1. **Image Discovery**: Searches Docker Hub for available images matching your specified distribution and version
2. **Interactive Selection**: If multiple images are found, presents an interactive menu for selection
3. **Dockerfile Generation**: Creates a temporary Dockerfile with build tools and your source code
4. **Container Build**: Builds a Docker image with the necessary compilation environment
5. **Compilation**: Runs the compilation inside the container with your source code mounted
6. **Cleanup**: Automatically removes the temporary Docker image to save disk space

## 📁 Project Structure

```
cross-compile-linux/
├── cross-compile.py      # Main Python script
├── Dockerfile           # Example Dockerfile
├── Docker.template      # Dockerfile template
├── sample.c            # Example C program
├── output/             # Compiled binaries (created during compilation)
└── README.md           # This file
```

## 🛠️ Supported Distributions

The tool supports any Linux distribution available on Docker Hub. Popular options include:

- **Ubuntu**: 18.04, 20.04, 22.04, 24.04
- **Debian**: 9, 10, 11, 12
- **CentOS**: 7, 8
- **Alpine**: 3.15, 3.16, 3.17, 3.18
- **Fedora**: 35, 36, 37, 38

## 🔧 Advanced Features

### Makefile Support

If your project contains a `Makefile`, the tool will:
- Parse available targets
- Present an interactive menu to choose the target
- Use `make` instead of direct `gcc` compilation

### Automatic C File Detection

For projects without a Makefile:
- Automatically detects `.c` files in the directory
- Compiles the first found C file
- Outputs to `output` binary

### Build Tools Installation

The tool automatically installs necessary build tools:
- `build-essential` (GCC, make, etc.)
- `musl-tools` (for static linking)
- `libmnl-dev` and `libnftnl-dev` (for networking libraries)

## 🐛 Troubleshooting

### Common Issues

**Docker not running:**
```bash
sudo systemctl start docker
```

**Permission denied:**
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

**No matching images found:**
- Check if the distribution and version combination exists on Docker Hub
- Try a different version number
- Use more specific version tags

### Debug Mode

For verbose output, you can modify the script to add debug prints or use Docker's verbose mode.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Docker team for the amazing containerization platform
- Python community for excellent libraries
- Linux distributions maintainers for providing base images

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/h4ckusaur/cross-compile-linux/issues) page
2. Create a new issue with detailed information
3. Join our discussions for community support

---

**Made with ❤️ by [h4ckusaur](https://github.com/h4ckusaur)**

*Happy cross-compiling! 🐧✨*

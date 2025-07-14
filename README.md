# IEEE Paper Template

## Overview
This repository provides a LaTeX template for writing papers for IEEE.

## Features
- Output files are generated in the `out` directory.
- Uses the IEEE standard style (IEEEtran class and bst).
- Uses `pdflatex` for building.

## Environment Setup
### 1. Install TeX Live
If you do not have a LaTeX environment, it is recommended to install TeX Live.
- On macOS:
  ```sh
  brew install --cask mactex
  # Add TeX Live to PATH if necessary
  sudo tlmgr path add
  ```
- On Windows:
  Download the installer from the official TeX Live website (https://tug.org/texlive/) and follow the instructions.
- On Linux:
  ```sh
  sudo apt-get install texlive-full
  ```

### 2. Install latexmk
In most cases, latexmk is included with TeX Live. If you need to install it separately:
- On macOS/Linux:
  ```sh
  sudo tlmgr install latexmk
  ```
- On Windows:
  Use the TeX Live package manager (tlmgr) to add `latexmk`.

## Linting and Formatting LaTeX Files Locally
You can check and format your LaTeX files locally using the following commands:

### 1. Lint (lacheck)
```sh
lacheck paper.tex
```
- Checks the syntax of your LaTeX source and reports any errors or warnings.

### 2. Format (latexindent)
```sh
latexindent -w paper.tex
```
- Automatically formats your LaTeX source file.
- The `-w` option overwrites `paper.tex` (a backup is saved as `paper.tex.bak`).

#### If you need to install these tools:
```sh
sudo tlmgr install lacheck latexindent
```

## How to Build
1. Install the required LaTeX environment (such as TeX Live).
2. Run the following command to generate the PDF:

```sh
latexmk -C
latexmk -pdf paper.tex
```

## File Structure
- `paper.tex` : Main TeX file
- `IEEEtran.cls` : IEEE paper class file
- `IEEEtran.bst` : IEEE bibliography style
- `out/` : Output directory (auto-generated)
- `.latexmkrc` : Configuration file for latexmk

## Notes
- The IEEEtran class and style files are specified in `paper.tex`.
- Please use `.bib` files for references.

## GitHub Actions
This repository can be configured to use GitHub Actions for continuous integration (CI) and automated PDF builds. By setting up a workflow (e.g., `.github/workflows/latex.yml`), you can automatically compile your LaTeX documents on every push or pull request. The generated PDF can be uploaded as an artifact or deployed to GitHub Pages for easy sharing and review.

Typical workflow steps include:
- Setting up the TeX Live environment
- Installing required LaTeX packages
- Compiling the `.tex` file using `latexmk` or `pdflatex`
- Uploading the resulting PDF as a build artifact

For more details, refer to the [GitHub Actions documentation](https://docs.github.com/en/actions) or add a sample workflow file to your repository.

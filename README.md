# Docthub-Enterprise

## Overview

This repository contains two main areas:

- `Docthub Enterprise/` — Python automation and utility scripts for Docthub Enterprise workflows.
- `monkey-testing/` — Node.js-based link and page testing suite for Docthub sites.

## Project Setup

### 1. Python environment for `Docthub Enterprise`

1. Open a terminal in `c:\Users\DELL9\vscode\Docthub-Enterprise`
2. Activate the existing virtual environment:

```powershell
& .venv\Scripts\Activate.ps1
```

3. Install Python dependencies if needed (check each script folder for requirements files):

```powershell
pip install -r "Docthub Enterprise\Userapp_script\requirements.txt"
```

> Note: Some scripts may not have a requirements file. Inspect the individual Python script to determine the required packages.

### 2. Node.js setup for `monkey-testing`

1. Open a terminal in `c:\Users\DELL9\vscode\monkey-testing`
2. Install dependencies:

```powershell
npm install
```

3. Install Playwright browsers if needed:

```powershell
npm run install:browser
```

## How to Run

### Python scripts

Run any Python script from the root or from the script folder directly. Example:

```powershell
python "Docthub Enterprise\Membership\manage membership 2.py"
```

### Monkey-testing suite

From the `monkey-testing` folder, run a test command:

```powershell
npm run test:home
```

## Folder Layout

- `Docthub Enterprise/`
  - `Candidate Search/`
  - `docthub_script/`
  - `E Certificate/`
  - `Institute_Script/`
  - `Membership/`
  - `Recruiter_scripts/`
  - `test_example/`
  - `Userapp_script/`
  - `X Path/`
  - `Xpath/`

- `monkey-testing/`
  - `config/`
  - `reports/`
  - `scripts/`

## Notes

- Python scripts are organized by feature area and may require local data files.
- `monkey-testing` uses Node.js and Playwright for automated link checks and report generation.
- Keep the virtual environment activated when running Python scripts from `Docthub Enterprise`.


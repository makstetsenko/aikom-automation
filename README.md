# aikom-automation
Automated actions for AIKOM

## Data directories

You can use `./data` and `./output` directories for storing your data files, auth keys, downloaded reports etc. 

These directories are in `.gitignore` files.

## Auth 

For authorization you need auth key for your organization (like `Key-6.pfx` or `Key-6.dat`). Place it in `./data` directory.

## Code generation to help setup actions

```bash
playwright codegen --user-data-dir=./browser-profile https://cabinet.aikom.gov.ua
```
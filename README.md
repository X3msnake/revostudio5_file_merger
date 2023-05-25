# RevoStudio5 file merger app

![revostudio_file_merger](https://github.com/X3msnake/revostudio5_file_merger/assets/11083514/7e404238-fe90-48e2-b5aa-e7534f908670)

## Installation

- Download and install Python3 (check the boax add to path when prompted)
- Downlaod the project
- On windows run RS5pmerge.bat

## Why

This basic project merger app to allows me to merge multiple RevoStudio5 projects into a single project with multiple scans.
I found i have this need specially when using mobile captures since at the moment of writing this code the android app always creates a new project instead of a new scan inside a project like in the desktop app.

This would ideally be done natively inside the software but for now it solves this issue.

Also one can merge the project files manually by copying the data folder into the merge project and editing the .revo file with notepad++ copying the blocks for the childs that give the program the reference of the files to load in the scan timeline

Should work on all platforms, requiring only python3+ to be installed with no other dependencies.

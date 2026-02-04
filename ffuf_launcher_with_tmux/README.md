# ffuf - Launche with tmux
The scripts available launches several sessions of tmux and then for each URL specified creates a different output file of the `ffuf` discovery task.

## Requirements
You need the following programs installed on a linux terminal:
- ffuf
- tmux

## Configuration
- Move to the folder `<folder_name>` you want to use
- clone the repository
- Create a folder `targets` with all the TXT files with the URLs to be discovered. For example:

```bash
├── targets
│   ├── target1.txt
│   ├── target2.txt
│   ├── target3.txt
│   │       ...
│   └── target4.txt
│
├── ffuf_content_discovery.sh
└── parallel_tmux.sh
```

**target<N>.txt:**
```bash
https://example1.com:8080/
http://example1.com:80/
https://example2.com:8443/
...
https://exampleN.com/
```


## Run
### Launch the TMUX sessions
```bash
./parallel_tmux.sh start
```

For each file in the `targets` folder, a new TMUX session will be created.

For each URL, the script will create a different result file in a `results` sub-folder of the current working directory.

If you want to use a different folder as input:
```bash
./parallel_tmux.sh start <folder_name>
```

**Example of final folder content:**
```bash
├── targets
│   ├── target1.txt
│   ├── target2.txt
│   ├── target3.txt
│   │       ...
│   └── target4.txt
│
├── results
│   ├── https___example1_com_8080_directories.csv
│   ├── https___example1_com_8080_files.csv
│   ├── http___example1_com_80_directories.csv
│   ├── http___example1_com_80_files.csv
│   ├── https___example2_com_8443_directories.csv
│   ├── https___example2_com_8443_files.csv
│   │       ...
│   ├── https___exampleN_com_directories.csv
│   └── https___exampleN_com_files.csv
│
├── ffuf_content_discovery.sh
└── parallel_tmux.sh
```

### Pause/restart the TMUX sessions
```bash
./parallel_tmux.sh pause
```

or:

```bash
./parallel_tmux.sh start
```

In both cases, the script sends carriage return as input of the TMUX sessions (with session name `files_*` or `dir_*`), pausing the current `ffuf` scan or restarting the paused `ffuf` scan.

### Kill the TMUX sessions
```bash
./parallel_tmux.sh kill
```

The script kills all the TMUX sessions (with session name `files_*` or `dir_*`).

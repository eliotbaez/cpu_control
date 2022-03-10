# cpu\_control

cpu\_control is a Python script to dynamically enable or disable CPU cores on 
Linux based systems.

## Installation

cpu\_control employs a little bit of `argv[0]` magic on the command line. The
recommended method of installation is to make symbolic links to the same script
in /usr/local/bin:

```sh
ln -s /usr/local/bin/cpu_enable $(pwd)/cpu_control.sh
ln -s /usr/local/bin/cpu_disable $(pwd)/cpu_control.sh
```

The links **must** be called `cpu_enable` and `cpu_disable` to take advantage of
the magic. If `argv[0]` is neither of these names, the script will fall back to
the default behavior of requiring an argument to specify whether you want to
enable or disable the specified CPUs.

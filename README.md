# zenbuilder

JavaScript concatenation tool

### What it does

zenbuilder starts in a specified source directory and recursively finds all JavaScript (.js) files under the directory. It concatenates them in the order they're found and writes the result to the specified output file. If the minify flag is passed, a minified version of the concatenated file will also be generated, at the same location as the main output file but with a `.min.*` extension.

### How to use

zenbuilder is a single Python script, so it's fairly simple to use. If you create a Batch/shell script (called `zen` for example) to run the Python file then you can use it as follows:

```
$ zen -i src -o build/lib.js
```

### Examples

Concatenate all .js files in the folder `src` and its subdirectories to an output file `build/lib.js`:

```
$ zen -i src -o build/lib.js
```

Concatenate all .js files in the folder `myproject/js` and its subdirectories to an output file `main.js` and also generate a minified version at `main.min.js`:

```
$ zen -i myproject/js -o main.js -m
```

### Arguments and .zenconfig

zenbuilder accepts the following command-line arguments:

* `-i, --in  <root_dir>`  
  Specify the root directory for JavaScript source


* `-o, --out <output_file>`  
  Specify the name of the concatenated output file
  
  
* `-m, --minify`  
  Also generate a minified JS file in the same location as the output file


* `-v, --verbose`  
  Enable verbose mode to print extra information about build progress


* `-h, --help`  
  Show help

When zenbuilder is run, it first looks for a `.zenconfig` file in the working directory and attempts to load arguments from there. It then overwrites any loaded arguments with any passed command-line arguments. The format of the `.zenconfig` file is as follows:

```
@root_dir src
@output_file build/zen.js
@minify
@verbose
@ignore -test.js lib.js
```

The only notable difference from the command-line arguments is the presence of the `@ignore` flag, which allows you to specify a list of file endings to ignore (i.e. filenames that end with anything in the list are not included in the concatenated output).

----
Eric Schmidt 2016  
www.eschmidt.co

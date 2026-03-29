### CONFIG FILE

```
WIDTH=15                // Integer [11~100]
HEIGHT=15               // Integer [9~100]
ENTRY=0,0               // Integers
EXIT=9,8                // Integers
OUTPUT_FILE=maze.txt    // valid .txt, .maze or .mf file
PERFECT=True            // Boolean: One valid path or more
SEED=7852486468         // Integer: Seed used for the maze generation (can be negative)
```

### INSTRUCTIONS

To use the package as a library within another project, you can run
`pip install mazegen-x.x.x-py3-none-any.whl` or
`pip install mazegen-x.x.x.tar.gz`

The library contains all the core logic related to maze generation and path
generation.

Once installed, you can import it with `import mazegen`.

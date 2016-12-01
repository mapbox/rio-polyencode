# rio-polyencode
Encode time-series data into a single polynomial raster


## encoding
```
Usage: rio polyencode [OPTIONS] INPUTS OUTPUT

  Encode n-inputs into one polynomial raster. Each successive input is
  interpreted as a step of 1.

Options:
  -d, --poly-order INTEGER
  -r, --reflect INTEGER
  --version                 Show the version and exit.
  --help                    Show this message and exit.
```

## decoding
```
Usage: rio polydecode [OPTIONS] INPUT OUTPUT X

  Decode a polynomial raster for a given X value

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.
```



import sys

import click
import rasterio as rio

import numpy as np

from rio_polyencode import __version__ as polyencode_version

def read_all(inputs, reflect):
    with rio.open(inputs[0]) as src:
        out = np.zeros((len(inputs) + reflect, src.height, src.width), dtype=src.meta['dtype'])

    for i, p in enumerate(inputs):
        with rio.open(p) as src:
            src.read(1, out=out[i])

    for r in range(reflect):
        out[r + len(inputs)] = out[r]

    return out

def poly_multid(data, pdegree=2):
    depth, rows, cols = data.shape
    X = np.arange(depth)

    polyvals = np.dstack(
        np.polyfit(
            X,
            data.reshape(depth, rows * cols),
            pdegree
        )
    )[0].reshape(rows, cols, pdegree + 1)
        
    return polyvals


@click.command(short_help="")
@click.argument(
    'inputfiles',
    type=click.Path(resolve_path=True),
    required=True,
    nargs=-1,
    metavar="INPUTS")
@click.argument(
    'output',
    type=click.Path(resolve_path=True))
@click.option('--poly-order', '-d', type=int, default=2)
@click.option('--reflect', '-r', type=int, default=0)
@click.version_option(version=polyencode_version, message='%(version)s')
@click.pass_context
def polyencode(ctx, inputfiles, output, poly_order, reflect):
    """
    Encode n-inputs into one polynomial raster. Each successive input is interpreted as a step of 1.
    """
    with rio.open(inputfiles[0]) as src:
        metaprof = src.profile.copy()

    metaprof.update(dtype=np.float32, count=(poly_order + 1))

    verbosity = (ctx.obj and ctx.obj.get('verbosity')) or 1

    data = read_all(inputfiles, reflect)
    
    out = poly_multid(data, poly_order).astype(np.float32)

    with rio.open(output, 'w', **metaprof) as dst:
        for i in range(poly_order + 1):
            dst.write(out[:, :, i], i + 1)

@click.command(short_help="")
@click.argument(
    'inputfile',
    type=click.Path(resolve_path=True),
    required=True,
    metavar="INPUT")
@click.argument(
    'output',
    type=click.Path(resolve_path=True))
@click.argument('x', type=float)
@click.version_option(version=polyencode_version, message='%(version)s')
@click.pass_context
def polydecode(ctx, inputfile, output, x):
    """
    Decode a polynomial raster for a given X value
    """
    with rio.open(inputfile) as src:
        metaprof = src.profile.copy()
        data = src.read()

    depth, rows, cols = data.shape

    depth -= 1

    out = (
        np.sum(np.dstack(
            [p * x ** abs(depth - d) for p, d in zip(data, range(depth))]
            ), axis=2) + data[-1]
        ).astype(np.float32)

    metaprof.update(dtype=np.float32, count=1)

    verbosity = (ctx.obj and ctx.obj.get('verbosity')) or 1


    with rio.open(output, 'w', **metaprof) as dst:
        dst.write(out, 1)

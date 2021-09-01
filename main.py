from app.openapi_bundler import process

import click


@click.command(no_args_is_help=True)
@click.option(
    "--in", "-i", "in_file", required=True, help="Path to main API spec file",
)
@click.option(
    "--out-file", "-o", "out_file", default="./OpenAPI.yaml", help="Path to output file"
)
def main(in_file, out_file):
    """
    This tool combines multi file API specification into a single file
    """
    process(in_file, out_file)


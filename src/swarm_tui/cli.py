import click

from swarm_tui.backends.docker import AioDockerBackend
from swarm_tui.backends.fake import FakeBackend
from swarm_tui.tui import SwarmTui


@click.group(invoke_without_command=True)
@click.option("--fake", is_flag=True, help="Use fake backends")
@click.pass_context
def cli(ctx, fake) -> None:
    """Run the tui"""
    backend = FakeBackend() if fake else AioDockerBackend()
    tui = SwarmTui(backend)
    tui.run()


if __name__ == "__main__":
    cli()

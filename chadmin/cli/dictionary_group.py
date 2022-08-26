from click import group, option, pass_context
from cloud.mdb.cli.common.formatting import print_response
from cloud.mdb.clickhouse.tools.chadmin.internal.dictionary import get_dictionaries, reload_dictionary


@group('dictionary')
def dictionary_group():
    """Dictionary management commands."""
    pass


@dictionary_group.command('list')
@option('--name')
@option('--status')
@pass_context
def list_command(ctx, name, status):
    """
    List dictionaries.
    """
    dictionaries = get_dictionaries(ctx, name=name, status=status)
    print_response(
        ctx,
        dictionaries,
        default_format='table',
    )


@dictionary_group.command('reload')
@option('--name')
@option('--status')
@pass_context
def reload_command(ctx, name, status):
    """
    Reload one or several dictionaries.
    """
    dictionaries = get_dictionaries(ctx, name=name, status=status)
    for dictionary in dictionaries:
        print(f'Reloading dictionary {_full_name(dictionary)}')
        reload_dictionary(ctx, database=dictionary['database'], name=dictionary['name'])


def _full_name(dictionary):
    database = dictionary['database']
    name = dictionary['name']
    if database:
        return f'`{database}`.`{name}`'
    else:
        return f'`{name}`'
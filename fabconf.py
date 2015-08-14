app_name = 'example.com'
app_remote_dir = '/usr/local/apps/' + app_name


def apply(env):
    env.user = 'YOUR-USER'
    env.port = 22
    env.roledefs = {
        'app': {
            'hosts': ['IP-PUBLIC-1', 'IP-PUBLIC-2'],
            'hosts_private': ['IP-PRIVATE-1', 'IP-PRIVATE-2']
        },
        'sql': {
            'hosts': ['IP-PUBLIC-SQL-1', 'IP-PUBLIC-SQL-2'],
            'hosts_private': ['IP-PRIVATE-SQL-1', 'IP-PRIVATE-SQL-2']
        },
        'prx': {
            'hosts': ['IP-PUBLIC-1'],
            'hosts_private': ['IP-PRIVATE-1'],
        },
    }

    all_hosts = []
    for data in env.roledefs.values():
        hosts = data['hosts']
        all_hosts.extend(hosts)
    env.roledefs['all'] = all_hosts

    env.passwords = {
        # apps
        'davinci@IP-PUBLIC-APP-1:SSH-PORT': 'USER-PASSWD-APP',
        'davinci@IP-PUBLIC-APP-2:SSH-PORT': 'USER-PASSWD-APP',

        # sql
        'davinci@IP-PUBLIC-SQL-1:SSH-PORT': 'USER-PASSWD-SQL',
        'davinci@IP-PUBLIC-SQL-2:SSH-PORT': 'USER-PASSWD-SQL',

        # prx
        'davinci@IP-PUBLIC-1:SSH-PORT': 'USER-PASSWD-PRX',
    }

    env.key_filename = [
        './keys/app.key',
        './keys/sql.key',
        './keys/prx.key',
    ]

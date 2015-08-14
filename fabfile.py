import os
import time

from fabric.api import *
from fabric.operations import put
from fabric.contrib import files

# Apply credentials
import fabconf
fabconf.apply(env)


# =============================================================================
# Machine operations
# =============================================================================

def remote_machine_do(command):
    """ Execute `command` on remote machines """
    run(command.strip().strip())


def remote_machine_sudo_do(command):
    """ Execute `command` with sudo privileges """
    sudo(command.strip().strip())


def remote_machine_upgrade():
    """ Run apt-get update & upgrade """
    sudo('apt-get update')
    sudo('apt-get upgrade -y')


def uptime():
    run('uptime')


def ufw():
    sudo('ufw status')


# =============================================================================
# App related operations (app servers)
# =============================================================================

def remote_app_start():
    """ Start app """

    sudo('service {}.app start'.format(fabconf.app_name))
    # sudo('service {}.worker start'.format(fabconf.app_name))


def remote_app_stop():
    """ stop app """
    sudo('service {}.app stop'.format(fabconf.app_name))
    # sudo('service {}.worker stop'.format(fabconf.app_name))


def remote_app_restart():
    """ restart app """
    sudo('service {}.app restart'.format(fabconf.app_name))
    # sudo('service {}.worker restart'.format(fabconf.app_name))


def remote_app_test():
    """ Test app """
    with cd(fabconf.app_remote_dir):
        run('make local.app.test')


def remote_app_upstart():
    """ Push upstart config. > fab -P --roles prx remote_app_upstart """

    # Web
    put('conf/app.upstart.conf', '/tmp/{}.app.conf'.format(fabconf.app_name))
    sudo('cp /tmp/{}.app.conf /etc/init/{}.app.conf'.format(
        fabconf.app_name, fabconf.app_name)
    )
    sudo('rm /tmp/{}.app.conf'.format(fabconf.app_name))

    # Worker
    # Install worker upstart conf


def remote_app_install():
    """ Install app on remote machines """

    # Make sure app dir exists
    if not files.exists(fabconf.app_remote_dir):
        run('mkdir -p {}'.format(fabconf.app_remote_dir))

    # Make sure var/log directory exists
    with cd(fabconf.app_remote_dir):
        if not files.exists('var/log'):
            run('mkdir -p var/log')

    # Copy upstart script
    remote_app_upstart()

    # Install python and co.

    sudo('apt-get -y install build-essential')
    sudo('apt-get -y install python3-dev')
    sudo('apt-get -y install python-dev')

    # Run local install script
    with cd(fabconf.app_remote_dir):
        run('make local.app.install')


def remote_app_push():
    """ Upload app src to remote machines, and retart """

    now = time.strftime('%c')
    now = now.replace(' ', '-').replace('/', '-').replace(':', '-')
    files_to_tar = 'app script Makefile'
    tarfile = '{}-{}.tar.gz'.format(fabconf.app_name, now)

    # Create app parent directory
    parent_dir = os.path.dirname(fabconf.app_remote_dir)
    if not files.exists(parent_dir):
        print('* Creating remote app parent dir')
        sudo('mkdir -p {}'.format(parent_dir))
        sudo('chown {user} {parent_dir}'.format(
            user=env.user, parent_dir=parent_dir))

    # Create app directory
    if not files.exists(fabconf.app_remote_dir):
        print('* Creating app dir')
        run('mkdir -p {}'.format(fabconf.app_remote_dir))

    # Tar project and ship it to remote machines
    local('tar -czf {tarfile} {files_to_tar}'.format(
        tarfile=tarfile,
        files_to_tar=files_to_tar)
    )
    put(tarfile, parent_dir)

    # Untar
    with cd(parent_dir):
        # Extract tar archive to directory
        run("tar -xvf ./{} -C {}".format(tarfile, fabconf.app_remote_dir))
        run('rm ./{}'.format(tarfile))
        run('echo "release on {}" > {}.release.txt'.format(
            now, fabconf.app_name))

    with quiet():
            local('rm ./{}'.format(tarfile))


# =============================================================================
# DATABASE
# =============================================================================
def remote_sql_config():
    """ Configure database """
    sudo('cp /etc/rethinkdb/default.conf.sample /etc/rethinkdb/instances.d/instance1.conf')
    sudo('service rethinkdb start')


def remote_sql_init():
    """ Init database (tables, etc) """
    with cd(fabconf.app_remote_dir):
        run('make local.sql.init')


def remote_sql_backup():
    """ Backup DB """
    with cd(fabconf.app_remote_dir):
        run('make local.sql.backup')


def remote_sql_restore():
    """ Restore DB """
    with cd(fabconf.app_remote_dir):
        run('make local.sql.restore')


# =============================================================================
# FIREWALLS
# =============================================================================
def _allow_ufw_rule_for_ips(interface, private_ips, port, proto):
    """ Create ufw rule """
    for ip in private_ips:
        cmd = 'ufw allow in on {} from {} to any port {} proto {}'.format(
            interface, ip, port, proto
        )
        sudo(cmd)


@roles('sql')
def remote_ufw_sql():
    """ Allow sql access to app private ips """
    ips = env.roledefs['app']['hosts_private']
    _allow_ufw_rule_for_ips('eth1', ips, 28015, 'tcp')


@roles('app')
def remote_ufw_app():
    """ Allow app access from prx servers on private interface"""
    ips = env.roledefs['prx']['hosts_private']
    _allow_ufw_rule_for_ips('eth1', ips, '8001:8004', 'tcp')


@roles('prx')
def remote_ufw_prx():
    """ Allow regular http(s) ports """
    sudo('ufw allow http')
    sudo('ufw allow https')


# =============================================================================
# Nginx configuration for different roles
# =============================================================================

def _remote_nginx_config(role):
    sudo('cp /etc/nginx/nginx.conf{,.backup}')
    put('./conf/{}.nginx.conf'.format(role), '/tmp/nginx.conf')
    sudo('cp /tmp/nginx.conf /etc/nginx/nginx.conf')
    run('rm /tmp/nginx.conf')
    sudo('service nginx reload')


@roles('prx')
def remote_prx_nginx_config():
    _remote_nginx_config('prx')


@roles('sto')
def remote_sto_nginx_config():
    _remote_nginx_config('sto')


# =============================================================================
# OTHER
# =============================================================================

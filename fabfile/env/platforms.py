from fabric.api import env
from fabric.decorators import task
from fabric.colors import yellow
import re
import os
from importlib import import_module

env.distrib = 'ubuntu14.04'
env.KRAKEN_USER = 'www-data'
env.TYR_USER = env.KRAKEN_USER

#setup
env.packages_url = 'https://ci.navitia.io/job/navitia_release/lastSuccessfulBuild/artifact/*zip*/archive.zip'
env.packages_destination = '/tmp'

env.KRAKEN_RABBITMQ_OK_PORT = 5672
env.KRAKEN_RABBITMQ_WRONG_PORT = 56722
env.PUPPET_RESTART_DELAY = 30
# max time (in s) that a kraken can take to restart
env.KRAKEN_RESTART_DELAY = 90
env.TYR_WORKER_START_DELAY = 10
env.APACHE_START_DELAY = 8
env.KRAKEN_START_ONLY_ONCE = True
env.TYR_START_ONLY_ONCE = True
env.APACHE_START_ONLY_ONCE = True

# get the port in kraken.ini zmq_socket directive
# ex.: "zmq_socket = tcp://*:1234"
env.KRAKEN_RE_PORT = re.compile('^tcp://.*\:(?P<port>[0-9]*)')
env.zmq_server = 'localhost'

# kraken.ini defaults number of thread for an instance
env.KRAKEN_NB_THREADS = 4
env.KRAKEN_START_PORT = 30000

# use ZMQ socket file or use inet socket auto increment
env.use_zmq_socket_file = True

env.AT_BASE_LOGDIR = '/var/log/connectors-rt'

env.ADC_HOSTNAME = 'pa4-adc1-prd.canaltp.prod'

""" default environment variables
    /!\ To overwrite these defaults, define it in the corresponding env below
    not here !
"""
# manual_package_deploy is used if we want to deploy custom debian package
# if false we only update the package from the debian repository
env.manual_package_deploy = False

# backup all configuration files before uploading a new one
env.backup_conf_files = False

#postgis dir is usefull for old postgis version where we cannot  do a 'create extention'
env.postgis_dir = '/usr/share/postgresql/9.1/contrib/postgis-1.5'

# if only one machine host all services
# only overriden to False on production and exploit envs
env.standalone = True
env.use_load_balancer = False
# some envronment use nfsv4 which does not allow chmod
env.use_nfs4 = False

# brokker == brokk == rabbitmq
# used by tyr, kraken, ...
# only overwritten on exploit and prod
env.rabbitmq_host = 'localhost'
env.rabbitmq_port = 5672

env.stat_broker_exchange = 'stat_persistor_exchange'

# tyr instance, jormungangr, and other database host
# no need to change this, works if the server is standalone or if it use a
# remote postgresql server

# redis host used by tyr and jormungandr
env.redis_host = 'localhost'
env.redis_port = 6379

# ed/tyr base dir
env.ed_basedir = '/srv/ed'
env.ed_datadir = '/srv/data'

##############################
# jormungandr
##############################
env.jormungandr_base_dir = '/srv/jormungandr'
env.jormungandr_wsgi_file = os.path.join(env.jormungandr_base_dir,
                                         'jormungandr.wsgi')
env.jormungandr_settings_file = os.path.join(env.jormungandr_base_dir,
                                          'settings.py')

# apache conf is usually not handled by fabric, but when it is (for docker for example)
# we do not use virtualhost, so all is in conf.d
env.jormungandr_apache_config_file = '/etc/apache2/conf.d/jormungandr.conf'

env.jormungandr_url = 'localhost'
env.jormungandr_port = 80
env.jormungandr_listen_port = env.jormungandr_port
env.jormungandr_save_stats = True
env.jormungandr_is_public = False

env.jormungandr_log_dir = '/var/log/jormungandr/'
env.jormungandr_log_file = os.path.join(env.jormungandr_log_dir, 'jormungandr.log')
env.jormungandr_instances_dir = '/etc/jormungandr.d'
env.jormungandr_log_level = 'INFO'

# index of the redis data base used (integer from 0 to 15)
env.jormungandr_redis_db = 0
env.jormungandr_redis_password = None

# stat_persitor and rt (?)
env.jormungandr_broker_username = 'guest'
env.jormungandr_broker_password = 'guest'

# jormungandr: kraken instance socket:
# [instance]
# key = bretagne
# socket = tcp://10.93.4.63:30001
# Note: only production need to override this
env.jormungandr_instance_socket = 'localhost'

env.jormungandr_default_handler = 'default'
env.jormungandr_syslog_facility = 'local7'

##############################
# kraken
##############################

# base dir for kraken binary and configuration
env.kraken_basedir = '/srv/kraken'

# log dir for all kraken instances, no need to change this
env.kraken_log_basedir = '/var/log/kraken'
env.kraken_log_name = '{}/navitia'.format(env.kraken_log_basedir)

# kraken rabbitmq connections parameters
# used in the kraken/kraken.ini.jinja template
#

env.kraken_broker_port = 5672
env.kraken_broker_username = 'guest'
env.kraken_broker_password = 'guest'
env.kraken_broker_vhost = '/'
env.kraken_broker_exchange = 'navitia'

# name of kraken database, no need to change this
env.kraken_data_nav = 'data.nav.lz4'

# log parameters
#
env.kraken_log_level = 'INFO'

env.kraken_log_max_backup = 5
# after this size (in MB), rotation done automatically by log4cplus lib
env.kraken_log_max_size = 20

# only used if syslog mode used instead of file
env.kraken_syslog_facility = 'local7'
env.kraken_syslog_ident = 'kraken'

# We use apache wsgi to monitor kraken
env.kraken_monitor_port = 80
env.kraken_monitor_location_dir = 'monitor-kraken'
env.kraken_monitor_listen_port = env.kraken_monitor_port
env.kraken_monitor_basedir = '/srv/monitor'
env.kraken_monitor_wsgi_file = os.path.join(env.kraken_monitor_basedir, 'monitor.wsgi')
env.kraken_monitor_config_file = os.path.join(env.kraken_monitor_basedir, 'settings.py')
env.kraken_monitor_apache_config_file = '/etc/apache2/conf.d/monitor-kraken'

##############################
# tyr
##############################

# rabbitmq username/password
env.tyr_broker_username = 'guest'
env.tyr_broker_password = 'guest'
env.tyr_broker_exchange = 'navitia'

env.tyr_base_instances_dir = '/etc/tyr.d'
env.tyr_basedir = '/srv/tyr'
env.tyr_base_logdir = '/var/log/tyr'
env.tyr_base_logfile = os.path.join(env.tyr_base_logdir, 'tyr.log')
env.tyr_logfile_pattern = os.path.join(env.tyr_base_logdir, '%(name).log')
env.tyr_migration_dir = os.path.join(env.tyr_basedir, 'migrations')
env.tyr_settings_file = os.path.join(env.tyr_basedir, 'settings.py')
env.tyr_settings_file_sh = os.path.join(env.tyr_basedir, 'settings.sh')
env.tyr_wsgi_file = os.path.join(env.tyr_basedir, 'settings.wsgi')
env.tyr_beat_service_file = '/etc/init.d/tyr_beat'
env.tyr_worker_service_file = '/etc/init.d/tyr_worker'
env.tyr_reloader_service_file = '/etc/init.d/tyr_reloader'

env.tyr_ws_url = 'localhost'
env.tyr_ws_port = 86

env.use_syslog = True
env.tyr_default_handler = 'default'
env.tyr_default_handler_instance = 'instance'
env.tyr_syslog_facility = 'local7'


# tyr share the same database as jormungandr
env.tyr_postgresql_database = 'jormungandr'
env.tyr_postgresql_user = 'jormungandr'
env.tyr_postgresql_password = 'jormungandr'

# redis
env.tyr_redis_password = None
# index of the database use in redis, between 0 and 15 by default
env.tyr_redis_db = 0

# smtp checks are not really possible when the server don't have direct smtp
# access (which should be always the case)
env.tyr_check_mx = False
env.tyr_check_smtp = False

#token for fabric to be able to query jormungandr
env.token = ''

#parameter to allow fabric to kill old tyr worker still alive after service stop
env.kill_ghost_tyr_worker = True

# default is to do things
env.dry_run = False

#number of parallele binarization
env.nb_thread_for_bina = 1

#instances configurations
env.instances = {}

# those 3 strings template will be formated with base = tyr base directory and instance = name of the instance
env.tyr_backup_dir_template = '{base}/backup'
env.tyr_source_dir_template = '{base}/source'
env.tyr_destination_dir_template = '{base}/destination'

env.kraken_database_file = '{base_dest}/{instance}/data.nav.lz4'

#in general we don't want to configure apache
env.setup_apache = False

env.cities_database_uri = None

#use protobuff cpp implementation (needs up to date probobuf version (at least 2.6))
env.use_protobuf_cpp = False

env.is_prod = False

@task
def let(**kwargs):
    """
    This function is a way to give env variables in the cli

    call then

    fab dev let:x=bob,z=toto upgrade_all

    to have a env.x and env.z variable
    """
    env.update(kwargs)


@task
def really_run():
    """ If called set dry_run as false """
    print(yellow("WARNING: really_run() is now deprecated and dry_run is always"
        "set to 'False'. Use dry_run() to set it to 'True'"))

def dry_run():
    """ If called set dry_run as true """
    env.dry_run = True


""" Environnements """

@task
def use(module_path, *args):
    pos = module_path.rfind(".")
    if pos == -1:
        path, f_name = module_path, module_path
    else:
        path, f_name = module_path[:pos], module_path[pos+1:]
    module = import_module(path)
    getattr(module, f_name)(*args)


""" Include or exclude instances """

@task
def include(*args):
    """
    include only the listed instances when running a fabric command
    :param args: instance names, as of 1st parameter of add_instance()
    """
    for name in args:
        if name not in env.instances:
            raise ValueError("Unknown instance '{}'".format(name))
    for name in list(env.instances):
        if not name in args:
            del env.instances[name]


@task
def exclude(*args):
    """
    exclude all the listed instances when running a fabric command
    :param args: instance names, as of 1st parameter of add_instance()
    """
    for name in args:
        try:
            del env.instances[name]
        except KeyError:
            raise ValueError("Unknown instance '{}'".format(name))

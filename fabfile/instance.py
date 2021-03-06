from fabric.api import env
import os

all_zmq_ports = [0]

def get_next_zmq_socket():
    port = max(all_zmq_ports) + 1
    all_zmq_ports.append(port)
    return 'tcp://*:{}'.format(env.KRAKEN_START_PORT + port)


class Instance:
    def __init__(self, name, db_password, db_local='fr_FR.UTF8',
                 is_free=False, chaos_database=None, rt_topics=[],
                 zmq_socket_port=None, db_name=None, db_user=None, source_dir=None):
        self.name = name
        self.db_password = db_password
        self.is_free = is_free
        if env.use_zmq_socket_file:
            self.kraken_zmq_socket = 'ipc://{kraken_dir}/{instance}/kraken.sock'.format(kraken_dir=env.kraken_basedir, instance=self.name)
            self.jormungandr_zmq_socket_for_instance = self.kraken_zmq_socket
        else:
            if zmq_socket_port is not None and env.zmq_server is not None:
                # kraken needs to listen to all but jomgandr needs to communicates with the engine
                self.kraken_zmq_socket = 'tcp://*:{port}'.format(port=zmq_socket_port)
                self.jormungandr_zmq_socket_for_instance = 'tcp://{server}:{port}'.format(server=env.zmq_server, port=zmq_socket_port)
                all_zmq_ports.append(zmq_socket_port)
            else:
                print 'no zmq configuration defined, use default'
                self.kraken_zmq_socket = get_next_zmq_socket()
                self.jormungandr_zmq_socket_for_instance = self.kraken_zmq_socket
        self.kraken_nb_threads = env.KRAKEN_NB_THREADS
        self.db_local = db_local
        self.chaos_database = chaos_database
        self.rt_topics = rt_topics
        # postgres doesn't like dash, replace them by underscore
        self.db_name = db_name if db_name else 'ed_' + self.name.replace('-', '_')
        self.db_user = db_user if db_user else 'ed_' + self.name.replace('-', '_')
        self._source_dir = source_dir if source_dir != 'auto' else '/srv/ed/source/{}/{}/FUSIO/EXPORT/'.\
            format(self.name.upper(), (getattr(env, 'fusio_name', None) or env.name).upper())

    #we might want to overload all those properties

    @property
    def target_lz4_file(self):
        return "{base_dest}/{instance}/data.nav.lz4".format(base_dest=env.tyr_base_destination_dir, instance=self.name)

    @property
    def kraken_database(self):
        return env.kraken_database_file.format(base_dest=env.tyr_base_destination_dir, instance=self.name, ed_basedir=env.ed_basedir)

    @property
    def base_destination_dir(self):
        return "{base_dest}/{instance}".format(base_dest=env.tyr_base_destination_dir, instance=self.name)

    @property
    def target_tmp_file(self):
        return "{base}/{instance}/datatmp.nav.lz4".format(base=env.ed_basedir, instance=self.name)

    # @property
    # def target_lz4_file(self):
    #     #return "{base}/{instance}/data.nav.lz4".format(base=env.tyr_base_destination_dir, instance=self.name)
    #     return "{}/data.nav.lz4".format(base=env.tyr_base_destination_dir, instance=self.name)

    @property
    def base_ed_dir(self):
        return "{base}/{instance}".format(base=env.ed_basedir, instance=self.name)

    @property
    def backup_dir(self):
        return env.tyr_backup_dir_template.format(base=env.ed_basedir, instance=self.name)

    @property
    def source_dir(self):
        if self._source_dir:
            return self._source_dir
        return env.tyr_source_dir_template.format(base=env.ed_basedir, instance=self.name)

    @property
    def kraken_basedir(self):
        return "{kraken_dir}/{instance}".format(kraken_dir=env.kraken_basedir, instance=self.name)

    @property
    def jormungandr_config_file(self):
        return os.path.join(env.jormungandr_instances_dir, self.name + '.ini')


def add_instance(name, db_pwd, **kwargs):
    env.instances[name] = Instance(name, db_pwd, **kwargs)



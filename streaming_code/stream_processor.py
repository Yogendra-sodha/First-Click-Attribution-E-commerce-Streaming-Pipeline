# this python script consumes data from kafka producers and topic
# Then it difenes sql table trhough flink table api which stays in kafka topic
# but does not store data and modified execution time and state
# though datastream api and executes the sql queries and outputs data in sinks table
# defined in the code

# req jars
# class streamjob,kafka,click,checkout,application users, application database,application_attibuted

from dataclasses import asdict, dataclass, field
from typing import List,Tuple

from jinja2 import Environment, FileSystemLoader
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment


REQUIRED_JARS = [
    "file:///opt/flink/flink-sql-connector-kafka-1.17.0.jar",
    "file:///opt/flink/flink-connector-jdbc-3.0.0-1.16.jar",
    "file:///opt/flink/postgresql-42.6.0.jar",
]

@dataclass(frozen=True)
class Stream_job_config:
    job_name : str = "checkout-attribution"
    jars : List[str] = field(default_factory = lambda : REQUIRED_JARS)
    spanshot_checkout : int = 10
    spanshot_pause : int = 5
    spanshot_timeout : int =  5
    parellelism : int = 2

@dataclass(frozen=True)
class Kafka_config:
    connector : str = 'kafka'
    bootstrap_servers : str = 'kafka:9092'
    scan_startup_mode : str = 'earliest-offset'
    consumer_group_id : str = 'flink-consumer-group-1'

@dataclass(frozen=True)
class Click_conifig(Kafka_config):
    topic : str = 'clicks'
    format : str = 'json'

@dataclass(frozen=True)
class Checkout_conifig(Kafka_config):
    topic : str = 'checkouts'
    format : str = 'json'

@dataclass(frozen=True)
class Database_config:
    connector : str = 'jdbc'
    url : str = 'jdbc:postgresql://postgres:5432/postgres'
    username : str = 'postgres'
    password : str = 'postgres'
    driver : str = 'org.postgresql.Driver'


@dataclass(frozen=True)
class Users_table_config(Database_config):
    table_name : str = 'commerce.users'

@dataclass(frozen=True)
class Attribute_checkouts_config(Database_config):
    table_name : str = 'commerce.attributed_chceckouts'


def get_attribute_checkouts(config : Stream_job_config) -> tuple[StreamExecutionEnvironment, StreamTableEnvironment]:
    # calling datastream api and creating environment
    s_env = StreamExecutionEnvironment.get_execution_environment()

    # installing required jars in environment
    for jars in config.jars:
        s_env.add_jars(jars)

    # Intializing checkpoints to take snapshots of process every 10s for backup
    s_env.enable_checkpointing(config.spanshot_checkout*1000)

    # Adding pause to after snapshot of 5s to have some progress in process
    s_env.get_checkpoint_config().set_min_pause_between_checkpoints(config.spanshot_pause*1000)

    # Adding timeout for checkpoints if they are completed within 5 minutes it will eliminate
    s_env.get_checkpoint_config().set_checkpoint_timeout(config.spanshot_timeout * 1000)

    # executing parlellism
    exec_config = s_env.get_config()
    exec_config.set_parallelism(config.parellelism)

    # Using configuration defined in datastream env to process stream table environment
    t_env = StreamTableEnvironment.create(s_env)
    table_config = t_env.get_config().get_configuration()
    table_config.set_string("pipline_name",config.job_name)
    return s_env,t_env

def get_sql_query(entity : str, 
                  type : str = 'source', 
                  template_env : Environment = Environment(loader = FileSystemLoader("code/"))) -> str:
    config_map = {
        'clicks' : Click_conifig(),
        'checkouts' : Checkout_conifig(),
        'users' : Users_table_config(),
        'attribute_checkouts' : Attribute_checkouts_config(),
        'attributed_checkouts' : Users_table_config()
    }

    return template_env.get_template(f"{type}/{entity}.sql").render(asdict(config_map.get(entity)))

def process_attribution_jobs(t_env : StreamTableEnvironment,
                             get_sql_query = get_sql_query) -> None:
    
    # executing sql table and rendering as dict object as defined in get_sql_query function
    # to perform joins and aggregations
    t_env.execute_sql(get_sql_query('clicks'))
    t_env.execute_sql(get_sql_query('checkouts'))
    t_env.execute_sql(get_sql_query('users'))

    # executing sql table for sink
    t_env.execute_sql(get_sql_query('attributed_checkouts','sink'))

    # excuting the process that 
    stat_exec = t_env.create_statement_set()
    stat_exec.add_insert_sql(get_sql_query('attribute_checkouts','process'))

    checkout_attribution_job = stat_exec.execute()
    print(
        f"""
        Async attributed checkouts sink job
         status: {checkout_attribution_job.get_job_client().get_job_status()}
        """
    )

if __name__ == "__main__":
    s_env,t_env = get_attribute_checkouts(Stream_job_config())
    process_attribution_jobs(t_env)
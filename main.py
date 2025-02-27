import argparse

from cognitive_base.examples.coala_coder.coala_agent import CoalaAgent

from cognitive_base.knowledge_sources.loaders import load_agent_memory
from cognitive_base.utils.log import setup_logging_n_base_dirs
from cognitive_base.examples.voyager_coder.argparsers import add_base_voyager_args

from agent_expt_suite.eval_setup.argparsers import get_base_agent_parser
from agent_expt_suite.eval_setup import core as c
from agent_expt_suite.eval_setup.log import VerboseHandler

from data_tools.dataset_registry_updates import dataset_registry_updates

from config.experiment_args import add_experiment_args


def get_args() -> argparse.Namespace:
    parser = get_base_agent_parser()
    add_base_voyager_args(parser)
    add_experiment_args(parser)
    return parser.parse_args()

def main(args):
    setup_logging_n_base_dirs(args)
    c.initialize_directories(args)
    c.initialize_environment(args)
    c.save_args(args)

    handler = VerboseHandler(verbose=args.verbose)
    actor = CoalaAgent(args, {}, handler)

    c.attach_env_to_agent(args, actor)
    load_agent_memory(args, actor)
    c.load_train_data(args, actor, dataset_registry_updates=dataset_registry_updates)

    c.train_agent(args, actor)
    
    c.evaluate_agent(args, actor)

    c.cleanup(args)


if __name__ == "__main__":
    args = get_args()
    # set_debug(True)
    # set_verbose(True)
    main(args)

def add_experiment_args(parser):
    group = parser.add_argument_group('experiment')
    group.add_argument(
        "--disable_episodic", 
        action="store_true",
        help="Disable episodic memory (both storage and retrieval)"
    )
    # Placeholder args for future features
    # group.add_argument("--disable_semantic", action="store_true")
    # group.add_argument("--disable_procedural", action="store_true")
    # group.add_argument("--disable_reflection", action="store_true")
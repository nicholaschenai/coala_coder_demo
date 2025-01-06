import os
import json

from tqdm import tqdm

from agent_expt_suite.data_tools.APPS.APPS_data_pipeline import APPSDataPipeline
from agent_expt_suite.data_tools.APPS.APPS_data_utils import apps_filter_fn


class CustomAPPSDataPipeline(APPSDataPipeline):
    """
    custom pipeline where we filter out data points for coala experiment
    """
    def __init__(self, dataset_name="APPS", train=True, **kwargs):
        super().__init__(dataset_name, train, **kwargs)
        # Get directory of current file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.filtered_indices_path = os.path.join(current_dir, "cache", "filtered_indices.json")
        self.solution_idxs_path = os.path.join(current_dir, "cache", "solution_idxs.json")

        # Create cache directory if it doesn't exist
        os.makedirs(os.path.dirname(self.filtered_indices_path), exist_ok=True)

        self.dataset = None

        # Load or initialize solution codes cache
        if os.path.exists(self.solution_idxs_path):
            with open(self.solution_idxs_path, 'r') as f:
                self.solution_idxs = json.load(f)
        else:
            self.solution_idxs = {}

    def filter_dataset(self, dataset, dataloader):
        """
        Filter dataset based on difficulty and apps_filter_fn results.
        Uses caching to avoid recomputing expensive apps_filter_fn.
        Stores individual results to handle interruptions gracefully.

        Returns:
            filtered_dataset: The filtered dataset
            filter_metadata: Dict containing info about the filtering (e.g., indices kept)
        """
        dataset = dataset.filter(lambda x: x['difficulty'] == 'interview')

        # Load or initialize the filter results cache
        if os.path.exists(self.filtered_indices_path):
            with open(self.filtered_indices_path, 'r') as f:
                filter_results = json.load(f)
        else:
            filter_results = {}
        
        # Process any indices that haven't been filtered yet
        if len(filter_results) != len(dataset):
            for i, example in tqdm(enumerate(dataset), total=len(dataset), desc="Filtering dataset"):
                if str(i) not in filter_results:
                    passes_filter, p_id = apps_filter_fn(example)
                    filter_results[str(i)] = passes_filter
                    
                    # If passes filter, store the solution idx
                    if passes_filter and p_id:
                        self.solution_idxs[p_id] = example['soln_idx']
                        with open(self.solution_idxs_path, 'w') as f:
                            json.dump(self.solution_idxs, f)
                    
                    # Save after each new result to handle interruptions
                    with open(self.filtered_indices_path, 'w') as f:
                        json.dump(filter_results, f)
        # Get indices that passed both filters and sort for consistency
        filtered_indices = sorted([int(idx) for idx, passed in filter_results.items() if passed])
        
        # Create filtered dataset and shuffle using HuggingFace's built-in method
        filtered_dataset = dataset.select(filtered_indices).shuffle(seed=42)

        return filtered_dataset, dataloader

    def attach_to_agent(self, actor):
        dataset, _ = self.get_dataloader()
        self.dataset = dataset
        actor.data_pipeline = self
        print(f"Actor's data_pipeline after attachment: {actor.data_pipeline}")
        actor.env_interface.enable_input_hints = True

    def get_next_task(self, idx):
        example = self.dataset[idx]
        p_id = str(example['problem_id'])
        soln_idx = self.solution_idxs[p_id]
        full_task = self.preprocess(example, soln_idx=soln_idx)
        return full_task

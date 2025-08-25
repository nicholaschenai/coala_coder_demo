# Common experiment folder configuration

# Test experiments
EXPERIMENTS = {
    'ReAct': {
        '4o_mini': './final_results/react_test_4o_mini',
        '4o_0806': './final_results/react_test_4o_0806'
    },
    'RAG': {
        '4o_mini': './final_results/rag_test_k_3_4o_mini',
        '4o_0806': './final_results/rag_test_k_1_4o_0806'
    },
    'CoALA': {
        '4o_mini': './final_results/coala_test_k_3_disable_episodic_4o_mini',
        '4o_0806': './final_results/coala_test_k_1_4o_0806'
    }
}

SELECTED_TRAIN_EXPERIMENTS = {
    'CoALA Train': {
        '4o_mini': './final_results/coala_train_apps_k_3_disable_episodic_4o_mini',
        '4o_0806': './final_results/coala_train_apps_k_1_4o_0806'
    }
}

ALL_TRAIN_EXPERIMENTS = {
    'CoALA Train': {
        '4o_mini_k_1': './final_results/coala_train_apps_k_1_4o_mini',
        '4o_mini_k_2': './final_results/coala_train_apps_k_2_4o_mini',
        '4o_mini_k_3': './final_results/coala_train_apps_k_3_4o_mini',
        '4o_0806_k_1': './final_results/coala_train_apps_k_1_4o_0806',
        '4o_0806_k_2': './final_results/coala_train_apps_k_2_4o_0806',
        '4o_0806_k_3': './final_results/coala_train_apps_k_3_4o_0806',
        '4o_mini_k_3_no_ep': './final_results/coala_train_apps_k_3_disable_episodic_4o_mini',
        '4o_0806_k_1_no_ep': './final_results/coala_train_apps_k_1_disable_episodic_4o_0806'
    }
}

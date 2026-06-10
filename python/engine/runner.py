import importlib
import time
import random
import numpy as np


def set_seed(seed):
    if seed is None:
        return
    random.seed(seed)
    np.random.seed(seed)


def run_system(system_name: str, config):
    module = importlib.import_module(f"systems.{system_name}")

    if not hasattr(module, "run"):
        raise Exception(f"{system_name} no tiene run(config)")

    set_seed(config.seed)

    start = time.time()
    module.run(config)
    end = time.time()

    print("\n----------------------------")
    print(f"⏱ Tiempo: {end - start:.3f}s")
    print("----------------------------\n")
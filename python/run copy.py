import argparse
from engine.config import Config
from engine.runner import run_system


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("system", choices=["henon", "julia", "rossler", "lorenz"])
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--points", type=int, default=10000)
    parser.add_argument("--dt", type=float, default=0.01)

    args = parser.parse_args()

    config = Config(
        system=args.system,
        seed=args.seed,
        points=args.points,
        dt=args.dt
    )

    print(f"\n🚀 Running {args.system}...\n")

    run_system(args.system, config)


if __name__ == "__main__":
    main()
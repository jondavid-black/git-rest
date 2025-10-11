import os

from git_rest.app import create_app


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Launch git-rest server.")
    parser.add_argument(
        "--workdir",
        type=str,
        default=os.getcwd(),
        help="Working directory for the server",
    )
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host to bind")
    parser.add_argument("--port", type=int, default=5000, help="Port to bind")
    args = parser.parse_args()

    os.chdir(args.workdir)
    app = create_app()
    app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    main()

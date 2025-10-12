import subprocess
import time

import requests


def before_feature(context, feature):
    # Start the API server using the 'git-rest' CLI script
    import os

    workdir = "./test_working_dir"
    os.makedirs(workdir, exist_ok=True)
    context.api_process = subprocess.Popen(
        [
            "uv",
            "run",
            "git-rest-debug",
            "--workdir",
            workdir,
            "--host",
            "127.0.0.1",
            "--port",
            "5000",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    # Wait for the server to be up
    for _ in range(40):
        try:
            resp = requests.get("http://127.0.0.1:5000/healthz")
            if resp.status_code == 200:
                break
        except Exception:
            time.sleep(0.05)
    else:
        # Print server stdout and stderr for debugging
        try:
            out, err = context.api_process.communicate(timeout=2)
        except Exception:
            out, err = "", ""
        print("\n[BDD DEBUG] Server stdout:\n", out)
        print("\n[BDD DEBUG] Server stderr:\n", err)
        raise RuntimeError("API server did not start in time.")


def after_feature(context, feature):
    # Shut down the API server
    if hasattr(context, "api_process"):
        context.api_process.terminate()
        try:
            stdout, stderr = context.api_process.communicate(timeout=10)
        except Exception:
            stdout, stderr = "", ""
        print("\n--- API SERVER STDOUT ---\n" + (stdout or "<no stdout>"))
        print("\n--- API SERVER STDERR ---\n" + (stderr or "<no stderr>"))

    # Clean up the test repository directory
    import os
    import shutil

    tmp_repo_path = "/tmp/git-rest"
    if os.path.exists(tmp_repo_path):
        shutil.rmtree(tmp_repo_path)

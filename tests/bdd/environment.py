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
            "0.0.0.0",
            "--port",
            "5000",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    time.sleep(1)
    context.api_process.terminate()
    try:
        stdout, stderr = context.api_process.communicate(timeout=10)
    except Exception as e:
        print("Environment exception during initial start/stop: " + str(e))
        stdout, stderr = None, None
    print("\n--- API SERVER START STDOUT ---\n" + (stdout or "<no stdout>"))
    print("\n--- API SERVER START STDERR ---\n" + (stderr or "<no stderr>"))

    # Wait for the server to be up
    for _ in range(20):
        try:
            resp = requests.get("http://localhost:5000/healthz")
            if resp.status_code == 200:
                break
            else:
                print("Waiting for API server to start...")
                time.sleep(0.2)
        except Exception as e:
            print("Environment exception: " + str(e))
            time.sleep(0.2)
    else:
        # Print server stdout and stderr for debugging
        try:
            out, err = context.api_process.communicate(timeout=2)
        except Exception:
            out, err = '', ''
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

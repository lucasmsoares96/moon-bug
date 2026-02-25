import subprocess


def docker_clean():
    ids = subprocess.check_output(["docker", "ps", "-aq"]).split()

    if ids:
        subprocess.run(["docker", "stop"] + ids, stdout=subprocess.DEVNULL)
        subprocess.run(["docker", "rm"] + ids, stdout=subprocess.DEVNULL)


if __name__ == "__main__":
    docker_clean()

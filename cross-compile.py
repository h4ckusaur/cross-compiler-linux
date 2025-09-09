import subprocess
import sys
import os
import requests
import re

DOCKER_HUB_API = "https://hub.docker.com/v2/repositories/library/"

def search_images(name, version):
    """Search Docker Hub for images matching name and version."""
    images = []
    page = 1
    while True:
        response = requests.get(f"{DOCKER_HUB_API}{name}/tags?page_size=100&page={page}")
        response.raise_for_status()
        results = response.json()
        for r in results["results"]:
            tag = r["name"]
            # Match version anywhere in the tag and include slim/minimal if present
            if version in tag:
                images.append(tag)
        if not results["next"]:
            break
        page += 1
    return images

def choose_image(images):
    """Let user choose an image if multiple are available."""
    if not images:
        print("No matching images found.")
        sys.exit(1)
    elif len(images) == 1:
        return images[0]

    print("Multiple matching images found:")
    for i, img in enumerate(images, 1):
        print(f"{i}. {img}")
    choice = int(input("Choose an image by number: ")) - 1
    return images[choice]

def parse_makefile(makefile_path):
    """Parse Makefile for available targets."""
    targets = []
    with open(makefile_path, "r") as f:
        for line in f:
            match = re.match(r'^([a-zA-Z0-9_\-\.]+)\s*:', line)
            if match and match.group(1) != "all":
                targets.append(match.group(1))
    return targets

def build_and_compile(directory, distro, version):
    os.chdir(directory)
    makefile_path = os.path.join(directory, "Makefile")
    make_found = False

    # Determine build command
    if os.path.exists(makefile_path):
        print("Makefile detected!")
        targets = parse_makefile(makefile_path)
        if targets:
            print("Available targets:")
            for i, t in enumerate(targets, 1):
                print(f"{i}. {t}")
            choice = input("Enter the target to build (default: all): ").strip()
            target = choice if choice else "all"
        else:
            target = "all"
        build_cmd = f"make {target}"
        make_found = True
    else:
        # Find the first C file if no Makefile
        c_files = [f for f in os.listdir(directory) if f.endswith(".c")]
        if not c_files:
            print("No C files found in this directory and no Makefile exists.")
            sys.exit(1)
        c_file = c_files[0]
        build_cmd = f"gcc -o output {c_file}"

    # Find candidate images
    images = search_images(distro, version)
    chosen_tag = choose_image(images)
    image_name = f"crosscompile:{chosen_tag}"

    # Prepare Dockerfile dynamically
    dockerfile_content = f"""
    FROM {distro}:{chosen_tag}
    WORKDIR /workspace
    RUN apt-get update && apt-get install -y build-essential
    COPY . /workspace
    CMD {build_cmd}
    ARG TZ=America/New_York
    ENV TZ=$TZ
    ENV DEBIAN_FRONTEND=noninteractive
    """
    with open("Dockerfile", "w") as f:
        f.write(dockerfile_content)

    # Build the Docker image
    subprocess.run(["docker", "build", "-t", image_name, "."], check=True)

    # Run the container
    subprocess.run([
        "docker", "run", "--rm", "-v", f"{directory}:/workspace", image_name,
        "bash", "-c", f"apt-get update && apt-get install -y build-essential musl-tools libmnl-dev libnftnl-dev && {build_cmd}"
    ], check=True)

    # Cleanup image
    subprocess.run(["docker", "rmi", "-f", image_name], check=True)
    print(f"Image {image_name} removed to save space.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python cross_compile.py <directory> <distro> <version>")
        print("Example: python cross_compile.py . ubuntu 20.04")
        sys.exit(1)

    directory = sys.argv[1]
    distro = sys.argv[2]
    version = sys.argv[3]

    build_and_compile(directory, distro, version)

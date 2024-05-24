import os
import subprocess
from vimbot.config import settings


def get_docs():
    """
    Perform a shallow fetch and checkout the specified folder from the remote repository.
    """
    repo_url = settings.REPO_URL
    target_dir = settings.RESOURCE_FOLDER
    folder_name = (
        "docs"  # Replace with the desired folder name (from the remote repository)
    )

    print(
        f"Starting shallow fetch and checkout of '{folder_name}' folder from {repo_url}"
    )
    repo_name = os.path.basename(repo_url).replace(".git", "")
    print(f"Repository name: {repo_name}")

    if not os.path.exists(target_dir):
        # Create the target directory if it doesn't exist
        os.makedirs(target_dir)

    # Change to the target directory
    os.chdir(target_dir)

    if not os.path.exists(".git"):
        # Initialize a new Git repository in the target directory if it doesn't exist
        print(f"Initializing a new Git repository in {target_dir}")
        subprocess.run(["git", "init"], check=True)

        # Set up the repository to use sparse checkout
        print("Setting up sparse checkout")
        subprocess.run(["git", "config", "core.sparseCheckout", "true"], check=True)

        # Add the remote repository
        print(f"Adding remote repository: {repo_url}")
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)

    # Specify the folder you want to checkout
    print(f"Specifying the folder to checkout: {folder_name}/")
    with open(".git/info/sparse-checkout", "w") as f:
        f.write(f"{folder_name}/\n")

    # Fetch the latest changes from the remote repository with a depth of 1
    print("Fetching the latest changes from the remote repository with a depth of 1")
    subprocess.run(["git", "fetch", "--depth", "1", "origin", "main"], check=True)

    # Checkout the specified folder from the remote repository
    print(f"Checking out the '{folder_name}' folder from the remote repository")
    subprocess.run(["git", "checkout", "origin/main", folder_name], check=True)

    print(
        f"Shallow fetch and checkout of '{folder_name}' folder from {repo_url} completed."
    )


if __name__ == "__main__":
    get_docs()

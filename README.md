# Password Hasher

A simple Python command-line application that securely converts a user-provided password into a hashed value.

This project demonstrates a complete development workflow using **Python, automated testing, Docker, GitHub Actions, and GitHub Container Registry (GHCR)**.

The application is automatically tested and containerized whenever code is pushed to the `main` branch. If all tests pass, GitHub Actions builds a Docker image and publishes it to GHCR.

---

## Features

* Accepts a password through the command line
* Generates a hashed representation of the password
* Includes automated tests using `pytest`
* Packages the application using Docker
* Uses GitHub Actions for CI/CD
* Automatically builds a Docker image after successful tests
* Publishes the Docker image to GitHub Container Registry
* Allows the application to be downloaded and executed on any system with Docker

---

## Technologies Used

| Technology                | Purpose                      |
| ------------------------- | ---------------------------- |
| Python                    | Application development      |
| pytest                    | Automated testing            |
| Docker                    | Application containerization |
| Git                       | Version control              |
| GitHub                    | Source-code hosting          |
| GitHub Actions            | CI/CD automation             |
| GitHub Container Registry | Docker image storage         |

---

## Project Structure

```text
password-hash/
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── tests/
│   └── test_app.py
│
├── .dockerignore
├── .gitignore
├── app.py
├── Dockerfile
├── requirements.txt
└── README.md
```

### `app.py`

The main Python application.

It contains the password hashing functionality and accepts a password from the user through the command line.

---

### `tests/test_app.py`

Contains automated tests for the password hashing functionality.

The tests are executed using `pytest` before a Docker image is allowed to be built and published.

This helps ensure that changes to the application do not break its expected functionality.

---

### `requirements.txt`

Contains the Python dependencies required by the project.

Dependencies can be installed using:

```bash
pip install -r requirements.txt
```

The same file is also used by GitHub Actions when preparing the test environment.

---

### `Dockerfile`

Defines how the Docker image for the application is created.

The Dockerfile prepares the Python environment, copies the project files into the container, installs the required dependencies, and defines the command used to start the application.

---

### `.dockerignore`

Specifies files that Docker should ignore while building the image.

This prevents unnecessary files from being copied into the Docker image and helps keep the image clean and lightweight.

---

### `.gitignore`

Specifies files and directories that should not be tracked by Git, such as temporary Python files, cache files, or local environment files.

---

### `.github/workflows/ci.yml`

Defines the GitHub Actions CI/CD pipeline.

The workflow is triggered when:

* Code is pushed to the `main` branch
* A pull request is created against the `main` branch

The pipeline contains two main jobs:

1. Testing
2. Docker build and deployment

---

# How the Application Works

When the program starts, it asks the user to enter a password:

```text
Enter a password:
```

The application processes the password and produces its hashed representation.

Because the password is entered interactively, the Docker container must also be started in interactive mode.

---

# Running the Project Locally

## 1. Clone the Repository

```bash
git clone <repository-url>
```

Move into the project directory:

```bash
cd password-hash
```

---

## 2. Install Dependencies

Make sure Python is installed, then run:

```bash
pip install -r requirements.txt
```

---

## 3. Run the Application

```bash
python app.py
```

The application will ask:

```text
Enter a password:
```

Enter a password and press **Enter**.

---

# Running Automated Tests

The project uses `pytest` for automated testing.

Run the tests locally using:

```bash
python -m pytest
```

If the application behaves as expected, the tests should pass.

Example:

```text
tests/test_app.py PASSED
```

---

# Running with Docker

The application can also be executed inside a Docker container.

## Build the Docker Image

From the project directory, run:

```bash
docker build -t password-hasher .
```

---

## Run the Docker Container

Because the program requires keyboard input, Docker must be started using interactive mode:

```bash
docker run --rm -it password-hasher
```

The options mean:

* `-i` keeps standard input open
* `-t` creates an interactive terminal
* `--rm` automatically removes the stopped container

The application will then display:

```text
Enter a password:
```

---

# CI/CD Pipeline

The project uses **GitHub Actions** to automate testing, Docker image creation, and image publishing.

The workflow is defined in:

```text
.github/workflows/ci.yml
```

## Pipeline Flow

```text
Local Project
      │
      ▼
Push Code to GitHub (main)
      │
      ▼
GitHub Actions Workflow Triggered
      │
      ▼
┌─────────────────────────────┐
│         Test Job            │
│                             │
│ Checkout Repository         │
│          ↓                  │
│ Set Up Python               │
│          ↓                  │
│ Install Dependencies        │
│          ↓                  │
│ Run pytest                  │
└─────────────┬───────────────┘
              │
              ▼
         Tests Pass?
          /       \
        No         Yes
        │           │
        ▼           ▼
     Stop       Build-and-Push Job
                    │
                    ▼
          Checkout Repository
                    │
                    ▼
              Login to GHCR
                    │
                    ▼
           Build Docker Image
                    │
                    ▼
           Push Docker Image
                    │
                    ▼
      GitHub Container Registry
```

---

## Step 1: Push Code to GitHub

When changes are pushed to the `main` branch, GitHub detects the configured workflow and starts GitHub Actions.

---

## Step 2: GitHub-Hosted Runner

GitHub creates a temporary Ubuntu environment because the workflow uses:

```yaml
runs-on: ubuntu-latest
```

This temporary machine is called a **GitHub-hosted runner**.

The testing and Docker build processes are performed on these GitHub-hosted runners instead of on the developer's local computer.

---

## Step 3: Test Job

The first job checks the application before deployment.

GitHub Actions:

1. Checks out the repository
2. Sets up Python 3.12
3. Installs project dependencies
4. Runs the automated tests using `pytest`

The test command is:

```bash
python -m pytest
```

If the tests fail, the workflow stops and no Docker image is published.

---

## Step 4: Build-and-Push Job

The second job depends on the successful completion of the test job.

This relationship is defined using:

```yaml
needs: test
```

Therefore, the Docker image is only created when all automated tests pass.

The second job:

1. Checks out the repository again
2. Authenticates with GitHub Container Registry
3. Builds the Docker image using the `Dockerfile`
4. Pushes the image to GHCR

---

## Step 5: Docker Image Published to GHCR

After a successful build, the Docker image is published as:

```text
ghcr.io/anishadhikari02/password-hasher:latest
```

The `latest` tag represents the most recently published version of the image.

---

# Pulling the Published Docker Image

The Docker image can be downloaded directly from GitHub Container Registry.

```bash
docker pull ghcr.io/anishadhikari02/password-hasher:latest
```

Verify that the image exists locally:

```bash
docker images
```

---

# Running the Published Image

Run the downloaded image using:

```bash
docker run --rm -it ghcr.io/anishadhikari02/password-hasher:latest
```

The application will then request a password:

```text
Enter a password:
```

---

# CI vs CD in This Project

## Continuous Integration

The **CI** portion of the project includes:

```text
Push Code
    ↓
Checkout Repository
    ↓
Set Up Python
    ↓
Install Dependencies
    ↓
Run Automated Tests
```

This ensures that the application is tested whenever changes are introduced.

## Continuous Delivery

The **CD** portion includes:

```text
Tests Pass
    ↓
Build Docker Image
    ↓
Authenticate with GHCR
    ↓
Push Docker Image
    ↓
Store Image in GitHub Container Registry
```

This makes the tested application available as a Docker image that can be pulled and executed on another machine.

---

# Important CI/CD Behavior

The Docker build job runs only when the workflow is triggered by a `push`.

The workflow contains:

```yaml
if: github.event_name == 'push'
```

Therefore:

```text
Pull Request
    ↓
Tests Run
    ↓
No Docker Image Push
```

while:

```text
Push to main
    ↓
Tests Run
    ↓
Tests Pass
    ↓
Docker Image Built
    ↓
Docker Image Pushed to GHCR
```

This prevents Docker images from being published unnecessarily during pull-request validation.

---

# Development Workflow

The normal development process for this project is:

```text
Modify Application Locally
        ↓
Test Changes
        ↓
Commit Changes with Git
        ↓
Push to GitHub
        ↓
GitHub Actions Runs
        ↓
Automated Tests
        ↓
Docker Image Build
        ↓
Publish to GHCR
        ↓
Pull and Run Image Anywhere
```

---

# Conclusion

This project demonstrates more than a simple Python password hashing application. It implements a complete automated software delivery workflow.

The project combines:

* Python application development
* Automated software testing
* Version control with Git
* Source-code management with GitHub
* Docker containerization
* GitHub Actions CI/CD
* Container image publishing through GHCR

The CI/CD pipeline ensures that the application is tested before a Docker image is created and published, providing a repeatable and automated development and deployment process.

# Environment variable setup for git-rest

The application requires the following environment variables:

- `GIT_REST_SECRET_KEY`: Secret key for session and security (required)
- `GIT_REST_WORKDIR`: Absolute path to the working directory for managed repositories (required)


## Demo UI Toggle

- `ENABLE_INTERACTIVE_DEMO`: Set to `1` to enable the interactive API demo UI at `/apidocs`. Set to `0` (or unset) to disable. (optional, default: disabled)

## Example

Copy `.env.example` to `.env` and edit the values:

```sh
cp .env.example .env
```

Then edit `.env` and set your values.

## Usage

When running locally, you can load environment variables automatically with [python-dotenv](https://pypi.org/project/python-dotenv/) or by exporting them manually:

```sh
export GIT_REST_SECRET_KEY="your-secret-key"
export GIT_REST_WORKDIR="/absolute/path/to/repos"
```

In Docker or CI, set these variables in your container or workflow environment.

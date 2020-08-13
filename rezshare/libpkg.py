

def sys_path_prepend(env):
    import os
    import sys

    for path in env.PYTHONPATH.value().split(os.path.pathsep):
        sys.path.insert(0, path)


def load_dotenv(file, env):
    from dotenv.main import DotEnv
    from dotenv.compat import to_env

    for key, value in DotEnv(file).dict().items():
        env[to_env(key)] = to_env(value)

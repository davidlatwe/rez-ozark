

def profiles():
    """Return list of profiles

    This function is called asynchronously, and is suitable
    for making complex filesystem or database queries.
    Can also be a variable of type tuple or list

    """
    # (TODO) Dev `produzer`, `produzer-gui` in rez-project !!
    #   * Or maybe we don't need gui, just set editor and provide a template
    #     package.py (or profile.py ?), then build into montydb or mongodb.

    # view: super set of profile `features` attributes
    #   REZ_VIEW=show.ongoing;dev.pipeline;

    # role: super set of profile `positions` attributes
    #   REZ_ROLE=artist;technical;developer;admin

    # produzer:
    #   Write profile package to MongoDB (or MontyDB for test)
    #   with `features`, `positions` attributes in here when profile
    #   package being built.
    #
    #   Read-only MongoDB rez repo plugin for allzpark, rez-env, rez-search...
    #   It will be version less. (mongoread)

    # rolez (uzer)

    # rez-produzed: git repo for profile packages, if you need git.

    try:
        # Read profile_model from file or database
        return ["test", "demo"]
    except IOError:
        return []

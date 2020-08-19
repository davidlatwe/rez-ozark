
from rez.config import config as config_
from rez.packages import iter_package_families


__mongozark = config_.plugins.package_repository.mongozark


def profiles():
    """Return list of profiles

    This function is called asynchronously, and is suitable
    for making complex filesystem or database queries.
    Can also be a variable of type tuple or list

    """
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

    return [
        pkg_family.name
        for pkg_family in iter_package_families(paths=__mongozark.profiles)
    ]


def applications():
    """Return list of applications

    Applications are typically provided by the profile,
    this function is called when "Show all apps" is enabled.

    """

    return []


def style_loader():
    try:
        from ozark import style
    except ImportError:
        print("Failed to load Ozark CSS stylesheet.")
        return

    return style.load_stylesheet()

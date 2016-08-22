devbox - tools for isolated development
=======================================

Sometimes you need to work on a project that needs to be isolated from
your normal development environment.  A simple solution is to spin up
a container (or a separate machine) and do your development in there.
However, that means having to set up that host before you can get to
work, which diminishes the simplicity of the approach.

"devbox" addresses that problem by automating host setup, including
container provisioning.  A script is provided as well as Python
libraries (used by the script).

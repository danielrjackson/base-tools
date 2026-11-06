# Native project-path helper

The qualified subset is `basetools.d_paths.BaseProjectPaths`, imported with the
repository's `src` directory on Python's module path. It uses only the standard
library. Creating a paths object leaves the filesystem unchanged; calling
`ensure_dirs_exist()` creates its `config` and `logs` directories and preserves
existing content.

An explicit root is retained as supplied. Automatic discovery starts at the working
directory and selects the nearest ancestor with `src`, `config` or `.git`; a Git
worktree's `.git` file is supported. Without a marker it retains the working
directory. Relative explicit roots retain their existing relative-path semantics.

Native checks use disposable paths with spaces, nested project markers and existing
content. Original source bytes are recoverable through the recorded text lineage.
The remaining modules and package/dependency metadata are preserved drafts and are
outside this qualification. No package installation or complete-library compatibility
claim follows from these helper checks.

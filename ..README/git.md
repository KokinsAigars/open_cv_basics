

untrack files in git

# Tell Git to stop tracking the Jupyter checkpoints
git rm -r --cached .ipynb_checkpoints

# Tell Git to stop tracking the trash folder
git rm -r --cached .Trash-0

# Commit the removal
git commit -m "chore: remove tracked jupyter temporary files"
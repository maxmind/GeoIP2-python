#!/bin/bash

set -eu -o pipefail

# Check that we're not on the main branch
current_branch=$(git branch --show-current)
if [ "$current_branch" = "main" ]; then
    echo "Error: Releases should not be done directly on the main branch."
    echo "Please create a release branch and run this script from there."
    exit 1
fi

changelog=$(cat HISTORY.rst)

regex='
([0-9]+\.[0-9]+\.[0-9]+) \(([0-9]{4}-[0-9]{2}-[0-9]{2})\)
\+*

((.|
)*)
'

if [[ ! $changelog =~ $regex ]]; then
      echo "Could not find date line in change log!"
      exit 1
fi

version="${BASH_REMATCH[1]}"
date="${BASH_REMATCH[2]}"
notes="$(echo "${BASH_REMATCH[3]}" | sed -n -e '/^[0-9]\+\.[0-9]\+\.[0-9]\+/,$!p')"

if [[ "$date" != "$(date +"%Y-%m-%d")" ]]; then
    echo "$date is not today!"
    exit 1
fi

tag="v$version"

if [ -n "$(git status --porcelain)" ]; then
    echo ". is not clean." >&2
    exit 1
fi

perl -pi -e "s/(?<=^version = \").+?(?=\")/$version/gsm" pyproject.toml

echo $"Test results:"
uv run tox

echo $'\nDiff:'
git diff

echo $'\nRelease notes:'
echo "$notes"

read -e -p "Commit changes and push to origin? " should_push

if [ "$should_push" != "y" ]; then
    echo "Aborting"
    exit 1
fi

git commit -m "Update for $tag" -a

git push

gh release create --target "$(git branch --show-current)" -t "$version" -n "$notes" "$tag"

git push --tags

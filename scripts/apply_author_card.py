"""Append a standardized author card to every README in a repository list."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path


def apply_card(repo: Path, template: str) -> bool:
    readme = repo / "README.md"
    if not readme.is_file():
        return False
    original = readme.read_text(encoding="utf-8")
    marker = "## 👤 Autor"
    if marker in original:
        prefix = original.split(marker, 1)[0].rstrip()
    else:
        prefix = original.rstrip()
    updated = prefix + "\n\n" + template.strip() + "\n"
    readme.write_text(updated, encoding="utf-8")

    logo = repo / "assets" / "logo-cesar.png"
    if not logo.is_file():
        logo.parent.mkdir(parents=True, exist_ok=True)
        source = repo.parent.parent / "skill-lattes" / "assets" / "logo-cesar.png"
        if source.is_file():
            shutil.copy2(source, logo)
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--template", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    repos = json.loads(args.manifest.read_text(encoding="utf-8"))
    template = args.template.read_text(encoding="utf-8")
    changed = []
    for name in repos:
        repo = args.repo_root / name
        if apply_card(repo, template):
            changed.append(name)
            if args.commit:
                subprocess.run(["git", "-C", str(repo), "add", "README.md", "assets/logo-cesar.png"], check=False)
                subprocess.run(
                    ["git", "-C", str(repo), "-c", "user.name=Cleyber Silva",
                     "-c", "user.email=cleybersilva@users.noreply.github.com",
                     "commit", "-m", "Standardize author card in README"],
                    check=False,
                )
    print(json.dumps({"changed": changed}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

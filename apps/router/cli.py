from __future__ import annotations

import sys

from apps.router.repo_lint import format_report, validate_repo_backbone


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    if not args or args[0] in {"-h", "--help"}:
        print("Usage: python3 -m apps.router.cli validate-repo")
        return 0

    if args[0] == "validate-repo":
        report = validate_repo_backbone()
        print(format_report(report))
        return 0 if report.is_valid else 1

    print(f"Unknown command: {args[0]}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

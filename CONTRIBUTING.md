# Contributing to ClawShire CLI

Thank you for your interest! We welcome bug reports, feature suggestions, and code contributions.

## Types of Contributions

| Type | Description |
|------|-------------|
| **Bug fixes** | Fix CLI errors, API compatibility issues, crashes |
| **New features** | Add new commands, output formats, SDK methods |
| **Documentation** | Improve README, examples, or docstrings |
| **Tests** | Add test cases or improve coverage |

---

## Questions & Feedback

Before opening an issue:

1. Check the [README](./README.md) and existing [Issues](https://github.com/memect/clawshire-cli/issues)
2. Confirm the problem is reproducible on the latest version

**Bug reports** should include:
- Steps to reproduce
- Expected vs. actual behavior
- Environment info (OS, Python version, clawshire-cli version)

**Feature requests** should describe the use case and preferred interface.

---

## Contributing Code

### Prerequisites

| Tool | Version |
|------|---------|
| Python | >= 3.12 |
| [uv](https://docs.astral.sh/uv/) | latest |

### Workflow

```bash
# 1. Fork and clone
git clone https://github.com/<your-username>/clawshire-cli.git
cd clawshire-cli

# 2. Install dependencies
uv sync

# 3. Create a branch
git checkout -b feat/my-feature

# 4. Make changes, then push and open a PR against main
git push origin feat/my-feature
```

### Validation

Before submitting a PR:
- Run `./scripts/e2e_local_check.sh` to verify nothing is broken
- Keep each PR to a single goal

---

## Commit Message Format

```
<type> <short description>
```

| Type | When to use |
|------|-------------|
| `Add` | New feature, file, or dependency |
| `Fix` | Bug fix |
| `Update` | Improvement to existing functionality |
| `Refactor` | Code restructure with no behavior change |
| `Docs` | Documentation-only change |
| `Chore` | Build, tooling, or config change |

---

## License

By submitting a contribution, you agree that your work will be distributed under the [MIT License](./LICENSE).

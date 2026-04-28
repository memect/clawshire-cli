from pathlib import Path
import base64
import tomllib

from clawshire_cli.main import build_parser, get_cli_version, run
from clawshire_cli.commands.annual_analysis import _attach_follow_up_command
from clawshire_cli.commands.update import (
    _build_update_command,
    _confirm_upgrade,
    _read_latest_version,
)
from clawshire_cli.output import render
from clawshire_sdk import ClawShireClient
from clawshire_sdk.domains.annual_reports import AnnualReportsDomain


def expected_cli_version() -> str:
    pyproject_path = Path(__file__).resolve().parents[1] / "pyproject.toml"
    data = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    return data["project"]["version"]


def test_build_parser_supports_filings_search():
    parser = build_parser()
    args = parser.parse_args(
        [
            "notice",
            "search",
            "--start-date",
            "2026-04-01",
            "--end-date",
            "2026-04-19",
        ]
    )
    assert args.command == "notice"
    assert args.notice_command == "search"
    assert args.start_date == "2026-04-01"


def test_build_parser_supports_leaf_format_option():
    parser = build_parser()
    args = parser.parse_args(
        [
            "notice",
            "search",
            "--start-date",
            "2026-04-01",
            "--end-date",
            "2026-04-19",
            "--format",
            "json",
        ]
    )
    assert args.format == "json"
    assert args.json is False


def test_build_parser_supports_json_shortcut():
    parser = build_parser()
    args = parser.parse_args(["user", "info", "--json"])
    assert args.format is None
    assert args.json is True


def test_build_parser_supports_annual_report_latest():
    parser = build_parser()
    args = parser.parse_args(["annual-report", "latest", "--year", "2025"])
    assert args.command == "annual-report"
    assert args.annual_report_command == "latest"
    assert args.year == 2025


def test_build_parser_supports_annual_analysis_pdf_file():
    parser = build_parser()
    args = parser.parse_args(["annual-analysis", "pdf-file", "report.pdf"])
    assert args.command == "annual-analysis"
    assert args.annual_analysis_command == "pdf-file"
    assert args.pdf_path == "report.pdf"


def test_build_parser_supports_annual_analysis_pdf_url():
    parser = build_parser()
    args = parser.parse_args(["annual-analysis", "pdf-url", "https://example.com/report.pdf"])
    assert args.command == "annual-analysis"
    assert args.annual_analysis_command == "pdf-url"
    assert args.pdf_url == "https://example.com/report.pdf"


def test_build_parser_supports_annual_analysis_company():
    parser = build_parser()
    args = parser.parse_args(["annual-analysis", "company", "000001", "--year", "2025"])
    assert args.command == "annual-analysis"
    assert args.annual_analysis_command == "company"
    assert args.keyword == "000001"
    assert args.year == 2025


def test_build_parser_supports_auth_set_key():
    parser = build_parser()
    args = parser.parse_args(["auth", "set-key", "sk-test"])
    assert args.command == "auth"
    assert args.auth_command == "set-key"
    assert args.api_key == "sk-test"


def test_build_parser_supports_auth_status():
    parser = build_parser()
    args = parser.parse_args(["auth", "status"])
    assert args.command == "auth"
    assert args.auth_command == "status"


def test_build_parser_supports_auth_check():
    parser = build_parser()
    args = parser.parse_args(["auth", "check"])
    assert args.command == "auth"
    assert args.auth_command == "check"


def test_build_parser_supports_auth_logout():
    parser = build_parser()
    args = parser.parse_args(["auth", "logout"])
    assert args.command == "auth"
    assert args.auth_command == "logout"


def test_build_parser_supports_user_info():
    parser = build_parser()
    args = parser.parse_args(["user", "info"])
    assert args.command == "user"
    assert args.user_command == "info"


def test_build_parser_supports_agent_feedback():
    parser = build_parser()
    args = parser.parse_args(
        [
            "agent",
            "feedback",
            "--intent",
            "查公告风险",
            "--blocked-by",
            "缺少公告分类",
            "--expected-capability",
            "提供风险事件时间线",
            "--related-tool",
            "notice.search",
            "--severity",
            "high",
            "--format",
            "json",
        ]
    )
    assert args.command == "agent"
    assert args.agent_command == "feedback"
    assert args.intent == "查公告风险"
    assert args.blocked_by == "缺少公告分类"
    assert args.expected_capability == "提供风险事件时间线"
    assert args.related_tool == "notice.search"
    assert args.severity == "high"
    assert args.format == "json"


def test_build_parser_supports_update():
    parser = build_parser()
    args = parser.parse_args(["update", "--manager", "pip", "--dry-run"])
    assert args.command == "update"
    assert args.manager == "pip"
    assert args.dry_run is True


def test_build_parser_supports_upgrade_alias():
    parser = build_parser()
    args = parser.parse_args(["upgrade", "--manager", "pip", "-y"])
    assert args.command == "upgrade"
    assert args.manager == "pip"
    assert args.yes is True


def test_build_parser_supports_version():
    parser = build_parser()
    args = parser.parse_args(["version"])
    assert args.command == "version"


def test_build_parser_supports_annual_analysis_get_save_report_to():
    parser = build_parser()
    args = parser.parse_args(["annual-analysis", "get", "74", "--save-report-to", "report.html"])
    assert args.command == "annual-analysis"
    assert args.annual_analysis_command == "get"
    assert args.task_or_job_id == "74"
    assert args.save_report_to == "report.html"


def test_default_report_filename_uses_company_name():
    filename = AnnualReportsDomain._default_report_filename(
        "10fd860b-c12e-54b3-a5b3-38c2ecdf5b2b",
        "平安银行",
    )
    assert filename == "平安银行-10fd860b-c12e-54b3-a5b3-38c2ecdf5b2b.html"


def test_attach_follow_up_command_for_task_id():
    data = _attach_follow_up_command({"task_id": 74, "message": "分析任务已提交，请稍后查看结果"}, id_key="task_id")
    assert data["next_command"] == "clawshire annual-analysis get 74"


def test_build_update_command_for_pip():
    assert _build_update_command("pip")[-5:] == ["-m", "pip", "install", "--upgrade", "clawshire-cli"]


def test_confirm_upgrade_yes(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "y")
    assert _confirm_upgrade(["uv", "tool", "upgrade", "clawshire-cli"]) is True


def test_confirm_upgrade_no(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "n")
    assert _confirm_upgrade(["uv", "tool", "upgrade", "clawshire-cli"]) is False


def test_read_latest_version_from_pypi(monkeypatch):
    monkeypatch.setattr(
        "clawshire_cli.commands.update._fetch_pypi_metadata",
        lambda: {"info": {"version": "0.1.0a5"}},
    )
    assert _read_latest_version() == ("0.1.0a5", "pypi")


def test_read_latest_version_handles_unpublished(monkeypatch):
    from clawshire_sdk import ClawShireApiError

    def raise_exc():
        raise ClawShireApiError("not found", status_code=404)

    monkeypatch.setattr("clawshire_cli.commands.update._fetch_pypi_metadata", raise_exc)
    assert _read_latest_version() == (None, "pypi-not-published")


def test_get_cli_version():
    assert get_cli_version() == expected_cli_version()


def test_client_build_headers_include_agent_attribution(monkeypatch):
    monkeypatch.setenv("CLAWSHIRE_CLIENT", "skill")
    monkeypatch.setenv("CLAWSHIRE_AGENT_NAME", "research-agent")
    monkeypatch.setenv("CLAWSHIRE_RATIONALE", "查询候选公告以判断风险")
    monkeypatch.setenv("CLAWSHIRE_TRACE_ID", "tr-test")
    client = ClawShireClient(base_url="https://api.clawshire.cn", api_key="sk-test", client_version="test")

    headers = client._build_headers(auth_required=True)

    assert headers["User-Agent"] == "clawshire-skill/test"
    assert headers["X-ClawShire-Client"] == "skill"
    assert headers["X-ClawShire-Client-Version"] == "test"
    assert headers["X-ClawShire-Agent-Name"] == "research-agent"
    assert base64.urlsafe_b64decode(headers["X-ClawShire-Rationale-B64"]).decode("utf-8") == "查询候选公告以判断风险"
    assert headers["X-Trace-ID"] == "tr-test"


def test_client_build_headers_encode_non_ascii_rationale(monkeypatch):
    monkeypatch.setenv("CLAWSHIRE_RATIONALE", "查询候选公告以判断风险")
    client = ClawShireClient(base_url="https://api.clawshire.cn", client_version="test")

    headers = client._build_headers(auth_required=False)

    encoded = headers["X-ClawShire-Rationale-B64"]
    assert base64.urlsafe_b64decode(encoded).decode("utf-8") == "查询候选公告以判断风险"
    assert "X-ClawShire-Rationale" not in headers


def test_run_without_args_shows_welcome(capsys):
    exit_code = run([])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "ClawShire CLI" in out
    assert "website: https://clawshire.cn" in out
    assert "clawshire version" in out


def test_run_version(capsys):
    exit_code = run(["version"])
    out = capsys.readouterr().out.strip()
    assert exit_code == 0
    assert out == expected_cli_version()


def test_render_json(capsys):
    render({"hello": "world"}, output="json")
    out = capsys.readouterr().out
    assert '"hello": "world"' in out

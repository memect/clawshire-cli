from clawshire_cli.main import build_parser, get_cli_version, run
from clawshire_cli.commands.annual_analysis import _attach_follow_up_command
from clawshire_cli.output import render
from clawshire_sdk.domains.annual_reports import AnnualReportsDomain


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


def test_build_parser_supports_user_info():
    parser = build_parser()
    args = parser.parse_args(["user", "info"])
    assert args.command == "user"
    assert args.user_command == "info"


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


def test_get_cli_version():
    assert get_cli_version() == "0.1.0a2"


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
    assert out == "0.1.0a2"


def test_render_json(capsys):
    render({"hello": "world"}, output="json")
    out = capsys.readouterr().out
    assert '"hello": "world"' in out

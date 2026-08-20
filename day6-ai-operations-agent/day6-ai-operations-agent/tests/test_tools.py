from tools import calculator_tool, run_tool, summary_writer_tool, system_status_tool, ticket_lookup_tool


def test_calculator_tool_adds_and_multiplies():
    result = calculator_tool("42 * 8 + 17")

    assert result["tool"] == "calculator"
    assert result["result"] == 353


def test_calculator_tool_rejects_unsafe_code():
    result = calculator_tool("__import__('os').system('echo unsafe')")

    assert result["tool"] == "calculator"
    assert "error" in result


def test_ticket_lookup_tool_returns_ticket():
    result = ticket_lookup_tool("inc1002")

    assert result["tool"] == "ticket_lookup"
    assert result["ticket_id"] == "INC1002"
    assert result["status"] == "In Progress"


def test_system_status_tool_returns_mock_status():
    result = system_status_tool("payment service")

    assert result["tool"] == "system_status"
    assert result["service_name"] == "payment service"
    assert result["overall_status"] == "Healthy"


def test_summary_writer_tool_returns_summary():
    result = summary_writer_tool("First issue happened. Second update happened. Third action happened.")

    assert result["tool"] == "summary_writer"
    assert result["summary"] == "First issue happened"
    assert len(result["bullet_points"]) == 3


def test_run_tool_handles_unknown_tool():
    result = run_tool("unknown", {})

    assert "error" in result

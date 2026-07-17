import logging

from app.infra.logging.logging_lib_adapter import LoggingLibAdapter


def test_info_delega_para_o_logger_da_lib_padrao(caplog) -> None:
    adapter = LoggingLibAdapter("teste_info")

    with caplog.at_level(logging.INFO, logger="teste_info"):
        adapter.info("mensagem de info")

    assert "mensagem de info" in caplog.text


def test_erro_delega_para_o_logger_da_lib_padrao(caplog) -> None:
    adapter = LoggingLibAdapter("teste_erro")

    with caplog.at_level(logging.ERROR, logger="teste_erro"):
        adapter.erro("mensagem de erro")

    assert "mensagem de erro" in caplog.text
    assert "ERROR" in caplog.text

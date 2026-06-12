import logging
import sys


# TODO: 今の設定は暫定対応。Google Cloudデプロイ時にstruct logを導入する予定(https://github.com/tsukuneA1/hoge/issues/18)
def configure_logging() -> None:
    logging.basicConfig(
        format="%(levelname)s %(message)s", stream=sys.stdout, level=logging.INFO, force=True
    )

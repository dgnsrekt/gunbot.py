# SYSTEM
from pathlib import Path

# THIRD-PARTY
import luigi
import structlog
import toml
import wget
import zipfile

# LOCAL
from paths import GUNBOT_DOWNLOAD_PATH, GUNBOT_DOWNLOAD_URL

logger = structlog.get_logger(__name__)


class DownloadTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget(str(GUNBOT_DOWNLOAD_PATH))

    def run(self):
        logger.info("Download Gunbot Linux", url=GUNBOT_DOWNLOAD_URL)
        wget.download(GUNBOT_DOWNLOAD_URL, self.output().path)


class ExtractandVerifyTask(luigi.Task):
    pass


luigi.build([DownloadTask()], local_scheduler=True)

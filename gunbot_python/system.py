# SYSTEM
from pathlib import Path
import shutil

# THIRD-PARTY
import luigi
import structlog
import toml
import wget
from zipfile import ZipFile

# LOCAL
from paths import (
    GUNBOT_DOWNLOAD_PATH,
    GUNBOT_DOWNLOAD_URL,
    GUNBOT_PATH,
    TEMP_GUNBOT_EXTRACTION_PATH,
)
from log import config_logger

logger = structlog.get_logger(__file__)

config_logger(loglevel="DEBUG")


class DownloadTask(luigi.Task):
    def output(self):
        return luigi.LocalTarget(str(GUNBOT_DOWNLOAD_PATH))

    def run(self):
        logger.info("Downloading Gunbot Linux", url=GUNBOT_DOWNLOAD_URL)
        wget.download(GUNBOT_DOWNLOAD_URL, self.output().path)


class ExtractandVerifyTask(luigi.Task):
    def requires(self):
        return DownloadTask()

    def output(self):
        paths = [
            GUNBOT_PATH,
            GUNBOT_PATH / "gunthy-linx64",
            GUNBOT_PATH / "config.js",
            GUNBOT_PATH / "config-js-example.txt",
            GUNBOT_PATH / "gui/",
            GUNBOT_PATH / "gui/node_modules/",
            GUNBOT_PATH / "gui/node_modules/bcrypt/",
            GUNBOT_PATH / "gui/node_modules/bcrypt/lib/",
            GUNBOT_PATH / "gui/node_modules/bcrypt/lib/binding/",
            GUNBOT_PATH / "gui/node_modules/bcrypt/lib/binding/bcrypt_lib.node",
            GUNBOT_PATH / "gui/node_modules/sqlite3/",
            GUNBOT_PATH / "gui/node_modules/sqlite3/lib/",
            GUNBOT_PATH / "gui/node_modules/sqlite3/lib/binding/",
            GUNBOT_PATH / "gui/node_modules/sqlite3/lib/binding/node-v57-linux-x64/",
            GUNBOT_PATH
            / "gui/node_modules/sqlite3/lib/binding/node-v57-linux-x64/node_sqlite3.node",
            GUNBOT_PATH / "node_modules/bcrypt/lib/binding/bcrypt_lib.node",
            GUNBOT_PATH / "node_modules/keyv/LICENSE",
            GUNBOT_PATH / "node_modules/keyv/package.json",
            GUNBOT_PATH / "node_modules/keyv/README.md",
            GUNBOT_PATH / "node_modules/keyv/src/",
            GUNBOT_PATH / "node_modules/keyv/src/index.js",
            GUNBOT_PATH / "node_modules/sqlite3/lib/",
            GUNBOT_PATH / "node_modules/sqlite3/lib/binding/",
            GUNBOT_PATH / "node_modules/sqlite3/lib/binding/node-v57-linux-x64/",
            GUNBOT_PATH / "node_modules/sqlite3/lib/binding/node-v57-linux-x64/node_sqlite3.node",
            GUNBOT_PATH / "tulind/",
            GUNBOT_PATH / "tulind/lib/",
            GUNBOT_PATH / "tulind/lib/binding/",
            GUNBOT_PATH / "tulind/lib/binding/Release/",
            GUNBOT_PATH / "tulind/lib/binding/Release/node-v57-linux-x64/",
            GUNBOT_PATH / "tulind/lib/binding/Release/node-v57-linux-x64/tulind.node",
        ]
        paths = [luigi.LocalTarget(str(p)) for p in paths]
        return paths

    def run(self):

        if GUNBOT_PATH.exists():
            shutil.rmtree(str(GUNBOT_PATH))

        with ZipFile(self.input().path) as zip:
            zip.extractall(TEMP_GUNBOT_EXTRACTION_PATH)
            assert (TEMP_GUNBOT_EXTRACTION_PATH / "lin").exists()

        shutil.move(str(TEMP_GUNBOT_EXTRACTION_PATH / "lin"), self.output()[0].path)
        assert GUNBOT_PATH.exists()

        shutil.rmtree(str(TEMP_GUNBOT_EXTRACTION_PATH))
        assert not TEMP_GUNBOT_EXTRACTION_PATH.exists()

        for p in self.output():
            logger.info("Checking gunbot path.", path=p.path, exists=Path(p.path).exists())


class SystemCheck(luigi.WrapperTask):
    def requires(self):
        return ExtractandVerifyTask()


luigi.build([SystemCheck()], local_scheduler=True)

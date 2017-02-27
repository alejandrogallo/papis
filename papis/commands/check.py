from ..document import Document
import papis
import sys
import os
import papis.utils
from . import Command


class Check(Command):
    def init(self):
        """TODO: Docstring for init.

        :subparser: TODO
        :returns: TODO

        """
        check_parser = self.parser.add_parser(
                "check",
                help="Check document document from a given library"
                )
        check_parser.add_argument(
                "document",
                help="Document search",
                nargs="?",
                default=".",
                action="store"
                )
        check_parser.add_argument(
                "--keys", "-k",
                help="Key to check",
                nargs="*",
                default=[],
                action="store"
                )


    def main(self, config, args):
        """
        Main action if the command is triggered

        :config: User configuration
        :args: CLI user arguments
        :returns: TODO

        """
        documentsDir = os.path.expanduser(config[args.lib]["dir"])
        self.logger.debug("Using directory %s"%documentsDir)
        documentSearch = args.document
        folders = papis.utils.getFilteredFolders(documentsDir, documentSearch)
        allOk = True
        for folder in folders:
            self.logger.debug(folder)
            document   = Document(folder)
            allOk &= document.checkFile()
            for key in args.keys:
                if not key in document.keys():
                    allOk &= False
                    print("%s not found in %s"%(key, folder))
        if not allOk:
            print("Errors were detected, please fix the info files")
        else:
            print("No errors detected")
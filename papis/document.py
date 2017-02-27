import os
import yaml
import logging
import papis.utils
import papis.bibtex

class Document(object):

    """
     Structure implementing all information inside a document,
     which should be yaml information with few methods
    """

    def __init__(self, folder):
        self._keys = []
        self._folder = folder
        self.logger = logging.getLogger("Doc")
        self._infoFilePath = os.path.join(folder, papis.utils.getInfoFileName())
        self.loadInformationFromFile()
    def __setitem__(self, obj, value):
        """
        :obj: TODO
        :returns: TODO
        """
        self._keys.append(obj)
        setattr(self, obj, value)
    def __getitem__(self, obj):
        """
        :obj: TODO
        :returns: TODO
        """
        return getattr(self, obj) if hasattr(self, obj) else None
    def getMainFolder(self):
        """
        Get main folder where the document and the information is stored
        :returns: TODO

        """
        return self._folder
    def checkFile(self):
        """
        :returns: TODO
        """
        # Check for the exsitence of the document
        if not os.path.exists(self.getFile()):
            print("** Error: %s not found in %s"%(self.getFile(), self.getMainFolder()))
            return False
        else:
            return True
    def save(self):
        """
        :returns: TODO
        """
        fd = open(self._infoFilePath, "w+")
        structure = dict()
        for key in self.keys():
            structure[key] = self[key]
        yaml.dump(structure, fd, default_flow_style=False)
        fd.close()
    def toBibtex(self):
        """
        :f: TODO
        :returns: TODO
        """
        bibtexString = ""
        bibtexType = ""
        # First the type, article ....
        if "type" in self.keys():
            if self["type"] in papis.bibtex.bibtexTypes:
                bibtexType = self["type"]
        if not bibtexType:
            bibtexType = "article"
        if not self["ref"]:
            ref = os.path.basename(self._folder)
        else:
            ref = self["ref"]
        bibtexString += "@%s{%s,\n"%(bibtexType, ref)
        for bibKey in papis.bibtex.bibtexKeys:
            if bibKey in self.keys():
                bibtexString += "\t%s = { %s },\n"%(bibKey, self[bibKey])
        bibtexString += "}\n"
        return bibtexString
    def update(self, data, force = False, interactive = False):
        """TODO: Docstring for update.

        :data: TODO
        :force: TODO
        :interactive: TODO
        :returns: TODO

        """
        self.logger.debug("Updating...")
        for key in data:
            if self[key] != data[key]:
                if force:
                    self[key] = data[key]
                elif interactive:
                    confirmation = input("(%s conflict) Replace '%s' by '%s'? (y/N)"%(
                        key, self[key], data[key]
                        ) ) or "N"
                    if confirmation in "Yy":
                        self[key] = data[key]
                else:
                    pass
    def getInfoFile(self):
        """TODO: Docstring for getFiles.
        :returns: TODO

        """
        return self._infoFilePath
    def getFile(self):
        """TODO: Docstring for getFiles.
        :returns: TODO

        """
        return os.path.join(self._folder, self["file"])
    def keys(self):
        """TODO: Docstring for keys().

        :arg1: TODO
        :returns: TODO

        """
        return self._keys
    def dump(self):
        """TODO: Docstring for dump.
        :returns: TODO

        """
        string = ""
        for i in self.keys():
            string += str(i)+":   "+str(self[i])+"\n"
        return string
    def loadInformationFromFile(self):
        """
        load information from file
        :returns: TODO
        """
        try:
            fd = open(self._infoFilePath, "r")
        except:
            print("Warning: No info file found")
            return False
        structure = yaml.load(fd)
        fd.close()
        for key in structure:
            self[key] = structure[key]
import os

from conans import ConanFile, tools, MSBuild
from conans.tools import replace_in_file

class LibHunspellConan(ConanFile):
    name = "libhunspell"
    description = "libhunspell from Hunspell project"
    version = "1.6.2"
    license = "GPL 2"
    url = "https://github.com/hunspell/hunspell.git"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True,False]}
    default_options = "shared=False"

    scm = {
        "type": "git",
        "url": "https://github.com/hunspell/hunspell.git",
        "revision": "89d1084f1760c2cdbe1b636eb1cdc15e6f3ac519" # 1.6.2 + fixes
    }

    def build(self):
        if self.settings.compiler != "Visual Studio":
            raise "Only Visual Studio is supported at the moment"
        
        replace_in_file("msvc\\libhunspell.vcxproj", "v140_xp", "v140")
        msbuild = MSBuild(self)
        msbuild.build("msvc\\Hunspell.sln", targets=["libhunspell"])
        
    def package(self):
        for h in ["hunspell.hxx", "hunspell.h", "hunvisapi.h", "w_char.hxx", "atypes.hxx"]:
            self.copy(h, dst="include/hunspell", src="src\\hunspell")
        self.copy("*libhunspell.dll", dst="bin", keep_path=False)
        self.copy("*libhunspell.dylib", dst="bin", keep_path=False)
        self.copy("*libhunspell.so*", dst="bin", keep_path=False)
        self.copy("*libhunspell.lib", dst="lib", keep_path=False)
        self.copy("*libhunspell.a", dst="lib", keep_path=False)
        
    def package_info(self):
        if self.settings.compiler == "Visual Studio":
            self.cpp_info.libs = ["libhunspell.lib"]
        else:
            self.cpp_info.libs = ["hunspell"]
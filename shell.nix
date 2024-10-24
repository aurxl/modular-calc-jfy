{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs; [
      pandoc
      poetry
      neovim
      python312
      python312Packages.pyqt6
      qtcreator
      stdenv.cc.cc.lib
    ];

  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";

  shellHook = ''
    export PYTHON_KEYRING_BACKEND=keyring.backends.null.Keyring
    poetry env use $(which python)
    source $(poetry env info --path)/bin/activate
  '';

}
